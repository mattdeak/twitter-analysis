# -*- coding: utf-8 -*-
"""
A module to scrape tweets from twitter via the search
@author Matthew Deakos
@version 0.3
"""
import os
from os import environ
import pymongo
import tweepy
from tweepy import OAuthHandler
from datetime import datetime
from pprint import pprint

def modify_json(json, query):
    """Adds a query entry to json"""
    json['query'] = query
    json['_id'] = json['id']
    json.pop('id')
    return json


def download_tweets(query, collection, max_tweets=100000, tweets_per_query=100):
    """Downloads tweets via the search api and imports it into a mongo collection"""
    # Get authorization
    auth = OAuthHandler(environ['CONSUMER_KEY'], environ['CONSUMER_SECRET'])
    auth.set_access_token(environ['ACCESS_TOKEN'], environ['ACCESS_SECRET'])
    api = tweepy.API(auth)

    max_id = -1
    tweet_count = 0
    print ("Download max {0} tweets".format(max_tweets))
    while tweet_count < max_tweets:
        try:
            if (max_id <= 0):
                new_tweets = api.search(q=query, count=tweets_per_query)

            else:
                new_tweets = api.search(q=query, count=tweets_per_query,
                max_id = str(max_id - 1))

            if not new_tweets:
                print("No more tweets found")
                break

            try:
                result = collection.insert_many([modify_json(tweet._json, query) for tweet in new_tweets], ordered=False)
            except Exception as e:
                print (e)

            tweet_count += len(new_tweets)
            max_id = new_tweets[-1].id
            print("Downloaded {} tweets".format(tweet_count))
        except tweepy.TweepError as e:
            print("Error: " + str(e))
            break
