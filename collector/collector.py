import twitter, json, StringIO
from elasticsearch import Elasticsearch
from textblob import TextBlob
import sys
import requests

es = Elasticsearch(['http://107.170.211.113:9200'])

def main():
    api = twitter.Api(consumer_key='xiRvwM5u5lgLW4GsfMq1BLxmw',
                      consumer_secret='A7IPWnxsfTfTccnuyF9TXPXEBwpC6WyEVwkNseJXxv4SVqhncd',
                      access_token_key='1939224967-lZqH7LpKSs775MCNK2ynZlJ0meUIcDt9QiM5KAt',
                      access_token_secret='bgelSzudLaRrKaQcIHvXOXvNW7QaoNpEiaLmnGAnvYNmt')
    valueswecareabout = []
    query = getTweets(api, "adele")
    for status in query:
        valueswecareabout.append(
            (status.text, status.user.location, status.coordinates, status.geo, status.place))
    i = 0
    for tweet in valueswecareabout:
        lat = None
        lng = None
        if tweet[2] != None:
          lat = tweet[2]["coordinates"][0]
          lng = tweet[2]["coordinates"][1]
        if lat == None or lng == None:
            latLng = getLatLng(tweet[1])
            if latLng == None:
              i += 1
              continue
            lat = latLng["lat"]
            lng = latLng["lng"]
        score = getSentiment(tweet[0])
        es.index(index="index", doc_type="adele", body={"lat": lat, "lng": lng, "score": score}, id=i)
        i += 1

def getTweets(api, searchterm):
    query = api.GetSearch(term = searchterm, count = 100)
    return query
        
def getSentiment(tweet):
    value = TextBlob(tweet)
    return value.sentiment.polarity
        
def getLatLng(location):
    print location
    if len(location) == 0:
        return None
    payload = {'location': location}
    r = requests.get('http://www.mapquestapi.com/geocoding/v1/address?',data={
        'key': '7N1MeC0H0uFcbyzovGkG8SPFu5SdPUjU',
        'inFormat': 'json',
        'outFormat':'json',
        'maxResults': 1,
    },params=payload);

    re = r.json()
    if re['results'][0]['locations'][0]["geocodeQuality"] == "COUNTRY":
      return None
    latLng = re['results'][0]['locations'][0]['latLng']
    return latLng

if __name__ == '__main__':
    main()
