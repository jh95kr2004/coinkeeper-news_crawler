import requests
import time

subscription_key = "1b44b3da8fd5411bbf8e8dc5c0018d47"
search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
search_term = "비트코인"

headers = {"Ocp-Apim-Subscription-Key" : subscription_key}
params  = {"q": search_term,
           "textDecorations": False,
           "safeSearch": "Strict",
           "sortBy": "Date",
           "since": int(time.time())}

response = requests.get(search_url, headers=headers, params=params)
response.raise_for_status()
search_results = response.json()

print(search_results["totalEstimatedMatches"])

for article in search_results["value"] :
    print(article["name"])
    print(article["description"])
    print(article["url"])
    if "image" in article :
        print(article["image"])
    print(article["datePublished"])
    print()
