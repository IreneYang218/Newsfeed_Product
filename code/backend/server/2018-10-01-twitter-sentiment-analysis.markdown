---
title: "4 Steps to Implement Twitter Sentiment Analysis"
layout: post
date: 2018-10-01 22:10
tag: NLP
image: false
headerImage: true
projects: true
hidden: true # don't count this post in blog pagination
description: "Yixin Sun's project"
category: project
author: Yixin Sun
externalLink: false
---

This is an individual project of my master course [_data acquisition_](https://github.com/parrt/msds692) taught by Terence Parr at University of San Francisco. Due to course policies, I will not publicate my code. If you are interested in the implementation, feel free to contact me!   


# Results Display
With my server running in AWS, in response to URL `/user_id`, the script will   
1. __retrieve__ the lastest 100 tweets of this user,    
2. __calcualte and display__ one's median sentiment score (based on the 100 tweets),   
3. and __calcualte and display__ the sentiment of each tweet using a color spectrum.



### Demo   
Display sentiment analysis for user
`realDonaldTrump`    ![Screenshot](https://yixinsun.github.io/assets/images/twitter-sentiment-analysis.png)
    
user `msfca_msds`:  
![Screenshot](https://yixinsun.github.io/assets/images/usfca-msds.png)


# Pre-requisites
* your Twitter API Keys and Access Tokens [(reigster here)](https://developer.twitter.com/en/apps)
* python library flask (for your own web server)
* python library [vaderSentiment](https://github.com/cjhutto/vaderSentiment) (a handy sentiment analysis tool)
* python library tweepy
* template engine [jinja2](http://jinja.pocoo.org/docs/2.9/), which is built-in with flask, but you need to know how to render a template

# Steps 
### 1. Authenticating with the twitter API server
Register a Twitter API App. With your `consumer_key`, `consumer_secret`, `access_token`, `access_token_secret`, create and return an API object.

example: 

    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)  
  

### 2. Mining for tweets
Given a tweepy API object and the screen name of the Twitter user, create a list of tweets where each tweet is a dictionary with the following keys:  

	id: tweet ID
	created: tweet creation date
	retweeted: number of retweets
	text: text of the tweet
	hashtags: list of hashtags mentioned in the tweet
	urls: list of URLs mentioned in the tweet
	mentions: list of screen names mentioned in the tweet
	score: the "compound" polarity score from vader's polarity_scores()
	
	
Return a dictionary containing keys-value pairs:

	user: user's screen name
	count: number of tweets
	tweets: list of tweets, each tweet is a dictionary
	
For efficiency, create a single Vader SentimentIntensityAnalyzer() per call to this function, not per tweet. 


### 3. Add colors
Given a list of tweets, one dictionary per tweet, add
a "color" key to each tweets dictionary with a value
containing a color graded from red to green. Pure red
would be for -1.0 sentiment score and pure green would be for
sentiment score 1.0.


Use `colour.Color` to get 100 color values in the range
from red to green. Then convert the sentiment score from -1..1
to an index from 0..100. That index gives you the color increment from the 100 gradients.


This function modifies the dictionary of each tweet. It lives in the server script because it has to do with display not collecting.

### 4. Set up a server 
Using `flask` and your prepared HTML template, set up a server that responds with one pages, showing the most recent 100 tweets for given user.  

example: 

	app = Flask(__name__)
	@app.route("/<name>")
	def tweets(name):  
	    ...
	    return flask.render_template('your_template.html', ...)

Please keep in mind the limits imposed by the twitter API:
https://dev.twitter.com/rest/public/rate-limits

