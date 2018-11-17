import tweepy
import os
import pickle

from classifier import predict_jokowi, predict_prabowo
from time import sleep

clear = lambda: os.system('clear');

def login():
    print("Logging in...")
    consumer_key = "V80gpONO6afT0WTD6jJmL0JJE"
    consumer_secret = "ITvvYILOOqYN9Pr5iROCl7Iz1PvLBEYr2vYwuyVQjCgyPIwnCK"
    access_token = "98342662-cPlvAxAfJopG09yVXO7UYMX1uhKWJj5KlcHwiveT4"
    access_token_secret = "GJzJr4JlxcljxsjcFRn7tm1ZvYUkWv59GZQiSGqMDAdLq"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def start_screen(username):
    print("Pemilu RI 2019 Real Time Tweet Monitoring")
    print("=========================================")
    print("You are logged in as {}".format(username))
    print("")
    print("Command: ")
    print("exit   - Exit program.")
    print("start - Start monitoring.")


def print_header(jokowi, prabowo):
    print("Pemilu RI 2019 Real Time Tweet Monitoring")
    print("=========================================")
    print("Jokowi:  {}".format(jokowi))
    print("Prabowo: {}".format(prabowo))
    print("")
    print("Tweet:")


def search_tweets(api, jokowi, prabowo):
    def get_tweet_full_text(tweet):
        try:
            return tweet.retweeted_status.full_text
        except AttributeError:
            return tweet.full_text

    n_tweet = int(input("Number of Results: "))
    query = input("Query: ")
    sentiment_jokowi = jokowi
    sentiment_prabowo = prabowo
    for status in tweepy.Cursor(api.search, q=query, tweet_mode='extended').items(n_tweet):
        text = get_tweet_full_text(status)
        sentiment_jokowi += predict_jokowi(text)
        sentiment_prabowo += predict_prabowo(text)
        clear()
        print_header(sentiment_jokowi, sentiment_prabowo)
        print(text)
        print()
        sleep(4)
    return sentiment_jokowi, sentiment_prabowo


def main():

    api = login()
    username = api.me().name

    state = 'begin'
    jokowi = 0
    prabowo = 0

    while state != 'exit':
        if state == 'begin':
            clear()
            start_screen(username)
            state = input(">>> ")

        elif state == 'start':
            sentiments = search_tweets(api, jokowi, prabowo)
            jokowi += sentiments[0]
            prabowo += sentiments[1]
            state = 'begin'
        
        else:
            state = input(">>> ")
        

if __name__ == "__main__":
    main()