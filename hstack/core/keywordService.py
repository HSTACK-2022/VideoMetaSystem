# keywordService.py
#
# keyword를 추출하고, 그 keyword를 통해 category을 얻어냅니다.
#
# uses
# - doKeywordService(videoId)
# - mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath)
# - extractCategory(videoId)

# parameters
# - videoId : DB Table들의 key로 쓰이는 video의 고유 id
# - audioScriptPath : audio에서 추출한 text 파일의 경로
# - videoScriptPath : 
# - videoIndexScriptPath : 

# 필요 모듈 -> knolpy{JPype(파일 필요), numpy}, nltk, sklearn, scipy
# 환경변수 경로체크! 가상환경 경로가 환경변수에 잘 있다면 없애도 됩니다.

# 03.30 수정 1차 내용 
# -> getKeyword return 값을 리스트로 줌
# -> getKeyword 함수의 매개변수 이름 videoPath를 filePath 로 변경
# -> mergeKeyword 함수 구현 (return KEYWORD LIST)

# 04.01 수정 2차 내용 
# -> mergeKeyword에서 1.음성스크립트에서 키워드를 뽑는 경우랑 
# 2.영상+음성인 경우로 나눔
# 아래와 같이 쓰면 됨
# 1. mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath)
# 2. mergeKeyword(audioScriptPath, NULL, NULL)

# 테스트 위한 변수
min_count = 3   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 10 # 단어의 최대 길이
#audioScriptPath = '../cache/algoWithEnter.txt'
#videoScriptPath = '../cache/mytxt2.txt'
#videoIndexScriptPath = '../cache/mytxt.txt'

import os
from . import models

def doKeywordService(videoId):
    videopath = models.Videopath.objects.get(id = videoId)
    audioScript = videopath.textaddr
    videoScript = os.path.join(videopath.imageaddr, "keyword.txt")
    videoIndexScript = os.path.join(videopath.imageaddr, "keyword_line.txt")

    if (models.Metadata.objects.get(id = videoId).method=="PPT"):
        keywords = mergeKeyword(audioScript, videoScript, videoIndexScript)
    else :
        keywords = mergeKeyword(audioScript, None, None)

    if(keywords) :                
        for keyword in keywords :
            print(keyword, end='@')
            models.Keywords.objects.create(
                id = models.Videopath.objects.get(id=videoId),
                keyword = keyword
            )
        category = extractCategory(videoId)
        if(category):
            print("*************************************************")
            print(category)
            models.Metadata.objects.filter(id = videoId).update(category = category)
            return True
    return False


from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from krwordrank.word import summarize_with_keywords

import konlpy
import nltk
import sys
from konlpy.tag import Okt 

# 환경변수가 제대로 안돼서 넣음
#sys.path.append("C:\capstone\capstone\mhenv\Lib\site-packages")
verbose = False # 프로그램 진행을 보이는 정도

def getKeyword(filePath, min_count, max_length):
    wordrank_extractor = KRWordRank(min_count, max_length , verbose)
    beta = 0.85    # PageRank의 decaying factor beta
    max_iter = 10
    texts = []
    keyword_list = []
    with open(filePath, 'r', encoding='UTF8') as f:
        for line in f:
            texts.append(line)
    
    texts = [normalize(text,english=False , number=True) for text in texts ]
    stopwords ={'ERROR','할','단어'}
    #keywords = summarize_with_keywords(texts, min_count=5, max_length=10,
    #beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
    keywords = summarize_with_keywords(texts) # with default arguments
    #print(keywords)
    for word in keywords:
        splitWord = word.split(':')[0]
        keyword_list.append(splitWord+' ')
        #print(splitWord, end=" ")
    return postProcessing(keyword_list)


def postProcessing(keyword_list):
    okt = Okt()
    noun = 'Noun'
    alpha = 'Alpha'
    final_keywordList = []
    for word in okt.pos(''.join(keyword_list), join=True):
        if noun in word or alpha in word:
            #print(word.split('/')[0], end=" ")
            final_keywordList.append(word.split('/')[0])

    return final_keywordList


def mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath):
    audioScriptKeyword = []
    videoScriptKeyword = []
    videoIndexScriptKeyword = []
    audioScriptKeyword = getKeyword(audioScriptPath, min_count, max_length)
    print("audioScriptKeyword >> "+' '.join(audioScriptKeyword))
    set1 = set(audioScriptKeyword)


    if (videoScriptPath!=None and videoIndexScriptKeyword!=None):
        videoScriptKeyword = getKeyword(videoScriptPath,min_count,max_length)
        videoIndexScriptKeyword = getKeyword(videoIndexScriptPath,min_count,max_length)
        print("videoScriptKeyword >> "+' '.join(videoScriptKeyword))
        print("videoIndexScriptKeyword >> "+' '.join(videoIndexScriptKeyword))
        set2 = set(videoScriptKeyword)
        set1Inter2 = set1.intersection(set2)

        set3 = set(videoIndexScriptKeyword)
        return (list(set3.union(set1Inter2)))
    
    return list(set1)



