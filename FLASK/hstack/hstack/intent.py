# intent.py
#
# 검색어에서 핵심어를 추출합니다.
# 
# uses
# - init() : wiki 모델을 불러옵니다.
# - findWord(word) : word 검색어에서 핵심어를 추출합니다.
#
# parameters
# - word : 검색어


import os

from gensim.models import word2vec
from konlpy.tag import Okt
from . import deepRank

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

    # 3. get Category from word
    # 검색어에 해당하는 Category도 All에 포함
    l = getCategory(list(searchText))
    for ll in l:
        searchText.add(ll)

    '''
    # 3. run wiki model : get similar words
    wiki = wikiModel.wv.most_similar(positive = list(searchText))[:5]
    for w in wiki:
        searchWiki.append(w)
    print(searchWiki)
    '''

    print(searchText)

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
            intent_weight += round(intent_weight/n,2)
        else:
            result_all.append(perc)
            
    # print("최종 weight")
    # print(intent_weight)
    # print("최종 percentage")
    # print(result_all)

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
    # print("최종 dict")
    # print(re_dict)

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
    # print("After apply weight : ")
    # print(re_dict)

    # 총 랭킹 구하기
    ranking_weight = deepRank.organize_weight(deepRank_weight,whatzero)
    # print(ranking_weight)

    return re_dict, ranking_weight

openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
analysisCode = "ner"
import urllib3
import random
import json
from .config import STT_API_KEY
def getCategory(wordList):
    global accessKey
    accessKey = list(STT_API_KEY)
    # for i in range(0,len(wordList)):
    #     key_list = list(getCategoryService(accessKey[i%5],wordList[i]).keys())
    #     for key in key_list:
    #         to_category_set.add(key)
    # return list(to_category_set)    
    return list(getCategoryService(accessKey[random.randint(0,4)],' '.join(wordList)).keys())
def getCategoryService(accessKey, searchWord):
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": searchWord,
            "analysis_code": analysisCode
        }
    }
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    #print("[responseCode] " + str(response.status))
    if response.status == 200:
        return getCategoryFromJson(str(response.data, "utf-8"))
    else:
        return set()
def getCategoryFromJson(responseData):
    str = responseData
    json_obj = json.loads(str) # dumps - 파이썬 문자열을 json 형태로 변환
    json_text = json_obj['return_object']['sentence'][0]['NE'] # 형태소 태그 가져오기
    returnTypes = {}
    totalPerc = 0
    for i in json_text[0:]: # 리스트(json_text)의 형태소 태그 type들을 추출
        #print(i['type'])
        #print("+++")
        #print(i['weight'])
        percent = round(i['weight'], 3)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print(categoryClassification(i['type']))
        print(i)
        categoryDetect = categoryClassification(i['type'])
        if (categoryDetect != None):
            totalPerc += i['weight']
            returnTypes[categoryDetect] = round(percent, 2)

    #totalPerc 조정
    if totalPerc == 0:
        weight = 0
    else:
        weight = round(1.0 / totalPerc, 1)
    for key in returnTypes:
        returnTypes[key] = round(weight * returnTypes[key], 3)
        
    return returnTypes
