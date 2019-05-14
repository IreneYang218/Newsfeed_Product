from info import *
import boto3
import pandas as pd
import io


def read_s3(folder, filename):
    """
    Read data from s3 bucket and return dataframe.
    """
    # write DF to string stream
    s3 = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key)

    obj = s3.get_object(Bucket="newsphi", Key=folder + "/" + filename)
    df = pd.read_csv(io.BytesIO(obj['Body'].read()))
    return df


def write_s3(folder, filename):
    """
    Write data to s3 bucket.
    """
    # write DF to string stream
    s3 = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key)

    with open(filename, "rb") as f:
        s3.upload_fileobj(f, "newsphi", folder + "/"+filename)
