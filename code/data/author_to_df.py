import tweepy
from author_user_definition import *
from user_definition_api import *
from S3_connection import *
import numpy as np
import config


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
    append authors' Twitter information in the original dictionary.
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
    # Read new authors from today's update file and find distinct authors
    df = read_s3(news_folder, news_filename)
    author_list = df['author'].drop_duplicates().tolist()

    # connect to database and find current distinct authors
    conn = config.connect(config.dbconfig())
    conn.autocommit = True
    dbcursor = conn.cursor()
    dbcursor.execute("SELECT DISTINCT author_name FROM newsphi.news_authors")
    fetch = dbcursor.fetchall()
    db_set = set([fetch[i][0] for i in range(len(fetch))])

    # Find new authors that not in current data base
    author_set = set(author_list)
    new_author = list((author_set | db_set) - db_set)
    print(str(len(new_author)) + ' new authors to be searched')

    # search the screen_name of new authors
    api = authenticate(token_file)
    f = open(author_search, "w")
    f.write('idx,author,author_screen_name\n')
    f.close()
    for i, a in enumerate(author_list):
        if i % 500 == 0:
            print(str(i) + ' ' + 'author scraped')
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

    # fetch authors info and calculate reputation scores
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
