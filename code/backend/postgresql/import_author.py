import psycopg2
import config
import pandas as pd
import numpy as np
import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def read_file_and_process(filepath, TABLE_NAME, SCHEMA_NAME):
    """
    Read news authors' files and process to the format for database.
    """
    df = pd.read_csv(filepath)
    used_columns = ["author", "rep_score", "author_screen_name",
                    'rep_score_rank']
    df = df[used_columns]

    df.rename(columns={'author': 'author_name',
                       'rep_score': 'reputation_score',
                       'rep_score_rank': 'rank'},
              inplace=True)
    df['tweet_site'] = 'https://twitter.com/' + df.author_screen_name
    df.drop(columns=['author_screen_name'], inplace=True)
    OBJ_COLS = ['author_name', 'tweet_site']
    INT_COLS = ['reputation_score', 'rank']
    TIME_COLS = []
    df = df.replace([np.inf, -np.inf], np.nan)

    for col in df.columns:
        if col in OBJ_COLS:
            df[col] = df[col].astype(str)
            df.loc[df[col] == 'nan', col] = ''
        elif col in INT_COLS:
            df[col] = df[col].map('{:.4f}'.format)
            df.loc[df[col] == 'nan', col] = 'NULL'
        elif col in TIME_COLS:
            df.loc[df[col] == 'nan', col] = ''

    columns = df.columns
    print('total number of records: %s' % len(df))

    # Connect RDS database and copy data into database
    conn = config.connect(config.dbconfig())
    dbcursor = conn.cursor()

    # update_comm = 'INSERT INTO %s.%s (%s) VALUES (' %
    #   (SCHEMA_NAME, TABLE_NAME, ','.join(columns))
    # for row in df.iterrows():
    for i in range(len(df)):
        f = StringIO()
        df.iloc[[i]].to_csv(f, sep='\t', header=False,
                            index=False, na_rep='NULL')
        f.seek(0)
        try:
            # update_comm += '%s, %.2f, %s' % (row) + ');'
            # dbcursor.execute(,row)
            dbcursor.copy_from(f, '%s.%s' % (SCHEMA_NAME, TABLE_NAME),
                               sep='\t', null='NULL', columns=(columns))
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.rollback()
        if ((i+1) % 100 == 0):
            print('copy %d records' % (i+1))

    conn.close()


if __name__ == '__main__':
    SCHEMA_NAME = 'newsphi'
    TABLE_NAME = 'news_authors'
    filepath = sys.argv[1]
    read_file_and_process(filepath, TABLE_NAME, SCHEMA_NAME)
