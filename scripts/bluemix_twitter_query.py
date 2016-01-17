import json
import sys
import requests
import csv 
import time
names = []

with open('constituents.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        names.append(row[1])

names = names[1:]

with open('../data/login.properties', 'r') as login_file:
    login_info = login_file.readlines()

username = login_info[0].replace('\n', '')
password = login_info[1].replace('\n', '')


for i in range(0, len(names)):
    company_name = names[i]
    extra_stuff = '?q=' + company_name + '&size=500'
    url = 'http://cdeservice.mybluemix.net/api/v1/messages/search' + extra_stuff
    content = requests.get(url, auth=(username, password)).json()
    company_name = company_name.replace(' ', '_')
    
    with open('../data/' + company_name + '.json', 'w') as output:
        json.dump(content, output)

    time.sleep(0.2)

