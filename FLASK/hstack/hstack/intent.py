# intent.py
#
# 검색어에서 핵심어를 추출합니다.
# 
# uses
# - init() : wiki 모델을 불러옵니다.
# - findWord(word) : word 검색어에서 핵심어를 추출합니다.
# - doIntent(indeTexts) : indexTextes 검색어의 각 검색 파라미터 가중치 계산
#
# parameters
# - word : 검색어
#
# return
# - (new)searchText : 검색어의 핵심어 리스트
# - (new)re_dict, ranking_weight : 검색 결과 영상ID와 각 파라미터 랭킹 확률, 

import os

from gensim.models import word2vec
from konlpy.tag import Okt
from . import deepRank
from . import getCategory

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
    print("Keyword Extraction from Search sentences: "+ str(wordWithTag))

    # 2. extract noun, adj, verb
    searchText = set()
    for word, val in wordWithTag:
        if val in availTag:
            searchText.add(word)
            #searchWiki.append((word, 1.0))

    # 3. get Category from word
    # 검색어에 해당하는 Category도 All에 포함
    l = getCategory.getCategory(list(searchText))
    for ll in l:
        searchText.add(ll)

    '''
    # 3. run wiki model : get similar words
    wiki = wikiModel.wv.most_similar(positive = list(searchText))[:5]
    for w in wiki:
        searchWiki.append(w)
    print(searchWiki)
    '''

    print("Search Keyword :"+str(searchText))

    return searchText

def doIntent(indexTexts):   
    # 문장 검색의 각 검색 파라미터의 가중치 계산
    # 예: '운영체제가 스레드를 만드는 방법'을 검색 -> 검색 파라미터 = '운영','체제','스레드','만들다','방법' -> 각 파라미터의 가중치 = 0.2
    n = len(indexTexts)
    intent_weight = 1/n
    result_all = [] # 검색된 전체 결과 리스트

    for s in indexTexts:
        deepRank_weight = [0.3,0.3,0.2,0.2]
        perc = deepRank.deepRank(deepRank_weight, s.split(), None, None, None)
        # 검색 파라미터의 검색 결과가 없는 경우 가중치 재정립
        if perc=={}:
            n -= 1
            if n == 0:  # 검색 결과가 없는  경우 return
                return
            intent_weight += round(intent_weight/n,2)
        else:
            result_all.append(perc)

    deepRank_weight = [0.3,0.3,0.2,0.2] # deepRank_weight 재저장
    # 결과 딕셔너리 합치기
    result_dict = {} 
    for result in result_all:  # 리스트의 각 딕셔너리 (예: result={101: [100, 0, 65.5, 0], 77: [100, 0, 100.0, 0]})
        for r in result:    # 예: r=101,77
            if r in result_dict:
                result_dict[r].extend(result[r])
            else:
                result_dict[r] = result[r]

    # 가중치 적용된 확률 딕셔너리
    n = 0
    re_dict={}
    for key,value in result_dict.items():   # {101: [100, 0, 65.5, 0], 77: [100, 0, 100.0, 0]}
        n = 0
        perlist = [0,0,0,0]
        for v in value:
            perlist[n%4] += v*intent_weight
            n += 1
        re_dict[key] = perlist

    # max 구하기
    maxList = [0, 0, 0, 0]
    for value in re_dict.values():
        for i in range(0, 4):
            maxList[i] = max(maxList[i], value[i])

    # max weight 구하기
    whatzero = []
    for i in range(0, 4):
        if (maxList[i] != 0):
            maxList[i] = round(100/maxList[i], 2)
        else:
            whatzero.append(i)
            deepRank_weight[i] = 0
    # print("MAX : ")
    # print(maxList)

    # max weight 적용
    for key, value in re_dict.items():
        for i in range(0, 4):
            if (maxList[i] != 0):
                value[i] = round(value[i]*maxList[i],2)
            value[i] = 100 if value[i] > 100 else value[i]
    print("Final Ranking result : "+str(re_dict))

    # 총 랭킹 구하기
    ranking_weight = deepRank.organize_weight(deepRank_weight,whatzero)

    return re_dict, ranking_weight
