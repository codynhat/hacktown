#import everything
import twitter
import json
import StringIO
from elasticsearch import Elasticsearch
from textblob import TextBlob
import sys
import requests

#make our elasticsearch server
es = Elasticsearch(['http://localhost:9200'])


def main():
    api = twitter.Api(consumer_key = 'cVkMNul8qtA5W6dnWMaqRPMxO',
                consumer_secret = 'lYabB5Lq1FkZwY9S7qoBKaArUsrTDzme5l6WhpYEAYFeEYNfmr',
                access_token_key = '189645598-d85uGGNvjhdFTUL2rfmaIj4IHrRe3N4X2PZOm5AD',
                access_token_secret = 'TS3vqXwkm3wmTdTS1avi6kLzT3mRRDBbFskiBMF6v7LAG')
#    api = twitter.Api(consumer_key='xiRvwM5u5lgLW4GsfMq1BLxmw',
#                      consumer_secret='A7IPWnxsfTfTccnuyF9TXPXEBwpC6WyEVwkNseJXxv4SVqhncd',
#                      access_token_key='1939224967-lZqH7LpKSs775MCNK2ynZlJ0meUIcDt9QiM5KAt',
#                      access_token_secret='bgelSzudLaRrKaQcIHvXOXvNW7QaoNpEiaLmnGAnvYNmt')
    term = "adele" # input parsing
    numberofqueries = 2
    if len(sys.argv) > 1:
        term = sys.argv[1]
        if len(sys.argv) == 3:
            numberofqueries = int(sys.argv[2])

    #initialize values
    valueswecareabout = []
    possentiment = 0
    negsentiment = 0
    sentcount = 0
    goodlocs=0
    locations = []
    locations_needed = []
    i = 0 # iterate through queries
    
    query = getTweets(api, term)
    lastid = logTweets(query, valueswecareabout)

    while i<numberofqueries:
        if lastid == -1:
            break
        
        #insert code
        for (num, tweet) in enumerate(valueswecareabout):
            # score the tweet
            score = getSentiment(tweet[0])
            if score > 0.01:
                possentiment += score
                sentcount += 1
            elif score < -0.01:
                negsentiment += score
                sentcount += 1
            
            lat = None
            lng = None
            if tweet[2] != None: # if coordinates are nonnull
                lat = tweet[2]["coordinates"][0]
                lng = tweet[2]["coordinates"][1]
            if lat == None or lng == None: # if both coordinates exist
                if len(tweet[1]) > 0: # and the location isn't empty
                    locations.append(tweet[1]) # save some values
                    locations_needed.append((tweet[5],score, num))
                continue
            goodlocs+=1
            # add to elasticsearch
            es.index(index="index", doc_type=term, body={
                     "lat": lat, "lng": lng, "score": score,"name":tweet[6],"text":tweet[0]}, id=tweet[5])
        
        # looking through userlocations
        latLngs = getLatLng(locations)
        for a in range(len(latLngs)):
            latLng = latLngs[a]
            tweet = locations_needed[a]
            if latLng == None: # put it in bad location names
                es.index(index="index", doc_type="bad", body={"location":valueswecareabout[tweet[2]][1]},id = tweet[0])
                continue
            goodlocs+=1
            lat = latLng["lat"]
            lng = latLng["lng"]
            score = tweet[1]
            print tweet[0]
            # add the userlocation to the database
            es.index(index="index", doc_type=term, body={
                   "lat": lat, "lng": lng, "score": score, "name":valueswecareabout[tweet[2]][6],"text":valueswecareabout[tweet[2]][0]}, id=tweet[0])
        
        #reset all values
        valueswecareabout = []
        locations_needed=[]
        locations=[]
        query = getTweets(api, term, lastid - 1)
        lastid = logTweets(query, valueswecareabout)
        i += 1

    print goodlocs, sentcount, possentiment, negsentiment


def getTweets(api, searchterm, last_id=None):
    #just get 100 tweets
    if last_id: # we can put in no last_id for the first query
        query = api.GetSearch(term=searchterm, count=100,
                              lang="en", max_id=last_id)
    else:
        query = api.GetSearch(term=searchterm, count=100, lang="en")
    return query


def logTweets(query, valueswecareabout):
    if len(query) == 0:
        return -1 # error code to quit
    for status in query: # iterate through statuses, get a couple immportant values
        valueswecareabout.append(
            (status.text, status.user.location, status.coordinates, status.geo, status.place, status.id, status.user.name))
    return query[-1].id # remember last id


def getSentiment(tweet): #call textblob
    value = TextBlob(tweet)
    return value.sentiment.polarity


def getLatLng(locations):
    if len(locations) == 0:
        return None
    payload = []
    for location in locations: # make the list of json values
        payload.append(('location',location))
        
    # call the api
    r = requests.get('http://www.mapquestapi.com/geocoding/v1/batch?', data={
        'key': 'Ch0PhK6sUaGxQJRlogATGflCMRTgVQAq',
        'inFormat': 'json',
        'outFormat': 'json',
        'maxResults': 1,
        'thumbMaps': 'false',
    }, params=payload)
    re = r.json()
    coordinates = []
    for coord in re["results"]:
        if coord['locations'][0]["geocodeQuality"] != "COUNTRY":
            latLng = coord['locations'][0]['latLng']
            coordinates.append(latLng)
        else:
            coordinates.append(None) # for index preserving
            
    return coordinates

if __name__ == '__main__':
    main()
