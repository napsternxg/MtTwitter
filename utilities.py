import json
from tqdm import tqdm

import re

import time


URL_DOMAIN=re.compile(r'.*://([^/]+?)(/.*)?$')
def get_url_domain(url):
    m = URL_DOMAIN.match(url)
    return m.groups()[0]    

def extract_user_data(user_json):
    user_data = json.loads(user_json)
    return user_data['screen_name'], user_data['description']

def extract_hashtags(tweet_data):
    hashtags = ()
    if tweet_data["entities"]["hashtags"]:
        hashtags = tuple(map(lambda x: x["text"], tweet_data["entities"]["hashtags"]))
    return hashtags

def extract_mentions(tweet_data):
    mentions = ()
    if tweet_data["entities"]["user_mentions"]:
        mentions = tuple(map(lambda x: x["screen_name"], tweet_data["entities"]["user_mentions"]))
    return mentions

def extract_url_domains(tweet_data):
    url_domains = ()
    if tweet_data["entities"]["urls"]:
        url_domains = tuple(map(lambda x: get_url_domain(x["expanded_url"]), tweet_data["entities"]["urls"]))
    return url_domains
    
def extract_time(x):
    ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(x,'%a %b %d %H:%M:%S +0000 %Y'))
    return ts

def make_tweet_data_extractor(extractor_funcs):
    def extract_data(json_str):
        json_data = json.loads(json_str)
        extracted_features = tuple(func(json_data) for func in extractor_funcs)
        return extracted_features
    return extract_data    


