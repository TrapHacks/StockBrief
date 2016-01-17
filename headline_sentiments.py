import nytimes
from textblob import TextBlob
def nytimes_sentiment(query):
	search = nytimes.get_article_search_obj('2f5b350f0e83494221d16b3671f89af9:5:74041247')
	result = search.article_search(q=query, sort='newest', fl='headline,pub_date,lead_paragraph,web_url')

	articles = result['response']['docs']
	headlines = []
	pos_headlines = 0
	neg_headlines = 0
	for article in articles:
		headline = article['headline']['main']
		headlines.append(headline)

	for headline in headlines:
		blob = TextBlob(headline)
		if blob.sentiment.polarity > 0:
			pos_headlines += 1
		else:
			neg_headlines += 1

	

	if pos_headlines > 5: 
		return 'Positive'
	else:
		return 'Negative' 