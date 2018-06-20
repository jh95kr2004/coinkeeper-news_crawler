#!/usr/bin/python

import requests
import time
import json

with open("azure.key", "r") as keyFile :
	data = json.load(keyFile)
	subscription_key = data["azure_key"]
	keyFile.close()

search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
search_term = "비트코인"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params  = {
		"q": search_term,
		"textDecorations": False,
	    "safeSearch": "Strict"
	    # "sortBy": "Date",
	    # "since": int(time.time())
	}

response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

for article in search_results["value"] :
    print(article["name"])
    print(article["description"])
    print(article["url"])
    if "image" in article :
        print(article["image"])
    print(article["datePublished"])
    print()
