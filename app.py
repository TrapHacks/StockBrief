#!/usr/bin/env python

from flask import Flask, render_template, jsonify
import csv
import os

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/search", methods=['POST', 'GET'])
def search():
	date_list = []
	price_list = []

	with open('test_data.csv', 'rb') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
		next(csv_reader, None)

		for row in csv_reader:
			date_list.append(row[5])
			price_list.append(row[6])

	return jsonify(dates=date_list, prices=price_list)

@app.errorhandler(404)
def not_found(error):
	return 'This page does not exist', 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))

	if port == 5000:
		app.debug = True

	app.run()