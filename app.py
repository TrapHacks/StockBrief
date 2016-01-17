#!/usr/bin/env python

from flask import Flask, render_template, jsonify, request
import csv
import os
import nytimes
import yahoo_finance

app = Flask(__name__)

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

@app.errorhandler(404)
def not_found(error):
	return 'This page does not exist', 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))

	if port == 5000:
		app.debug = True

	app.run()