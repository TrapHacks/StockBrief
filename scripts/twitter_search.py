import tweepy
import requests
from textblob import TextBlob

with open('twitter_login.properties', 'rb') as login_file:
	login_info = login_file.readlines()
	api_key = login_info[0].replace('\n','')
	api_secret = login_info[1].replace('\n','')
	access_token_key = login_info[2].replace('\n','')
	access_token_secret=login_info[3].replace('\n','')
	
def tweet_query(query):
	auth = tweepy.OAuthHandler(api_key, api_secret)
	api = tweepy.API(auth)
	max_tweets = 1000
	searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
	tweet_bodies = []
	num_pos = 0
	num_neg = 0
	for tweet in searched_tweets:
		tweet_bodies.append(tweet.text)

	for body in tweet_bodies:
		blob = TextBlob(body)
		if blob.sentiment.polarity > 0:
			num_pos +=1
		else:
			num_neg += 1

	overall_sentiment = 'positive' if num_pos > 500 else 'negative'
	return [num_pos, num_neg, overall_sentiment]





