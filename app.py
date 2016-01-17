#!/usr/bin/env python

from flask import Flask, render_template
import csv
import os

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/")
def fake_data():
	with open('stock_data/MMM.csv', 'rb') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',', quitechar='|')
	return "fuck off"

@app.errorhandler(404)
def not_found(error):
	return 'This page does not exist', 404

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))

	if port == 5000:
		app.debug = True

	app.run()