def categoryClassification(each_tag):
    # 참고 십진분류법: http://www.booktrade.or.kr/kdc/kdc.jsp
    # 분류 ->

    # 철학
    # 종교
    # 사회과학 (정치/경제/사회, 교육, 법률/법학, 교통, 행정, 군사)
    # 순수과학 (자연, 과학)
    # 기술과학 (의학, It, 게임)
    # 예술 (미디어, 스포츠, 음악, 패션)
    # 언어
    # 문학
    # 역사 (지리, 문명/문화)
    # 지리...location,,..
    # ?요리, 건축

    # 정치/경제/사회, 교육, 미디어, 지리 , 스포츠, 과학, 법학, 종교, 
    # 의학, 요리, 건축, 음악, 문화, 교통, 예술, 언어, 패션, 사회과학, 철학, 역사,
    # 자연, It, 게임

    if 'TM' in each_tag:
        if each_tag == 'TMI_HW' or each_tag == 'TMI_SW' or each_tag == 'TMI_SERVICE':
            return('IT')
        elif each_tag == 'TM_CLIMATE':
            return('지리')
        elif each_tag == 'TM_CELL_TISSUE':
            # return('순수과학')
            # return('생명과학')
            return('의학')
        elif each_tag == 'TMM_DISEASE' or each_tag == 'TMM_DRUG':
            return('의학')
        elif each_tag == 'TMIG_GENRE':
            return('게임')
        elif each_tag == 'TM_SPORTS':
            return('스포츠')

    elif 'LC' in each_tag:
        return('지리')
        # LC_SPACE   천체 명칭?? 우주 넣어야하나 아님 걍 지리로?

    elif 'OG' in each_tag:
        if each_tag == 'OGG_ECONOMY':
            return('경제')
        elif each_tag == 'OGG_EDUCATION':
            return('교육')
        elif each_tag == 'OGG_MILITARY':
            return('군사')
        elif each_tag == 'OGG_MEDIA':
            return('미디어')
        elif each_tag == 'OGG_SPORTS':
            return('스포츠')
        elif each_tag == 'OGG_ART':
            return('예술')
        elif each_tag == 'OGG_MEDICINE':
            return('의학')
        elif each_tag == 'OGG_RELIGION':
            return('종교')
        elif each_tag == 'OGG_SCIENCE':
            return('과학')
        elif each_tag == 'OGG_LAW':
            return('법률/법학')
        elif each_tag == 'OGG_POLITICS':
            return('행정')
        elif each_tag == 'OGG_FOOD':
            return('요리')
        elif each_tag == 'OGG_HOTEL':
            return('여행') #숙박관련업체

    elif' AF' in each_tag:
        if each_tag == 'AF_CULTURAL_ASSET':
            return('문명/문화') #문화재
        elif each_tag == 'AF_BUILDING':
            return('건축')
        elif each_tag == 'AF_MUSICAL_INSTRUMENT':
            return('음악')
        elif each_tag == 'AF_ROAD':
            return('지리')
        elif each_tag == 'AF_WEAPON':
            return('군사')
        elif each_tag == 'AF_TRANSPORT':
            return('교통') #교통수단/자동차/선박 모델 및 유형, 운송 수단, 놀이기구
        elif each_tag == 'AF_WORKS':
            return('예술')
            #return('미술') #예술? 미술? /AFW의 세부 작품명에 해당하지 않는 기타 작품명
        elif each_tag == 'AFW_PERFORMANCE':
            return('예술')
        elif each_tag == 'AFW_VIDEO':
            return('미디어')
        elif each_tag == 'AFW_ART_CRAFT':
            return('예술')
            #return('미술')
        elif each_tag == 'AFW_MUSIC':
            return('음악')

    elif 'CV' in each_tag:
        if each_tag == 'CV_NAME':
            return('문명/문화')
        elif each_tag == 'CV_TRIBE':
            return('문명/문화')
        elif each_tag == 'CV_SPORTS':
            return('스포츠')
        elif each_tag == 'CV_SPORTS_INST':
            return('스포츠')
        elif each_tag == 'CV_POLICY':
            return('행정')
        elif each_tag == 'CV_TAX':
            return('행정')
        elif each_tag == 'CV_FUNDS':
            return('경제') 
        elif each_tag == 'CV_LANGUAGE':
            return('언어') 
        elif each_tag == 'CV_BUILDING_TYPE':
            return('건축')
        elif each_tag == 'CV_FOOD':
            return('요리')
        elif each_tag == 'CV_DRINK':
            return('요리')
        elif each_tag == 'CV_CLOTHING':
            return('패션')
        elif each_tag == 'CV_CURRENCY':
            return('경제')
        elif each_tag == 'CV_LAW':
            return('법률/법학')
        elif each_tag == 'CV_FOOD_STYLE   ':
            return('요리')
    
    elif 'PS_NAME' in each_tag:
        return
  
    elif 'AM' in each_tag:
        return('동물')

    elif 'PT' in each_tag:
        return('식물')

    elif 'QT' in each_tag:
        if each_tag == 'QT_TEMPERATURE':
            return('날씨') #온도 날씨 넣어야하나????????

    elif 'FD' in each_tag:
        if each_tag == 'FD_SCIENCE':
            return('과학')
        elif each_tag == 'FD_SOCIAL_SCIENCE':
            return('사회') #사회과학 학문 분야 및 학파, 정치/경제/사회와 관련된 분야
        elif each_tag == 'FD_MEDICINE':
            return('의학')
        elif each_tag == 'FD_ART':
            return('예술')
        elif each_tag == 'FD_PHILOSOPHY':
            return('철학')
    
    elif 'TR' in each_tag:
        if each_tag == 'TR_SCIENCE':
            return('과학')
        elif each_tag == 'TR_SOCIAL_SCIENCE':
            return('사회') #사회과학 이론/법칙/방법/원리/사상, 정치사상
        elif each_tag == 'TR_MEDICINE':
            return('의학')
        elif each_tag == 'TR_ART':
            return('예술')
        elif each_tag == 'TR_PHILOSOPHY':
            return('철학')

    elif 'EV' in each_tag:
        if each_tag == 'EV_ACTIVITY':
            return('역사???') #사회운동 및 선언
        elif each_tag == 'EV_WAR_REVOLUTION':
            return('역사') 
        elif each_tag == 'EV_SPORTS':
            return('스포츠')
    
    elif 'MT' in each_tag:
        return('과학')
