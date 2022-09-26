# categoryService.py
#
# 영상의 키워드와 제목을 기반으로 카테고리를 추출합니다.
# extractMetadata.py에 의해 호출됩니다.
# 
# uses
# - extractCategory(fileURL, totalDic) : 비디오 파일에서 카테고리 추출
# - getCategoryService(accessKey, keywordList) : ETRI API를 호출하여 단어 정보 추출
# - getCategoryFromJson(responseData) : 추출된 단어 정보중 형태소 분리
# - categoryClassification(each_tag) : 10진 분류법을 바탕으로 카테고리 추출
# 
# * extractCategory() 호출시 나머지 함수 역시 호출됩니다.
#
# parameters
# - fileURL : 비디오 파일이 저장된 경로
# - totalDic : 카테고리 값과 확률을 저장할 딕셔너리
# - accessKey : ETRI API에 접근하기 위한 키 (config.py에 명시)
# - keywordList : 영상에서 추출한 키워드의 리스트
# - responseData : getCategoryService()에서, ETRI API를 호출하여 얻은 결과값
# - each_tag : getCategoryFromJson()에서, 결과값을 후처리하여 얻은 태그값
# 
# return
# - totalDic : 카테고리의 종류와 확률을 넣어 반환합니다.
#
# reference
# https://aiopen.etri.re.kr/guide_wiseNLU.php#group03



from tkinter import E
from xmlrpc.client import boolean
from http.client import HTTPConnection, ImproperConnectionState

import urllib3
import json
import time

from .config import STT_API_KEY
 
# 언어 분석 기술(문어)
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
analysisCode = "ner"

def extractCategory(fileURL, totalDic):
    # get from config.py
    global accessKey
    accessKey = list(STT_API_KEY)

    # videoId를 통해 Keyword list를 받아온다.
    getTopicDict = {}
    transferTo_list = []
    for key in totalDic['keyword'].keys():
        transferTo_list.append(key)
    transferTo_list.append(totalDic['title'])
    for j in range(0,5):
        time.sleep(0.5)
        for i in range(0,5):
            getTopicDict = getCategoryService(accessKey[i], transferTo_list)
    

    print(".......................")
    print(getTopicDict)
    if (len(getTopicDict) == 0):
        getTopicDict['None'] = 0
        
    print(getTopicDict)
    totalDic['category'] = getTopicDict


def getCategoryService(accessKey, keywordList):
    text = ', '.join(keywordList) # 리스트를 문자열로 변환

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
            return('법률*법학')
        elif each_tag == 'OGG_POLITICS':
            return('행정')
        elif each_tag == 'OGG_FOOD':
            return('요리')
        elif each_tag == 'OGG_HOTEL':
            return('여행') #숙박관련업체

    elif' AF' in each_tag:
        if each_tag == 'AF_CULTURAL_ASSET':
            return('문명*문화') #문화재
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
        elif each_tag == 'AFW_DOCUMENT':
            return('예술')

    elif 'CV' in each_tag:
        if each_tag == 'CV_NAME':
            return('문명*문화')
        elif each_tag == 'CV_TRIBE':
            return('문명*문화')
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
            return('법률*법학')
        elif each_tag == 'CV_FOOD_STYLE   ':
            return('요리')
  
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

    elif 'PS' in each_tag:
        return ('인물')