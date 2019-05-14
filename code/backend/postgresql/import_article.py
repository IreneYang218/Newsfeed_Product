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
    Read news articles' files and process to the format for database.
    """
    df = pd.read_csv(filepath)

    df.rename(columns={'thread.site_full': 'site_full',
                       'thread.main_image': 'main_image',
                       'url': 'post_link',
                       'topic': 'news_topic',
                       'published': 'published_time',
                       'sentiment': 'sentiment_score',
                       'thread.uuid': 'article_id',
                       'General_Topic': 'general_topic'},
              inplace=True)
    OBJ_COLS = ['title', 'author', 'site_full', 'main_image',
                'post_link', 'news_topic', 'article_id', 'general_topic']
    INT_COLS = ['controversy_score', 'sentiment_score']
    TIME_COLS = ['published_time']
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
    for i in range(len(df)):
        f = StringIO()
        df.iloc[[i]].to_csv(f, sep='\t', header=False,
                            index=False, na_rep='NULL')
        f.seek(0)

        try:
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
    TABLE_NAME = 'news_articles'
    filepath = sys.argv[1]
    read_file_and_process(filepath, TABLE_NAME, SCHEMA_NAME)
