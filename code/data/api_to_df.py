import webhoseio
import pandas as pd
import datetime as dt
import boto3
from pandas.io.json import json_normalize
import numpy as np
from urllib.error import HTTPError
from fuzzywuzzy import fuzz
from user_definition_api import *
from info import *


def get_query(site_lists, time_delta):
    """
    Get query for webhose api given a site_lists and time window

    :param site_lists: list of sites we need to crawl
    :param time_delta: time window, -3 means recent 3 days.
                       Can only be from -1 to -30
    :return: a string of query for webhose api
    """
    q = "language:english site_type:news thread.country:US "
    if len(site_lists) == 1:
        sites = 'site:' + site_lists[0]
    else:
        sites = ' OR '.join(['site:' + x for x in site_lists])
    q = q+'('+sites+')'
    ts = dt.datetime.now()+dt.timedelta(time_delta)
    query_params = {"q": q,
                    "ts": str(int(dt.datetime.timestamp(ts)*1000)),
                    "sort": "published"}
    return query_params


def output_to_df(output, df):
    """
    Convert a single output (100 news) from webhose to pandas data frame
    and concat to previous data frame

    :param output:
        a json output from single webhose query
    :param df:
        previous pandas data frame from previous query,
            each row represent one news
    :return:
        pandas data frame, each row represent one news
    """
    output_flat = pd.io.json.json_normalize(output['posts'])
    df_tmp = output_flat[['thread.uuid', 'author', 'external_links',
                          'published', 'text', 'thread.site_full',
                          'thread.site_categories', 'thread.site_section',
                          'thread.section_title', 'thread.main_image',
                          'thread.social.facebook.comments',
                          'thread.social.facebook.likes',
                          'thread.social.facebook.shares', 'title', 'url']]
    df = pd.concat([df, df_tmp], axis=0)
    return df


def api_df(token, site_lists, time_delta, filename):
    """
    A pipeline from api to csv

    :param token:
        api token for webhose
    :param site_lists:
        list of sites we need to crawl
    :param time_delta:
        time window, -3 means recent 3 days.  Can only be from -1 to -30
    :param filename:
        filename of csv
    :return:
        None
    """
    webhoseio.config(token=token)
    query_params = get_query(site_lists, time_delta)
    output_init = webhoseio.query("filterWebContent", query_params)
    output_flat = pd.io.json.json_normalize(output_init['posts'])
    df = output_flat[['thread.uuid', 'author', 'external_links', 'published',
                      'text', 'thread.site_full', 'thread.site_categories',
                      'thread.site_section', 'thread.section_title',
                      'thread.main_image', 'thread.social.facebook.comments',
                      'thread.social.facebook.likes',
                      'thread.social.facebook.shares', 'title', 'url']]
    output = webhoseio.get_next()
    while len(output['posts']) > 0:
        df = output_to_df(output, df)
        try:
            output = webhoseio.get_next()
        except HTTPError:
            return df
            # df.to_csv(filename, index=False)
        if len(df) % 1000 == 0:
            print(str(len(df)) + ' has finished')
    return df


def pre_process_data(df, filename):
    """
    Pre-process data got from api:
    drop duplicates
    drop articles with no title, image, url and text
        less than 200 words
    drop articles with correct author name
    """

    # remove articles without title, title, url and main_image
    cols = ['thread.uuid', 'title', 'text',
            'thread.main_image', 'published', 'url',
            'thread.site_full', 'author']

    clean = df[cols]

    clean = clean.dropna()

    to_remove = ['rss.cnn.com', 'cnnespanol.cnn.com',
                 'execed.economist.com', 'espndeportes.espn.com',
                 'events.latimes.com', 'gmat.economist.com',
                 'gre.economist.com', 'long-island-jobs.newsday.com',
                 'interactive.aljazeera.com', 'markets.businessinsider.com',
                 'partners.wsj.com', 'rss.cnn.com', 'tv5.espn.com',
                 'video.cnbc.com', 'ww.npr.org', 'www3.forbes.com']

    clean = clean[clean['thread.site_full'].map(
        lambda x: x not in to_remove)]

    # drop duplicate

    clean = clean.drop_duplicates(subset='thread.uuid')
    clean = clean.reset_index(drop=True)

    titles = clean['title'].values

    to_drop = []

    for i in range(len(titles) - 4):
        f1 = fuzz.ratio(titles[i], titles[i + 1])
        f2 = fuzz.ratio(titles[i], titles[i + 2])
        f3 = fuzz.ratio(titles[i], titles[i + 3])
        f4 = fuzz.ratio(titles[i], titles[i + 4])
        if f1 > 90 or f2 > 90 or f3 > 90 or f4 > 90:
            to_drop.append(i)

    clean.drop(to_drop, inplace=True)
    clean.reset_index(inplace=True, drop=True)

    # clean text
    clean = clean[clean['text'].str.split(' ').map(
        lambda x: len(x) >= 200)]

    # clean author
    clean = clean[clean['author'].str.len() <= 256]
    clean['author'] = clean['author'].map(
        lambda x: x.split(',')[0] if ',' in x else x)

    clean.replace('', np.nan, inplace=True)
    clean.dropna(inplace=True, how='any')
    clean.to_csv(filename, index=False)

    return clean


def write_s3(filename):
    """
    Write data to s3 bucket
    """
    # write DF to string stream
    s3 = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key)

    with open(filename, "rb") as f:
        s3.upload_fileobj(f, "newsphi", "news_articles"+filename)


if __name__ == '__main__':
    data = api_df(token, site_lists, time_delta, filename)
    pre_process_data(data, filename)
    write_s3(filename)
