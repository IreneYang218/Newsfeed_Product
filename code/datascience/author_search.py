import pandas as pd
import tweepy
from author_user_definition import *


def loadkeys(filename):
    """"
    Load twitter API keys/tokens from CSV file with format:
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


if __name__ == '__main__':
    df = pd.read_csv(data_file)
    df_author = df['author'].drop_duplicates()
    df_author = df_author[~df_author.isnull()]
    api = authenticate(token_file)
    author_list = df_author.tolist()
    f = open(author_search, "w")
    f.write('idx,author,author_screen_name\n')
    f.close()
    for i, a in enumerate(author_list):
        if i % 500 == 0:
            print(str(i) + ' ' + 'author scraped')
        if ',' in str(a):
            a = str(a).split(',')[0]
        if (isinstance(a, str) and len(str(a).split(' '))) > 10:
            continue
        else:
            search = api.search_users(a)
        try:
            s_name = search[0].screen_name
        except IndexError:
            s_name = '\n'
        f = open(author_search, "a")
        f.write(str(i))
        f.write(',')
        f.write(str(a))
        f.write(',')
        f.write(str(s_name))
        f.write('\n')
        f.close()
