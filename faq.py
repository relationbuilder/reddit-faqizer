#!/usr/bin/env python

import praw
import pickle
import sys

import requests

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

import numpy as np
import nltk
from collections import Counter
from pymongo import MongoClient
from pymongo import errors

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import linear_kernel

from sklearn.cluster import KMeans 
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

import pprint

porter = PorterStemmer()
#snowball = SnowballStemmer('english')
wordnet = WordNetLemmatizer()

corpus = []
BigBagOfWords = []
import argparse

def fetchFromFile(f):

    comments = pickle.load(open(f, 'r'))
    return comments
    pass

def fetchFromUrl(url):
    amy = None
    try:
        amy = r.get_submission(url)
    except (requests.exceptions.MissingSchema):
        print "%s is not a valid schema" % (url)
        sys.exit()
    except (requests.exceptions.ConnectionError):
        print "%s couldn't be connected " % (url)
        sys.exit()
    except (requests.exceptions.InvalidURL):
        print "Invalid URL"
        sys.exit()
    except (requests.exceptions.HTTPError):
        print "Couldn't find %s" % (url)
        sys.exit()

    if amy is None:
        print "Unknown error with URL fetching!"
        sys.exit()

    print "Starting to download all comments for this submission (takes time)"
    amy.replace_more_comments(limit=None, threshold=0)

    comments = []
    for c in amy.comments:
        if c.parent_id.find(amy.id) == -1:
            continue
        if type(c) == praw.objects.MoreComments:
            continue
        a = ' '.join(c.body.splitlines())
        comments.append(a)

    return comments
    pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('-u', metavar='url', type=str, nargs='?', help="URL to fetch comments from")
    parser.add_argument('-f', metavar='f', type=str, nargs='?', help="Pickle File to fetch list of comments from")

    args = parser.parse_args()

    print args

    comments = []
    r  = praw.Reddit(user_agent='example')
    stop = set(stopwords.words('english'))

    if args.f is not None:
        comments = fetchFromFile(args.f)
    elif args.url is not None:
        comments = fetchFromUrl(args.url)

    for c in comments:
        a = ' '.join(c.splitlines())
        tok = word_tokenize(a)
        tok_stopped = []
        stopped = []

        for word in tok:
            if word not in stop:
                tok_stopped.append(word)

        corpus.append(a)



    tfidf = TfidfVectorizer(ngram_range=(2,5), stop_words=stop, ).fit_transform(corpus)

    X = StandardScaler().fit_transform(tfidf.todense())

    km = KMeans(n_clusters=40, init='random', n_init=1, verbose=1)

    km = DBSCAN(eps=.1, min_samples=1)

    km.fit(X)

    res = {}
    for i in range(len(corpus)):
        label = km.labels_[i] 
        if res.has_key(label):
            if corpus[i] not in res[label]:
                res[label].append(corpus[i])
        else:
            res[label] = []
            res[label].append(corpus[i])

    for i in res.keys():
        if len(res[i]) > 1:
            pprint.pprint(res[i])

    
