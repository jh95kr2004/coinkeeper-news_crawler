#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import json
from mysql.connector import connection

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
	    "safeSearch": "Strict",
		"count": 100,
	    # "sortBy": "Date",
	    # "since": int(time.time())
	}

response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

cnx = connection.MySQLConnection(user="coinkeeper", password="coinkeeper",
		host="coinkeeper.cyafa3gjnbdg.ap-northeast-2.rds.amazonaws.com",
		database="article_db")
cursor = cnx.cursor()

cursor.execute("TRUNCATE article")

for article in search_results["value"] :
	add_article = ("INSERT INTO article "
			"(name, url, image_url, description, provider, datePublished) "
			"VALUES (%(name)s, %(url)s, %(image_url)s, %(description)s, %(provider)s, %(datePublished)s)")
	
	image_url = None
	if "image" in article :
		if "thumbnail" in article["image"] :
			image_url = article["image"]["thumbnail"]["contentUrl"]
	
	data_article = {
		"name": article["name"],
		"url": article["url"],
		"image_url": image_url,
		"description": article["description"],
		"provider": article["provider"][0]["name"],
		"datePublished": article["datePublished"]
		}

	cursor.execute(add_article, data_article)

cnx.commit()
cursor.close()
cnx.close()

print("News is updated: %d" %(time.time()))
