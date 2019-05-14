from texts2id_corpus import *
from user_definition_model import *
from user_definition_api import *
from S3_connection import *
import pandas as pd
import spacy
import gensim
import gensim.corpora as corpora
from gensim.models.wrappers import LdaMallet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def para_filter(x):
    """
    Preprocess the news text, return the first paragraph more than 20 words.
    """
    para = x.split('\n')
    for p in para:
        if len(p.split(' ')) >= 20:
            return p


def format_topics_sentences(ldamodel, corpus, df_assign):
    """
    Mapping the news topics to news texts,
    return the dataframe contains index and assigned news topics.
    """
    # Init output
    sent_topics_df = pd.DataFrame()

    # Get main topic in each document
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        # Get the Dominant topic,
        # Perc Contribution and Keywords for each document
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                sent_topics_df = sent_topics_df.append(
                    pd.Series([int(topic_num), round(prop_topic, 4),
                               topic_keywords]), ignore_index=True)
            else:
                break
    sent_topics_df.columns = ['Dominant_Topic',
                              'Perc_Contribution', 'Topic_Keywords']
    sent_topics_df = sent_topics_df.reset_index()

    # Get the assign topics
    df_topic = pd.merge(sent_topics_df, df_assign,
                        on='Dominant_Topic', how='left')
    return df_topic


def predict(model_name, df, model_type, df_assign):
    """
    Use the model to predict topics on new data,
    return the dataframe with uuid and assigned news topics.
    """
    mallet_path = 'mallet-2.0.8/bin/mallet'
    model = gensim.models.wrappers.LdaMallet.load(model_name)
    first_para = df.text.apply(lambda x: para_filter(x))
    test_texts = df.title + ' ' + first_para
    test_texts = test_texts.dropna()
    df = df[~test_texts.isnull()]
    test_id2text, test_corpus, test_words_lemmatized = \
        text2corpus(test_texts, num_gram=3)
    predict_result = format_topics_sentences(
        ldamodel=model, corpus=test_corpus, df_assign=df_assign)
    result = pd.concat([df, predict_result], axis=1)
    if model_type == 'general':
        df_general = result[['thread.uuid', 'General_Topic']]
        return df_general
    if model_type == 'specific':
        df_specific = result[['thread.uuid', 'topic']]
        return df_specific
    else:
        print('model is not exist')


def calculate_sentiment(df):
    """
    Calculate the sentiment score of each articles,
    return a dataframe contains uuid and responding sentiment score.
    """
    SIA = SentimentIntensityAnalyzer()
    df['sentiment'] = df['text'].apply(
        lambda x: SIA.polarity_scores(x)['compound'])
    df_sentiment = df[['thread.uuid', 'thread.site_full', 'thread.main_image',
                       'url', 'author', 'published', 'sentiment']]
    return df_sentiment


def merge_topic_sentiment(df_general, df_specific, df_sentiment):
    """
    Merge the results of two topic modeling and sentiment score by uuid,
    generate the model output into a CSV file.
    """
    df_topic2 = pd.merge(df_general, df_specific, on='thread.uuid')
    df_final = pd.merge(df_topic2, df_sentiment, on='thread.uuid')
    df_final.to_csv(output, index=False)


if __name__ == '__main__':
    # specify model path:
    mallet_path = mallet_path

    # read the preprocessed the data
    df = read_s3(news_folder, news_filename)

    # get the general topics
    general_assign = read_s3('news_topics', general_assign_filename)
    df_general = predict(general_model, df, 'general', general_assign)
    print('general topic assign finished')

    # get the specific topics
    specific_assign = read_s3('news_topics', specific_assign_filename)
    df_specific = predict(specific_model, df, 'specific', specific_assign)
    print('specific topic assign finished')

    # get the sentiment topics
    df_sentiment = calculate_sentiment(df)
    print('sentiment score finished')

    # merge the result into output
    merge_topic_sentiment(df_general, df_specific, df_sentiment)
    print('merging data frame finished')

    # write the output to s3
    write_s3('model_output_data', output)
    print('uploading the output to s3 finished')
