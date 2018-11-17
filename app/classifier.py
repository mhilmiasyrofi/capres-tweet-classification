import csv
import pickle
import numpy as np
from nltk.probability import FreqDist
from preprocessors import clean, tokenize, remove_stopwords

with open('../id.stopwords.02.01.2016.txt', 'r') as file:
    csv = csv.reader(file)
    stopwords = [row for row in csv]

features = pickle.load(open('features.pkl', 'rb'))
jokowi_neutral_model = pickle.load(open('jokowi_neutral_model.pkl', 'rb'))
prabowo_neutral_model = pickle.load(open('prabowo_neutral_model.pkl', 'rb'))
jokowi_sentiment_model = pickle.load(open('jokowi_sentiment_model.pkl', 'rb'))
prabowo_sentiment_model = pickle.load(open('prabowo_sentiment_model.pkl', 'rb'))

def preprocess(tweet):
    tokens = remove_stopwords(tokenize(clean(tweet)), stopwords)
    fdist = FreqDist(tokens)
    return np.array([[fdist[f] for f in features]])

def predict_jokowi(tweet):
    vector = preprocess(tweet)
    is_sentimental = jokowi_neutral_model.predict(vector)
    if is_sentimental:
        sentiment = jokowi_sentiment_model.predict(vector)
        return int(sentiment[0]) # {-1, 1}
    else:
        return 0

def predict_prabowo(tweet):
    vector = preprocess(tweet)
    is_sentimental = prabowo_neutral_model.predict(vector)
    if is_sentimental:
        sentiment = prabowo_sentiment_model.predict(vector)
        return int(sentiment[0]) # {-1, 1}
    else:
        return 0


if __name__ == "__main__":
    print(stopwords[:5])