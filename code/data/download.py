import boto3
from info import *
import pandas as pd

# Declare S3 as the destination
s3 = boto3.resource('s3')
bucket = s3.Bucket('newsphi')

# Reading a single file
obj = s3.meta.client.get_object(Bucket='newsphi',
                                Key='testing/news_clean_march.csv')
df = pd.read_csv(obj['Body'])
# print(sales)

# for obj in bucket.objects.all():
#     key = obj.key
#     body = obj.get()['Body'].read()
#     print('The current directory is: ', key)
#     print(body)

df.to_csv('downloaded_data.csv')