# https://aiopen.etri.re.kr/guide_wiseNLU.php#group03
# -*- coding: utf-8 -*-
from tkinter import E
from xmlrpc.client import boolean
from http.client import HTTPConnection, ImproperConnectionState

import urllib3
import json
 
# 언어 분석 기술(문어)
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
analysisCode = "ner"

# API KEY 설정
def initCategory():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secretFile = os.path.join(BASE_DIR, 'secrets.json')
    with open(secretFile) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
            raise ImproperConnectionState(error_msg)

    return get_secret("STT_API_KEY")

def extractCategory(videoId):
    global accessKey
    accessKey = initCategory()
    # videoId를 통해 Keyword list를 받아온다.
    keywordList = models.Keywords.objects.filter(id = videoId).values_list('keyword', flat=True).distinct()
    print("******************************************")
    for k in keywordList :
        print(k)
    print("checked")
    getCategorySet=set()
    for i in range(0,5):
        getCategorySet|=getCategoryService(accessKey[i], keywordList)
    result = ','.join(getCategorySet) # 리스트를 문자열로 변환
    return result

def getCategoryService(accessKey, keywordList):
    text = ','.join(keywordList) # 리스트를 문자열로 변환
    requestJson = {
        "access_key": accessKey,
        "argument": {
            "text": text,
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
    print("[responseCode] " + str(response.status))
    if response.status == 200:
        return getCategoryFromJson(str(response.data, "utf-8"))
    else:
        return set()

def getCategoryFromJson(responseData):
    # str = {"result":0,"return_object":{"doc_id":"","DCT":"","category":"","category_weight":0.0,"title":{"text":"","NE":""},"metaInfo":{},"paragraphInfo":[],"sentence":[{"id":0.0,"reserve_str":"","text":"단일,기능,메모리,실행,파일,커널,관리,프로,구조,자원,입출력","morp":[{"id":0.0,"lemma":"단일","type":"NNG","position":0.0,"weight":0.0389027},{"id":1.0,"lemma":",","type":"SP","position":6.0,"weight":1.0},{"id":2.0,"lemma":"기능","type":"NNG","position":7.0,"weight":0.0429483},{"id":3.0,"lemma":",","type":"SP","position":13.0,"weight":1.0},{"id":4.0,"lemma":"메모리","type":"NNG","position":14.0,"weight":0.089975},{"id":5.0,"lemma":",","type":"SP","position":23.0,"weight":1.0},{"id":6.0,"lemma":"실행","type":"NNG","position":24.0,"weight":0.0415775},{"id":7.0,"lemma":",","type":"SP","position":30.0,"weight":1.0},{"id":8.0,"lemma":"파일","type":"NNG","position":31.0,"weight":0.0572481},{"id":9.0,"lemma":",","type":"SP","position":37.0,"weight":1.0},{"id":10.0,"lemma":"커널","type":"NNG","position":38.0,"weight":0.0159203},{"id":11.0,"lemma":",","type":"SP","position":44.0,"weight":1.0},{"id":12.0,"lemma":"관리","type":"NNG","position":45.0,"weight":0.063389},{"id":13.0,"lemma":",","type":"SP","position":51.0,"weight":1.0},{"id":14.0,"lemma":"프로","type":"NNG","position":52.0,"weight":0.0491239},{"id":15.0,"lemma":",","type":"SP","position":58.0,"weight":1.0},{"id":16.0,"lemma":"구조","type":"NNG","position":59.0,"weight":0.0477435},{"id":17.0,"lemma":",","type":"SP","position":65.0,"weight":1.0},{"id":18.0,"lemma":"자원","type":"NNG","position":66.0,"weight":0.0393283},{"id":19.0,"lemma":",","type":"SP","position":72.0,"weight":1.0},{"id":20.0,"lemma":"입","type":"NNG","position":73.0,"weight":0.0382438},{"id":21.0,"lemma":"출력","type":"NNG","position":76.0,"weight":0.0382438}],"WSD":[{"id":0.0,"text":"단일","type":"NNG","scode":"01","weight":1.0,"position":0.0,"begin":0.0,"end":0.0},{"id":1.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":6.0,"begin":1.0,"end":1.0},{"id":2.0,"text":"기능","type":"NNG","scode":"03","weight":4.0,"position":7.0,"begin":2.0,"end":2.0},{"id":3.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":13.0,"begin":3.0,"end":3.0},{"id":4.0,"text":"메모리","type":"NNG","scode":"00","weight":0.0,"position":14.0,"begin":4.0,"end":4.0},{"id":5.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":23.0,"begin":5.0,"end":5.0},{"id":6.0,"text":"실행","type":"NNG","scode":"02","weight":2.0,"position":24.0,"begin":6.0,"end":6.0},{"id":7.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":30.0,"begin":7.0,"end":7.0},{"id":8.0,"text":"파일","type":"NNG","scode":"03","weight":2.0,"position":31.0,"begin":8.0,"end":8.0},{"id":9.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":37.0,"begin":9.0,"end":9.0},{"id":10.0,"text":"커널","type":"NNG","scode":"00","weight":0.0,"position":38.0,"begin":10.0,"end":10.0},{"id":11.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":44.0,"begin":11.0,"end":11.0},{"id":12.0,"text":"관리","type":"NNG","scode":"04","weight":6.0,"position":45.0,"begin":12.0,"end":12.0},{"id":13.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":51.0,"begin":13.0,"end":13.0},{"id":14.0,"text":"프로","type":"NNG","scode":"03","weight":1.0,"position":52.0,"begin":14.0,"end":14.0},{"id":15.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":58.0,"begin":15.0,"end":15.0},{"id":16.0,"text":"구조","type":"NNG","scode":"05","weight":2.5,"position":59.0,"begin":16.0,"end":16.0},{"id":17.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":65.0,"begin":17.0,"end":17.0},{"id":18.0,"text":"자원","type":"NNG","scode":"04","weight":2.0,"position":66.0,"begin":18.0,"end":18.0},{"id":19.0,"text":",","type":"SP","scode":"00","weight":1.0,"position":72.0,"begin":19.0,"end":19.0},{"id":20.0,"text":"입출력","type":"NNG","scode":"00","weight":0.0,"position":73.0,"begin":20.0,"end":21.0}],"word":[{"id":0.0,"text":"단일,기능,메모리,실행,파일,커널,관\n리,프로,구조,자원,입출력","type":"","begin":0.0,"end":21.0}],"NE":[{"id":0.0,"text":"메모리","type":"TMI_HW","begin":4.0,"end":4.0,"weight":0.229931,"common_noun":0.0}],"NE_Link":[],"dependency":[],"SRL":[]}],"entity":[]}}
    str = responseData
    json_obj = json.loads(str) # dumps - 파이썬 문자열을 json 형태로 변환
    json_text = json_obj['return_object']['sentence'][0]['NE'] # 형태소 태그 가져오기
    print(json_text)
    returnTypes = set()
    for i in json_text[0:]: # 리스트(json_text)의 형태소 태그 type들을 추출
        print(i['type'])
        returnTypes.add(i['type'])

    return categoryClassification(returnTypes)

def categoryClassification(tagSet):
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

    category_list = set()
    for each_tag in tagSet:
        #print(each_tag)
        #print('TM' in each_tag)
        if 'TM' in each_tag:
            if each_tag == 'TMI_HW' or each_tag == 'TMI_SW' or each_tag == 'TMI_SERVICE':
                category_list.add('IT')
            elif each_tag == 'TM_CLIMATE':
                category_list.add('지리')
            elif each_tag == 'TM_CELL_TISSUE':
                category_list.add('순수과학')
                category_list.add('생명과학')
                category_list.add('의학')
            elif each_tag == 'TMM_DISEASE' or each_tag == 'TMM_DRUG':
                category_list.add('의학')
            elif each_tag == 'TMIG_GENRE':
                category_list.add('게임')
            elif each_tag == 'TM_SPORTS':
                category_list.add('스포츠')

        elif 'LC' in each_tag:
            category_list.add('지리')
            # LC_SPACE   천체 명칭?? 우주 넣어야하나 아님 걍 지리로?

        elif 'OG' in each_tag:
            if each_tag == 'OGG_ECONOMY':
                category_list.add('경제')
            elif each_tag == 'OGG_EDUCATION':
                category_list.add('교육')
            elif each_tag == 'OGG_MILITARY':
                category_list.add('군사')
            elif each_tag == 'OGG_MEDIA':
                category_list.add('미디어')
            elif each_tag == 'OGG_SPORTS':
                category_list.add('스포츠')
            elif each_tag == 'OGG_ART':
                category_list.add('예술')
            elif each_tag == 'OGG_MEDICINE':
                category_list.add('의학')
            elif each_tag == 'OGG_RELIGION':
                category_list.add('종교')
            elif each_tag == 'OGG_SCIENCE':
                category_list.add('과학')
            elif each_tag == 'OGG_LAW':
                category_list.add('법률/법학')
            elif each_tag == 'OGG_POLITICS':
                category_list.add('행정')
            elif each_tag == 'OGG_FOOD':
                category_list.add('요리')
            elif each_tag == 'OGG_HOTEL':
                category_list.add('여행') #숙박관련업체

        elif 'AF' in each_tag:
            if each_tag == 'AF_CULTURAL_ASSET':
                category_list.add('문명/문화') #문화재
            elif each_tag == 'AF_BUILDING':
                category_list.add('건축')
            elif each_tag == 'AF_MUSICAL_INSTRUMENT':
                category_list.add('음악')
            elif each_tag == 'AF_ROAD':
                category_list.add('지리')
            elif each_tag == 'AF_WEAPON':
                category_list.add('군사')
            elif each_tag == 'AF_TRANSPORT':
                category_list.add('교통') #교통수단/자동차/선박 모델 및 유형, 운송 수단, 놀이기구
            elif each_tag == 'AF_WORKS':
                category_list.add('예술')
                category_list.add('미술') #예술? 미술? /AFW의 세부 작품명에 해당하지 않는 기타 작품명
            elif each_tag == 'AFW_PERFORMANCE':
                category_list.add('예술')
            elif each_tag == 'AFW_VIDEO':
                category_list.add('미디어')
            elif each_tag == 'AFW_ART_CRAFT':
                category_list.add('예술')
                category_list.add('미술')
            elif each_tag == 'AFW_MUSIC':
                category_list.add('음악')

        elif 'CV' in each_tag:
            if each_tag == 'CV_NAME':
                category_list.add('문명/문화')
            elif each_tag == 'CV_TRIBE':
                category_list.add('문명/문화')
            elif each_tag == 'CV_SPORTS':
                category_list.add('스포츠')
            elif each_tag == 'CV_SPORTS_INST':
                category_list.add('스포츠')
            elif each_tag == 'CV_POLICY':
                category_list.add('행정')
            elif each_tag == 'CV_TAX':
                category_list.add('행정')
            elif each_tag == 'CV_FUNDS':
                category_list.add('경제') 
            elif each_tag == 'CV_LANGUAGE':
                category_list.add('언어') 
            elif each_tag == 'CV_BUILDING_TYPE':
                category_list.add('건축')
            elif each_tag == 'CV_FOOD':
                category_list.add('요리')
            elif each_tag == 'CV_DRINK':
                category_list.add('요리')
            elif each_tag == 'CV_CLOTHING':
                category_list.add('패션')
            elif each_tag == 'CV_CURRENCY':
                category_list.add('경제')
            elif each_tag == 'CV_LAW':
                category_list.add('법률/법학')
            elif each_tag == 'CV_FOOD_STYLE':
                category_list.add('요리')
  
        elif 'AM' in each_tag:
            category_list.add('동물')

        elif 'PT' in each_tag:
            category_list.add('식물')

        elif 'QT' in each_tag:
            if each_tag == 'QT_TEMPERATURE':
                category_list.add('날씨') #온도 날씨 넣어야하나????????

        elif 'FD' in each_tag:
            if each_tag == 'FD_SCIENCE':
                category_list.add('과학')
            elif each_tag == 'FD_SOCIAL_SCIENCE':
                category_list.add('사회') #사회과학 학문 분야 및 학파, 정치/경제/사회와 관련된 분야
            elif each_tag == 'FD_MEDICINE':
                category_list.add('의학')
            elif each_tag == 'FD_ART':
                category_list.add('예술')
            elif each_tag == 'FD_PHILOSOPHY':
                category_list.add('철학')
    
        elif 'TR' in each_tag:
            if each_tag == 'TR_SCIENCE':
                category_list.add('과학')
            elif each_tag == 'TR_SOCIAL_SCIENCE':
                category_list.add('사회') #사회과학 이론/법칙/방법/원리/사상, 정치사상
            elif each_tag == 'TR_MEDICINE':
                category_list.add('의학')
            elif each_tag == 'TR_ART':
                category_list.add('예술')
            elif each_tag == 'TR_PHILOSOPHY':
                category_list.add('철학')

        elif 'EV' in each_tag:
            if each_tag == 'EV_ACTIVITY':
                category_list.add('역사???') #사회운동 및 선언
            elif each_tag == 'EV_WAR_REVOLUTION':
                category_list.add('역사') 
            elif each_tag == 'EV_SPORTS':
                category_list.add('스포츠')
    
        elif 'MT' in each_tag:
             category_list.add('과학')
          
    return category_list


#example_list = {'입출력', '기능', '실행', '관리', '커널', '메모리', '구조', '자원', '프로', '파일', '단일'}
#extractCategory(example_list)

#category_list_example = {'TMM_DRUG','TM_CELL_TISSUE','TMI_SW','CV_POSITION'}
#print(categoryClassification(category_list_example))