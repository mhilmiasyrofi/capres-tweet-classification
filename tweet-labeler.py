import tweepy
import os
import pickle

from pprint import pprint
from datetime import datetime

clear = lambda: os.system('clear')

def save_result(obj):
    filename = "tweet-data-" + str(int(datetime.now().timestamp())) + '.pkl'
    with open(filename, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

def login():
    print("Logging in...")
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)

def start_screen(username):
    print("Tweet Labeler for NLP assignment")
    print("================================")
    print("You are logged in as {}".format(username))
    print("")
    print("Command: ")
    print("exit   - Exit program.")
    print("search - Start searching and labeling for tweets")

def search_tweets(api):
    def get_tweet_full_text(tweet):
        try:
            return tweet.retweeted_status.full_text
        except AttributeError:
            return tweet.full_text

    def tweet_to_dict(tweet):
        return {
            'id': tweet.id,
            'text': get_tweet_full_text(tweet),
            'aspect': {
                'jokowi': 0,
                'prabowo': 0
            }
        }

    def label_tweet(status):
        tweet = tweet_to_dict(status)
        label_j = input("Jokowi (p/n): ")
        label_p = input("Prabowo(p/n): ")
        if label_j == 'p':
            tweet['aspect']['jokowi'] = 1
        elif label_j == 'n':
            tweet['aspect']['jokowi'] = -1
        if label_p == 'p':
            tweet['aspect']['prabowo'] = 1
        elif label_p == 'n':
            tweet['aspect']['prabowo'] = -1
        return tweet

    n_tweet = int(input("Number of Results: "))
    query = input("Query: ")

    labeled_tweets = []
    for status in tweepy.Cursor(api.search, q=query, tweet_mode='extended').items(n_tweet):
        clear()
        print(get_tweet_full_text(status))
        print()
        action = input("Save? (Y/n): ")
        if action == 'n':
            continue
        tweet = label_tweet(status)
        labeled_tweets.append(tweet)
    return labeled_tweets
        

def main():

    api = login()
    username = api.me().name

    state = 'start'

    while state != 'exit':
        if state == 'start':
            clear()
            start_screen(username)
            state = input(">>> ")

        elif state == 'search':
            result = search_tweets(api)
            pprint(result)
            action = input("\nSave result as pickle file? (Y/n):")
            if action == 'n':
                state = 'start'
                continue
            save_result(result)
            state = 'start'

        

if __name__ == "__main__":
    main()