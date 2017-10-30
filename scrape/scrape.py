# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import tweepy
import jsonpickle
import csv
from tweepy import OAuthHandler

def read_certs():
    certs = {}
    with open('certs.txt','r') as cert_file:
        for line in cert_file:
            (key, val) = line.split(': ')
            certs[key] = val.replace('\n','')
    return certs
            
def download_tweets(api, query, max_tweets=100000, fname='tweets.txt'):
    """Searches tweets and dumps the json into a text file"""
    since_id = None
    
    max_id = -1
    tweet_count = 0
    print ("Download max {0} tweets".format(max_tweets))
    with open(fname, 'w') as f:
        while tweet_count < max_tweets:
            try:
                if (max_id <= 0):
                    if (not since_id):
                        new_tweets = api.search(q=query, count=100)
                    else:
                        new_tweets = api.search(q=query, count=100, since_id=since_id)
                else:
                    if (not since_id):
                        new_tweets = api.search(q=query, count=100, max_id = str(max_id - 1))
                        
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
                        '\n')
                
                tweet_count += len(new_tweets)
                print("Downloaded {} tweets".format(tweet_count))
            except tweepy.TweepError as e:
                print("Error: " + str(e))
                break
            
def tweets_to_csv(infile, outfile):
    f = open(infile, 'r')
    tweet_data = []
    for line in f:
        tweet_data.append(jsonpickle.decode(line))
    
    f.close()
    
    csv_file = open(outfile, 'w', encoding='utf-8', newline='')
    writer = csv.writer(csv_file)
    for tweet in tweet_data:
        line = [tweet['id'],tweet['user']['screen_name'], tweet['user']['followers_count'], tweet['user']['favourites_count'],
            tweet['user']['statuses_count'],tweet['text'],tweet['favorite_count'],tweet['retweet_count']]
        
        writer.writerow(line)
    csv_file.close()
                    
def main():
    certs = read_certs()
    
    auth = OAuthHandler(certs['consumer_key'], certs['consumer_secret'])
    auth.set_access_token(certs['access_token'], certs['access_secret'])
    
    api = tweepy.API(auth)
    
    #download_tweets(api, query='iWatch', max_tweets=5000, fname='sweep1.txt')
    
    print ("Generating CSV...")
    tweets_to_csv('sweep1.txt', 'sweep1.csv')
    print ("Done")
    
    
                    
if __name__ == '__main__':
    main()