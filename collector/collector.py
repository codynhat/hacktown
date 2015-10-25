import twitter
import json
import StringIO
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
    term = "adele"
    numberofqueries = 2
    if len(sys.argv) > 1:
        term = sys.argv[1]
        if len(sys.argv) == 3:
            numberofqueries = int(sys.argv[2])

    valueswecareabout = []
    query = getTweets(api, term, 0)
    lastid = logTweets(query, valueswecareabout)

    for i in range(numberofqueries - 1):
        if lastid == -1:
            break
        query = getTweets(api, term, lastid - 1)
        lastid = logTweets(query, valueswecareabout)
    
    possentiment = 0
    negsentiment = 0
    sentcount = 0
    goodlocs=0
    locations = []
    locations_needed = []
    for tweet in valueswecareabout:
        score = getSentiment(tweet[0])
        if score > 0.01:
            possentiment += score
            sentcount += 1
        elif score < -0.01:
            negsentiment += score
            sentcount += 1

        lat = None
        lng = None
        if tweet[2] != None:
            lat = tweet[2]["coordinates"][0]
            lng = tweet[2]["coordinates"][1]
        if lat == None or lng == None:
            if len(tweet[1]) > 0:
                #print tweet[1].encode('utf-8')
                locations.append(tweet[1])
                locations_needed.append((tweet[5],score))
            continue
        # print score
        goodlocs+=1
        es.index(index="index", doc_type=term, body={
                 "lat": lat, "lng": lng, "score": score,"name":tweet[6],"text":tweet[0]}, id=tweet[5])

    c = 0
    while(c < len(locations)):
        latLngs = getLatLng(locations[c:c+100])
        for a in range(len(latLngs)):
            latLng = latLngs[a]
            tweet = locations_needed[c+a]
            if latLng == None:
                es.index(index="index", doc_type="bad", body={"location":valueswecareabout[c+a][1]})
                continue
            goodlocs+=1
            lat = latLng["lat"]
            lng = latLng["lng"]
            score = tweet[1]
            print tweet[0]
            es.index(index="index", doc_type=term, body={
                   "lat": lat, "lng": lng, "score": score, "name":valueswecareabout[c+a][6],"text":valueswecareabout[c+a][0]}, id=tweet[0])
        c += 100

    print len(valueswecareabout), goodlocs, sentcount, possentiment, negsentiment


def getTweets(api, searchterm, last_id):
    if last_id:
        query = api.GetSearch(term=searchterm, count=100,
                              lang="en", max_id=last_id)
    else:
        query = api.GetSearch(term=searchterm, count=100, lang="en")
    return query


def logTweets(query, valueswecareabout):
    if len(query) == 0:
        return -1
    for status in query:
        valueswecareabout.append(
            (status.text, status.user.location, status.coordinates, status.geo, status.place, status.id, status.user.name))
    return query[-1].id


def getSentiment(tweet):
    value = TextBlob(tweet)
    return value.sentiment.polarity


def getLatLng(locations):
    if len(locations) == 0:
        return None
    payload = []
    for location in locations:
        payload.append(('location',location))
    r = requests.get('http://www.mapquestapi.com/geocoding/v1/batch?', data={
        'key': 'Ch0PhK6sUaGxQJRlogATGflCMRTgVQAq',
        'inFormat': 'json',
        'outFormat': 'json',
        'maxResults': 1,
        'thumbMaps': 'false',
    }, params=payload)
    print dir(r)
    print r.url
    re = r.json()
    coordinates = []
    for coord in re["results"]:
        if coord['locations'][0]["geocodeQuality"] != "COUNTRY":
            latLng = coord['locations'][0]['latLng']
            coordinates.append(latLng)
        else:
            coordinates.append(None)
            
    print(len(coordinates))
    return coordinates

if __name__ == '__main__':
    main()
