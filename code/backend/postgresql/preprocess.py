import numpy as np
import pandas as pd


def pre_process_output(input_path, output_path):
    """
    Pre-process models' output
    Only keep website used columns
    Remove unquantified ariticles under restrictions
    """
    data = pd.read_csv(input_path)
    used_columns = ["title", "author", "published", "thread.site_full",
                    "thread.main_image", "url", "Dominant_Topic"]
    OBJ_COLS = ['title', 'author', 'thread.site_full', 'thread.main_image',
                'url']
    
    output = data[used_columns]

    # remove articles without title and main_image
    output = output[~output[['title', 'thread.main_image']]
                    .isnull().any(axis=1)]
    
    # remove unqualified rows
    for column in OBJ_COLS:
        output = output[output[column].str.len()<=256]
    output.to_csv(output_path, index=False)


if __name__ == '__main__':
    input_path = '../sample_data/result_with_25_topics.csv'
    output_path = '../sample_data/sample_data_topics.csv'
    pre_process_output(input_path, output_path)
