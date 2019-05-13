import datetime


token = '48d3f6a0-4b6d-4c42-9221-71f15b7694aa'
site_lists = ['wsj.com', 'latimes.com', 'newsday.com'
              'cnn.com', 'bloomberg.com', 'espn.com',
              'aljazeera.com',
              'pitchfork.com', 'bbc.com', 'npr.org', 'pbs.org', 'cnbc.com',
              'msnbc.com', 'economist.com', 'tmz.com', 'forbes.com',
              'politico.com', 'slate.com', 'salon.com',
              'huffingtonpost.com',
              'propublica.org', 'nbcnews.com',
              'businessinsider.com',
              'thedailybeast.com', 'foreignpolicy.com',
              'bleacherreport.com',
              'mtv.com', 'rollingstone.com',
              'theverge.com', 'cbssports.com']

time_delta = -1

today = datetime.datetime.now().date()
delta = datetime.timedelta(days=time_delta)
news_day = today + delta
news_folder = 'news_articles'
news_filename = 'news_from_'+str(news_day)+'_to_'+str(today)+'.csv'
