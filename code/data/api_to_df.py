import webhoseio
import pandas as pd
import datetime as dt
import boto3
from pandas.io.json import json_normalize
from urllib.error import HTTPError
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
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
    :param output: a json output from single webhose query
    :param df: previous pandas data frame from previous query,
               each row represent one news
    :return: pandas data frame, each row represent one news
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
    :param token: api token for webhose
    :param site_lists: list of sites we need to crawl
    :param time_delta: time window, -3 means recent 3 days.
                       Can only be from -1 to -30
    :param filename: filename of csv
    :return: None
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
            df.to_csv(filename, index=False)
        if len(df) % 1000 == 0:
            print(str(len(df)) + ' has finished')
    # df.to_csv(filename, index=False)
    return df


def write_s3(df, filename):
    """
    Write data to s3 bucket
    """
    # write DF to string stream
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # reset stream position
    csv_buffer.seek(0)
    # create binary stream
    gz_buffer = BytesIO()

    session = boto3.Session(aws_accaws_access_key_id=key_id,
                            aws_secret_access_key=secret_key)
    s3 = session.resource("s3")
    bucket = s3.Bucket('newsphi')
    s3.upload_file(gz_buffer, bucket, filename)


if __name__ == '__main__':
    api_df(token, site_lists, time_delta, filename)
