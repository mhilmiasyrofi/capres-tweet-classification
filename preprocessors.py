import re

def clean(text):
    result = text.lower().encode('ascii', 'replace').decode()
    result = re.sub(r'http(\w|\W)+\s?', '', result)
    result = re.sub('[.?,]', '', result)
    return result

def tokenize(text):
    return text.split()

def remove_stopwords(tokens, stopwords):
    return [token for token in tokens if token not in stopwords]
