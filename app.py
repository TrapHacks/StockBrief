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

	date_list = []
	price_list = []

	with open('stock_data/'+symbol+'.csv', 'rb') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
		next(csv_reader, None)

		for row in csv_reader:
			date_list.append(row[5])
			price_list.append(row[6])

	date_list2 = []
	price_list2 = []

	stock = yahoo_finance.Share(symbol)
	stock_data = stock.get_historical('2015-10-01', '2016-01-16')

	for data in stock_data:
		date_list2.append(data['Date'])
		price_list2.append(data['Close'])

	print 'dl==='
	print type(date_list[0])
	print '\n\n'
	print 'pl==='
	print type(price_list[0])
	print '\n\n'

	print 'dl2==='
	print type(date_list2[0])
	print '\n\n'
	print 'pl2==='
	print type(price_list2[0])
	print '\n\n'



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