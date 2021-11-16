import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

bearerToken = os.environ['TWITTER_BEARER_TOKEN']

#magic begin
def bearerOAuth(r):
    r.headers["Authorization"] = f'Bearer {bearerToken}'
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r

def connectToEndpoint(url):
    response = requests.request('GET', url, auth=bearerOAuth)
    if response.status_code != 200:
        raise Exception('request returned an error: {} {}'.format(response.status_code, response.text))
    return response.json()
#magic end

#returns the amount of tweets containing "keyword" from the past week
def tweetCount(keyword) -> int:
    url = 'https://api.twitter.com/2/tweets/counts/recent?query={}'.format(keyword)
    tweets = connectToEndpoint(url)
    return tweets['meta']['total_tweet_count']

#returns the most recent tweet containing "keyword" under parameters that help filter out useless tweets
def recentTweet(keyword) -> str:
    url = 'https://api.twitter.com/2/tweets/search/recent?query={} -is:reply -is:retweet -airdrop -giveaway -follow lang:en&max_results=10&tweet.fields=id'.format(keyword)
    jsonResponse = connectToEndpoint(url)
    latestTweet = jsonResponse['data'][0]
    tweetID = latestTweet['id']
    return 'https://twitter.com/_/status/{}'.format(tweetID)
