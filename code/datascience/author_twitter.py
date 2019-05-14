import pandas as pd
import tweepy
import numpy as np
from author_user_definition import *


def loadkeys(filename):
    """"
    Load Twitter API keys/tokens from CSV file with format:
    consumer_key, consumer_secret, access_token, access_token_secret.
    """
    with open(filename) as f:
        items = f.readline().strip().split(',')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file containing the Twitter keys and tokens,
    create and return a Tweepy API object.
    """
    consumer_key, consumer_secret, \
        access_token, access_token_secret = loadkeys(twitter_auth_filename)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(
        auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return api


def fetch_user(api, con_dict):
    """
    Given a Tweepy API object and the con_dict of
    the authors' Twitter accounts,
    append authors' twitter information in the original dictionary.
    The key-values pairs contain:
        followers_count: The number of followers this account currently has.
        listed_count: The number of public lists that
            this user is a member of a list.
        verified: Whether the Twitter account is verified or not.
    :param api: Twitter API.
    :param con_dict: authors's dictionary with screen name.
    :return: a dictionary with all new key_values pairs appended.
    """
    user = api.get_user(screen_name=con_dict['author_screen_name'])
    con_dict['verified'] = user.verified
    con_dict['followers_count'] = user.followers_count
    con_dict['listed_count'] = user.listed_count
    return con_dict


if __name__ == '__main__':
    api = authenticate(token_file)
    author_df = pd.read_csv(author_search, sep=',', error_bad_lines=False)
    author_df = author_df.fillna('')
    author_df_found = author_df.loc[author_df.author_screen_name != '', ]
    con_info = author_df_found.T.to_dict().values()
    new_con = list()
    for i, c in enumerate(con_info):
        if i % 500 == 0:
            print(i)
        c = fetch_user(api, c)
        new_con.append(c)
    df_new = pd.DataFrame.from_dict(new_con)
    df_new['rep_score'] = np.log(df_new['followers_count'] + 1) / (
                np.log(df_new['listed_count'] + 1) + 0.01)
    df_new['rep_score_rank'] = df_new['rep_score'].rank()
    df_new['followers_count_rank'] = df_new['followers_count'].rank(
        ascending=False)
    df_new['listed_count_rank'] = df_new['listed_count'].rank(ascending=False)
    df_new.to_csv(author_twitter_rep, index=False)
