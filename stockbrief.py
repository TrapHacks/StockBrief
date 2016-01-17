#!/usr/bin/env python

from flask import Flask, render_template, jsonify, request
from headline_sentiments import nytimes_sentiment
from scripts.twitter_search import tweet_query
from microsoft_request import azure_req
import csv
import os
import nytimes
import yahoo_finance
import time

app = Flask(__name__)

if 'DYNO' in os.environ:
    keys = os.environ['NY_TIMES_KEY']
else:
    keys = open('login.properties', 'rb')
    nytimes_api_key = keys.readline().strip()

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/search", methods=['POST'])
def search():
	symbol = request.get_data()
	print symbol

	date_list2 = []
	price_list2 = []

	stock = yahoo_finance.Share(symbol)
	stock_data = stock.get_historical('2015-10-01', '2016-01-16')

	for data in stock_data:
		date_list2.append(data['Date'])
		price_list2.append(data['Close'])

	date_list2.reverse()
	price_list2.reverse()

	return jsonify(dates=date_list2, prices=price_list2)

@app.route("/nytimes", methods=['POST'])
def nytimes_articles():
	query = request.get_data()

	search_obj = nytimes.get_article_search_obj(nytimes_api_key)
	result = search_obj.article_search(q=query, sort="newest", fl="headline,pub_date,lead_paragraph,web_url")

	try:
		docs = result['response']['docs']
		for doc in docs:
			print jsonify(doc)
	except Exception, e:
		raise e

	return jsonify(docs=docs)

@app.route('/prediction', methods=['POST'])
def prediction():
	symbol = request.get_data()
	print symbol
	date = time.strftime('%Y-%m-%d')
	stock = yahoo_finance.Share(symbol)
	opening_price = stock.get_open()

	twitter_sentiment = tweet_query(symbol)
	headline_sentiment = nytimes_sentiment(symbol)
	overall_sentiment_num = twitter_sentiment[0] + headline_sentiment[0]
	overall_sentiment = 'Positive' if overall_sentiment_num > 505 else 'Negative'
	azure_sentiment = azure_req(date, symbol, overall_sentiment, opening_price)
	
	results = azure_sentiment['Results']['output1']['value']['Values'][0]
	closing_price = results[5]
	json_result = {
		'success': True,
		'opening_price' : opening_price,
		'closing_price' : closing_price
	}

	return jsonify(json_result)

@app.route('/tweet', methods=['POST'])
def tweets():
	symbol = request.get_data()
	twitter_sentiment = tweet_query(symbol)
	json_result = {
		'success' : True,
		'sentiment' : twitter_sentiment[2]
	}

	return jsonify(json_result)


@app.errorhandler(404)
def not_found(error):
	return 'This page does not exist', 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))

	# if port == 5000:
	app.debug = True

	app.run()
