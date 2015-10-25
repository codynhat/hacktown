import twitter, json, StringIO
from elasticsearch import Elasticsearch
from textblob import TextBlob
import sys
import requests

es = Elasticsearch()

def main():
    api = twitter.Api(consumer_key='xiRvwM5u5lgLW4GsfMq1BLxmw',
                      consumer_secret='A7IPWnxsfTfTccnuyF9TXPXEBwpC6WyEVwkNseJXxv4SVqhncd',
                      access_token_key='1939224967-lZqH7LpKSs775MCNK2ynZlJ0meUIcDt9QiM5KAt',
                      access_token_secret='bgelSzudLaRrKaQcIHvXOXvNW7QaoNpEiaLmnGAnvYNmt')
    term = "adele"
    numberofqueries = 2
    if len(sys.argv)>1:
        term = sys.argv[1]
        if len(sys.argv)==3:
            numberofqueries = int(sys.argv[2])
        
    geo  = ("38.5000","-98.0000","3000km")
    valueswecareabout = []
    query = getTweets(api, term, geo,0)
    lastid=logTweets(query, valueswecareabout)

    for i in range(numberofqueries-1):
        query = getTweets(api, term, geo, lastid-1)
        lastid = logTweets(query, valueswecareabout)
            
    i = 0
    totalsentiment = 0
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
        totalsentiment += score
        print score
        es.index(index="index", doc_type=term, body={"lat": lat, "lng": lng, "score": score}, id=i)
        i += 1
    print totalsentiment

def getTweets(api, searchterm, geo, last_id):
    if last_id:
        query = api.GetSearch(term = searchterm, count = 100, geocode = geo, max_id = last_id)
    else:
        query = api.GetSearch(term = searchterm, count = 100, geocode = geo)
    return query
    
def logTweets(query, valueswecareabout):
    for status in query:
        valueswecareabout.append((status.text, status.user.location, status.coordinates, status.geo, status.place))
    return query[-1].id

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
    latLng = re['results'][0]['locations'][0]['latLng']
    return latLng

if __name__ == '__main__':
    main()
