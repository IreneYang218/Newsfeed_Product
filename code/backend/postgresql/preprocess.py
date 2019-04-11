import numpy as np
import pandas as pd


def pre_process_output(output_path):
    """
    Pre-process models' output
    Only keep website used columns
    Remove unquantified ariticles under restrictions
    """
    data = pd.read_csv(output_path)
    used_columns =["title", "author", "published", "thread.site_full", "thread.main_image",
                "url", "Dominant_Topic", "Keywords"]
    output = data[used_columns]
    # remove articles without title and main_image
    output = output[~output[['title','thread.main_image']].isnull().any(axis=1)]
    output.to_csv('sample_data_topics.csv', index=False)