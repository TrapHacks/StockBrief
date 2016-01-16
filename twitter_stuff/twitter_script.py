import json
import sys
import requests

search_queries = ['Bank of America', 'Apple', 'Facebook', 'Workday', 'Amazon', 'GE']
with open('../data/login.properties', 'r') as login_file:
    login_info = login_file.readlines()

username = login_info[0].replace('\n', '')
password = login_info[1].replace('\n', '')
content = requests.get('http://cdeservice.mybluemix.net/api/v1/messages/search?q=Microsoft&size=5', auth=(username, password))

for i in range(0, len(search_queries)):
    company_name = search_queries[i]
    extra_stuff = '?q=' + company_name + '&size=500'
    url = 'http://cdeservice.mybluemix.net/api/v1/messages/search' + extra_stuff
    content = requests.get(url, auth=(username, password))
    company_name = company_name.replace(' ', '_')

    with open('../data/' + company_name + '.json', 'w') as output:
        json.dump(content.json(), output)
