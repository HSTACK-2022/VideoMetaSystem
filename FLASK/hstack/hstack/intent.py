# intent.py
#
# 검색어에서 핵심어와 연관어를 추출합니다.
# 
# uses
# - init() : wiki 모델을 불러옵니다.
# - findWord(word) : word 검색어에서 핵심어와 연관어를 추출합니다.
#
# parameters
# - word : 검색어


import os

from gensim.models import word2vec
from konlpy.tag import Okt

def init():
    global wikiModel

    print("load wiki...")
    wikiPath = os.path.join('.', 'models', 'wiki.model')
    wikiModel=word2vec.Word2Vec.load(wikiPath)
    print("load wiki... success")


def findWord(word):
    # 0. search tags
    availTag = {
        'Adjective',
        'Adverb',
        'Noun',
        'Verb'
    }

    # 1. pos tagging
    okt = Okt()
    wordWithTag = okt.pos(word, norm=True, stem=True)
    print(wordWithTag)

    # 2. extract noun, adj, verb
    searchText = set()
    for word, val in wordWithTag:
        if val in availTag:
            searchText.add(word)
            #searchWiki.append((word, 1.0))

    '''
    # 3. run wiki model : get similar words
    wiki = wikiModel.wv.most_similar(positive = list(searchText))[:5]
    for w in wiki:
        searchWiki.append(w)

    print(searchWiki)
    '''

    return searchText
