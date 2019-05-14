import boto3
from info import *
import pandas as pd
import sys
import os


def downloaded_from_s3(filepath, output_path):
    """Download data from S3 bucket and return a CSV file."""
    # Declare S3 as the destination
    s3 = boto3.client('s3',
                      aws_access_key_id=key_id,
                      aws_secret_access_key=secret_key)

    filename = filepath.split("/")[-1]
    if output_path:
        if not os.path.exists(output_path):
            os.mkdir(output_path)
    s3.download_file('newsphi', filepath, output_path+filename)


if __name__ == '__main__':
    filepath = sys.argv[1]
    output_path = sys.argv[2]
    downloaded_from_s3(filepath, output_path)
