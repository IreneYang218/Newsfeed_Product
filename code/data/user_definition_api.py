import datetime


token = '2fc2173a-abd5-437f-a617-4ebc492b90db'
site_lists = ['cnn.com', 'foxnews.com', 'npr.org', 'nbcnews.com',
              'latimes.com', 'newsday.com', 'seattletimes.com',
              'bostonglobe.com', 'nydailynews.com', 'espn.com',
              'aljazeera.com', 'bbc.com', 'pbs.org', 'cnbc.com',
              'economist.com', 'nationalreview.com', 'businessinsider.com',
              'nbcnews.com', 'propublica.org', 'huffingtonpost.com',
              'salon.com', 'slate.com', 'pitchfork.com', 'usatoday.com',
              'techmeme.com', 'bloomberg.com', 'wsj.com', 'forbes.com',
              'politico.com', 'tmz.com', 'msnbc.com']
time_delta = -1

today = datetime.datetime.now().date()
delta = datetime.timedelta(days=time_delta)
news_day = today + delta
filename = 'news-from-'+str(news_day)+'-to-'+str(today)+'.csv'
