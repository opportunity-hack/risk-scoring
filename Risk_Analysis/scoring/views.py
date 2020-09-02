from django.shortcuts import render
from pymongo import MongoClient
from authentication.views.encrypt_access import *
import json
from tweepy import OAuthHandler, API, Cursor
from requests_oauthlib import OAuth2Session
from scoring.preprocess import preprocess


# Create your views here.

def fetch_access_tokens():
    key = load_key()
    #Connect to MongoDB to retrive access_token
    try:
        conn = MongoClient()
        print("Connected successfully!!!")
        db = conn.database
        # Created or Switched to collection names: tokens
        collection = db.tokens
        print('connected to collection')
        record = collection.find_one()
        print('fetched record')
        collection.delete_one(record)
        print('record deleted')
        access_tokens = json.loads(decrypt(record['access_token'], key).decode('utf-8'))
        if 'twitter_access_token' in access_tokens and access_tokens['twitter_access_token'] and access_tokens['twitter_access_token_secret']:
            print('here')
            fetch_twitter_data(access_tokens['twitter_access_token'], access_tokens['twitter_access_token_secret'])
        print('After twitter')
        if 'facebook_access_token' in access_tokens and access_tokens['facebook_access_token']:
            fetch_facebook_data(access_tokens['facebook_access_token'])
        conn.close()
    except:
        print("Could not connect to MongoDB")


def fetch_twitter_data(access_token, access_token_secret):

    with open('authentication/credentials.json') as f:
        credentials = json.load(f)

    consumer_key = credentials['twitter_consumer_key']
    consumer_secret = credentials['twitter_consumer_secret']

    callback = 'http://127.0.0.1:8000/authentication/twitter/callback'
    print('in fetch twitter data')
    oauth = OAuthHandler(consumer_key, consumer_secret, callback)
    oauth.set_access_token(access_token, access_token_secret)
    api = API(oauth)
    statuses = []
    for status in Cursor(api.user_timeline).items():
        statuses.append(preprocess(status.text))
    print(statuses)
    # preprocess(statuses)


def fetch_facebook_data(access_token):

    # Json file that contains the user credentials to access Facebook API
    with open('authentication/credentials.json') as f:
        credentials = json.load(f)

    client_id = credentials['facebook_client_id']

    oauth = OAuth2Session(client_id, token=access_token)
    user_posts = oauth.get('https://graph.facebook.com/me/posts')
    user_posts_json = json.loads(user_posts.content.decode('utf-8'))['data']
    posts = []
    for i, x in enumerate(user_posts_json):
        if i > 3:
            break
        if 'message' in x:
            posts.append(preprocess(x['message']))
    # preprocess(posts)
    print(posts)