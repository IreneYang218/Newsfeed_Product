import psycopg2
import config
import pandas as pd
import numpy as np
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

in_files = 'sample_data.csv'
TABLE_NAME = 'sample'

df = pd.read_csv(in_files)

SCHEMA_NAME = 'news'
df.rename(columns={'Site Name':'Site_Name',
                    'Main Image':'Main_Image',
                    'Post Link':'Post_Link',
                    'Post Publication Date':'Post_Publication_Date'}, 
                 inplace=True)
OBJ_COLS = ['Title', 'Author', 'Site_Name', 'Main_Image', 'Post_Link']
INT_COLS = []
TIME_COLS = ['Post_Publication_Date']
df = df.replace([np.inf, -np.inf], np.nan)
sql_commands = ['DROP TABLE IF EXISTS %s.%s CASCADE' %(SCHEMA_NAME,TABLE_NAME)]

# print all_df.columns.to_series().groupby(all_df.dtypes).groups
cmd = 'CREATE TABLE %s.%s (' %(SCHEMA_NAME,TABLE_NAME)
for col in df.columns:
    if col in OBJ_COLS:
        df[col] = df[col].astype(str)
        df.loc[df[col]=='nan', col] = ''
        cmd += '%s text,' %col
    elif col in INT_COLS:
        df[col] = df[col].map('{:.0f}'.format)
        df.loc[df[col]=='nan', col] = 'NULL'
        cmd += '%s integer,' %col
    elif col in TIME_COLS:
    #    df[col] = df[col].map('{:.0f}'.format)
        df.loc[df[col]=='nan', col] = ''
        cmd += '%s timestamp,' %col
    else:
        cmd += '%s numeric,' %col
cmd += 'CONSTRAINT key PRIMARY KEY (Post_Link),'
cmd += 'CONSTRAINT unique_rec UNIQUE (Post_Link))'
sql_commands.append(cmd)
# sql_commands.append('GRANT SELECT ON TABLE %s.%s TO anon' %(SCHEMA_NAME,TABLE_NAME))

f = StringIO()
df.to_csv(f, sep='\t', header=False, index=False, na_rep='NULL')
f.seek(0)

conn = config.connect(config.dbconfig())
dbcursor = conn.cursor()

print('total number of records: %s' %len(df))

try:
   for command in sql_commands:
       dbcursor.execute(command)
  
   dbcursor.copy_from(f, '%s.%s' %(SCHEMA_NAME,TABLE_NAME), sep='\t', null='NULL')
except (Exception, psycopg2.DatabaseError) as error:
   print(error)
finally:
   conn.commit()
   conn.close()
