import datetime


time_delta = -1
today = datetime.datetime.now().date()
delta = datetime.timedelta(days=time_delta)
news_day = today + delta
output = 'news_output_from_'+str(news_day)+'_to_'+str(today)+'.csv'
general_model = 'lda_mallet_4_april.model'
specific_model = 'lda_mallet_100_april.model'
general_assign_filename = 'assign_general_topics.csv'
specific_assign_filename = 'assign_100_topics.csv'
mallet_path = 'mallet-2.0.8/bin/mallet'
