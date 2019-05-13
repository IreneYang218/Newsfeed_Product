import datetime

token_file = 'token.csv'

time_delta = -1

today = datetime.datetime.now().date()
delta = datetime.timedelta(days=time_delta)
news_day = today + delta
author_search = 'author_search_from-' + str(news_day) \
              + '_to_'+str(today) + '.csv'
author_twitter_rep = 'author_rep_from-' + str(news_day) \
                   + '_to_'+str(today) + '.csv'
