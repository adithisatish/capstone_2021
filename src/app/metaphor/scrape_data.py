from bs4 import BeautifulSoup
import requests
import json

r = requests.get('https://metaphor.wiki/api/home')
data = r.json()['body']['serverData'][1]['Value']
metaphors = []

for i in data:
    metaphors.append(i['Description'])

print(metaphors)
print(len(metaphors))
