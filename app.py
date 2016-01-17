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
	symbol = request.get_data()[11:]

	print symbol

	date_list = []
	price_list = []

	stock = yahoo_finance.Share(symbol)
	stock_data = stock.get_historical('2015-10-01', '2016-01-16')
	print stock_data
	for data in stock_data:
		date_list.append(data['Date'])
		price_list.append(data['Close'])

	return jsonify(dates=date_list, prices=price_list)

@app.route("/nytimes", methods=['POST'])
def nytimes():
	query = '3M Co'

	search_obj = nytimes.get_article_search_obj(nytimes_api_key)
	response = search.articles_search(q=query, sort='newest', fl='headline,pub_date,lead_paragraph,web_url')

	json = 'invalid return'
	try:
		json = response['response']['docs']
	except Exception, e:
		raise e

	return json

@app.errorhandler(404)
def not_found(error):
	return 'This page does not exist', 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))

	if port == 5000:
		app.debug = True

	app.run()