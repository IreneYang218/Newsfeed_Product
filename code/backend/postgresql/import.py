import psycopg2
import config
import pandas as pd
import numpy as np
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def read_file_and_process(filepath, TABLE_NAME, SCHEMA_NAME):
    """
    Read files and process to the format for database
    """
    df = pd.read_csv(filepath)

    df.rename(columns={'thread.site_full':'site_full',
                        'thread.main_image':'main_image',
                        'url':'post_link'}, 
                    inplace=True)
    OBJ_COLS = ['title', 'author', 'site_full', 'main_image', 'post_link', 'Keywords']
    INT_COLS = ['Dominant_Topic']
    TIME_COLS = ['published']
    df = df.replace([np.inf, -np.inf], np.nan)

    for col in df.columns:
        if col in OBJ_COLS:
            df[col] = df[col].astype(str)
            df.loc[df[col]=='nan', col] = ''
        elif col in INT_COLS:
            df[col] = df[col].map('{:.0f}'.format)
            df.loc[df[col]=='nan', col] = 'NULL'
        elif col in TIME_COLS:
        #    df[col] = df[col].map('{:.0f}'.format)
            df.loc[df[col]=='nan', col] = ''

    f = StringIO()
    df.to_csv(f, sep='\t', header=False, index=False, na_rep='NULL')
    f.seek(0)
    print('total number of records: %s' %len(df))
    return f


def import_data(f):
    """Connect RDS database"""
    conn = config.connect(config.dbconfig())
    dbcursor = conn.cursor()

    try:
        dbcursor.copy_from(f, '%s.%s' %(SCHEMA_NAME,TABLE_NAME), sep='\t', null='NULL')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.commit()
        conn.close()


if __name__ == '__main__':
    TABLE_NAME = 'articles'
    SCHEMA_NAME = 'news'
    f = read_file_and_process('../sample_data/sample_data_topics.csv', TABLE_NAME, SCHEMA_NAME)
    import_data(f)