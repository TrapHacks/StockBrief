import urllib2
import json 

def azure_req(date, symbol, sentiment, opening_price):

    data =  {

            "Inputs": {

                    "input1":
                    {
                        "ColumnNames": ["Date", "Sentiment", "Company Symbol", "Opening Price"],
                        "Values": [ [ date, sentiment, symbol, str(opening_price) ], [ "", "value", "value", "0" ], ]
                        
        
                    }, 
            },
            "GlobalParameters": {
            }
    }
    

    body = str.encode(json.dumps(data))

    url = 'https://ussouthcentral.services.azureml.net/workspaces/b6ac40870fe442feacc50a8ad7d58844/services/edd94a9153d44e71ba85f660e73d70ac/execute?api-version=2.0&details=true'
    api_key = 'mJhdmrK0B9jLIhQsQOgOetDBdIvsoTFrCbPMfMPIipH2AmFgdno8IhgV0TIFZTvTrdpOrH6oAEcuvXcl3iHmWQ=='
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib2.Request(url, body, headers) 

    try:
        response = urllib2.urlopen(req)

        # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
        # req = urllib.request.Request(url, body, headers) 
        # response = urllib.request.urlopen(req)

        result = json.loads(response.read())

        return result
    except urllib2.HTTPError, error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())

        print(json.loads(error.read()))                 


