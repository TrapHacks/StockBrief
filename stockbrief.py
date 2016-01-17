#!/usr/bin/env python

from flask import Flask, render_template, jsonify, request, send_from_directory
from headline_sentiments import nytimes_sentiment
from scripts.twitter_search import tweet_query
from microsoft_request import azure_req
import csv
import os
import nytimes
import yahoo_finance
import time

app = Flask(__name__)

symbol_map = {}

if 'DYNO' in os.environ:
    keys = os.environ['NY_TIMES_KEY']
else:
    keys = open('login.properties', 'rb')
    nytimes_api_key = keys.readline().strip()

@app.route("/")
def index():
    return 'hello'
    #	return render_template('index.html')

@app.route("/search", methods=['POST'])
def search():
	symbol = request.get_data()

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

	if symbol_map.has_key(query):
		query = query + ' ' + symbol_map[query]

	print query

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
	date = time.strftime('%Y-%m-%d')
	stock = yahoo_finance.Share(symbol)
	opening_price = stock.get_open()
	closing_price = 0.0
	twitter_sentiment = tweet_query(symbol)
	headline_sentiment = nytimes_sentiment(symbol)
	overall_sentiment_num = twitter_sentiment[0] + headline_sentiment[0]
	overall_sentiment = 'Positive' if overall_sentiment_num > 505 else 'Negative'
	pos_azure_sentiment = azure_req(date, symbol, 'Positive', float(opening_price) * 1.05)
	neg_azure_sentiment = azure_req(date, symbol, 'Negative', float(opening_price) * .95)

	pos_val = float(pos_azure_sentiment['Results']['output1']['value']['Values'][0][4])
	neg_val = float(neg_azure_sentiment['Results']['output1']['value']['Values'][0][4])
	print pos_val, neg_val
	midpoint = abs((pos_val + neg_val) / 2)
	if overall_sentiment == 'Positive':
		closing_price +=  float(opening_price) + (((pos_val - midpoint) / midpoint) * float(opening_price))
	else:
		closing_price +=  float(opening_price) - (((midpoint - neg_val) / midpoint) * float(opening_price))

	difference = closing_price - float(opening_price)
	percent_diff = (difference / float(opening_price)) * 100 
	json_result = {
		'success': True,
		'opening_price' : opening_price,
		'closing_price': closing_price,
		'difference': str(percent_diff),
		'sentiment': overall_sentiment
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

@app.route('/favicon.png')
def favicon():
	return send_from_directory(os.path.join(app.root_path,'static'),
		'favicon.png', mimetype='image/x-icon')
'''
if __name__ == '__main__':
	with open('stocks.csv', 'rb') as readfile:
		reader = csv.reader(readfile)
		for row in reader:
			symbol_map[row[0]] = row[1]

	port = int(os.environ.get('PORT', 5000))

	# if port == 5000:
	app.debug = True

	app.run(host='0.0.0.0', port=port)
'''
