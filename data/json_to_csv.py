import os
import json
import sys
import csv
import re


everything = []
test_set = set()
for i in os.listdir(os.getcwd()):
    if i.endswith('.json'):
        with open(i) as json_file:
            data = json.load(json_file)
            if 'tweets' in data:
                tweet_objects = data['tweets']
                for j in range(0, len(tweet_objects)):
                    cur_tweet = {}
                    current_tweet_object = tweet_objects[j]
                    time = current_tweet_object['message']['postedTime']
                    body = current_tweet_object['message']['body']
                    company_name = i 
                    if 'content' not in current_tweet_object['cde']:
                        pass
                    else:
                        sentiment_obj = current_tweet_object['cde']['content']
                        cur_tweet['sentiment'] = sentiment_obj['sentiment']['polarity']
                        cur_tweet['body'] = body
                        cur_tweet['time'] = time
                        cur_tweet['company_name'] = company_name
                        everything.append(cur_tweet)



with open('results.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Date', 'Tweet', 'Sentiment', 'Company Name'])
    for i in range(0, len(everything)):
        cur_tweet = everything[i]
        try:
            writer.writerow([cur_tweet['time'], re.sub(r'[^0-9a-zA-Z -]', '', cur_tweet['body']), cur_tweet['sentiment'], cur_tweet['company_name'][:-5]])
        except:
            pass

