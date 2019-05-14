import numpy as np
import pandas as pd
import sys


def pre_process_output(input_path, output_path):
    """
    Pre-process models' output:
    only keeps websites used columns;
    removes unquantified ariticles under restrictions.
    """
    data = pd.read_csv(input_path)
    used_columns = ["title", "author", "published", "thread.site_full",
                    "thread.main_image", "url", "topic", "thread.uuid",
                    "sentiment", "General_Topic", 'controversy_score']
    OBJ_COLS = ['title', 'author', 'thread.site_full', 'thread.main_image',
                'url', 'thread.uuid']

    output = data[used_columns]

    # remove articles without title and main_image
    output = output[~output[['thread.uuid', 'title', 'thread.main_image',
                             'published', 'url', 'thread.site_full']]
                    .isnull().any(axis=1)]

    # remove unqualified rows
    for column in OBJ_COLS:
        output = output[output[column].str.len() <= 256]
    output.to_csv(output_path, index=False)


if __name__ == '__main__':
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    pre_process_output(input_path, output_path)
