# searchAll.py
#
# 검색 결과를 제공합니다.
# 
# uses
# - search(All, T, K, P) : 검색어에 맞는 영상들을 찾아 메타데이터와 Deep Rank 결과를 반환합니다.
# - detailSearch(All, T, K, P, category, narrative, presentation) : search()에서 필터링이 걸린 경우 필터 결과를 반환합니다.
#
# - getVideoMetadataFromID(self, videoId) : videoId를 통해 해당 영상의 메타데이터 정보를 가져옵니다.
#
# - extractType(videoIdList) : videoIdList에 존재하는 Narrative Type을 뽑아냅니다.
# - extractData(videoIdList) : videoIdList에 존재하는 Prsentation을 뽑아냅니다.
# - extractCategories(videoIdList) : videoIdList에 존재하는 Category를 뽑아냅니다.
#
# * search(), detailSearch() 호출시 extract*()함수를 제외한 함수들이 호출됩니다.
#
# return
# - (new)videoIdList : 검색에 걸린 영상들의 id들의 리스트
# - (new)videoMetaList : 검색에 걸린 영상들의 메타데이터 리스트
# - (new)rankData : 검색에 걸린 영상들의 정확도(Deep Rank) 값

import re
import os

from .config import OS
from .config import DB

from .models import Keyword
from .models import Videopath
from .models import Metadatum

from sqlalchemy import and_


class Total:

    resultVideoIDList = set()
    finalDict = {}
    rankcount = {} # 정확도 합 카운트
    rankDict = {} #rank 딕셔너리
    rankDetail = [] #정확도 detail 텍스트
    detail = {}
    

    def getVideoMetadataFromID(self, videoId):
        # 아래는 단어찾은 비디오 id로 메타데이터 얻는 법
        # values_list() - 쿼리셋을 튜플로 변환 # [(5, 'post #1'), (6, 'title #1'), (7, 'title #2')]
        # values_list('title') # [('post #1',), ('title #1',), ('title #2',)]
        # values_list는 flat가능 -> 튜플이 아닌 리스트로 값 반환 그러나 값이 여러개일때는 사용X
        # values_list() - [5, 6, 7]  # values_list('title', flat=True) - ['post #1', 'title #1', 'title #2']
        self.finalDict = {} # 초기화
        keywordQ = and_(Keyword.id == videoId, Keyword.expose == True)
        
        # dict로 만들기
        mdlist = Metadatum.query.filter(Metadatum.id == videoId).first()
        #mdlist = DB.session.query(Metadatum).filter(Metadatum.id == videoId).first()
        

        mdlistDict = dict()
        mdlistDict['id'] = mdlist.id
        mdlistDict['title'] = mdlist.title
        mdlistDict['presenter'] = mdlist.presenter
        mdlistDict['category'] = mdlist.category
        mdlistDict['narrative'] = mdlist.narrative
        mdlistDict['presentation'] = mdlist.presentation
        mdlistDict['videoLength'] = mdlist.videoLength
        mdlistDict['videoFrame'] = mdlist.videoFrame
        mdlistDict['videoType'] = mdlist.videoType
        mdlistDict['videoSize'] = mdlist.videoSize
        mdlistDict['uploadDate'] = mdlist.uploadDate
        #mdlistDict['voiceManRate'] = mdlist.voiceManRate
        #mdlistDict['voiceWomanRate'] = mdlist.voiceWomanRate
        metadataList = list()
        metadataList.append(mdlistDict)
        
        keywordList = list()
        for kwlist in DB.session.query(Keyword).filter(keywordQ).with_entities(Keyword.keyword).all(): # list형태
            for kw in kwlist:
                keywordList.append(kw)

        #filePath = list(models.Videopath.objects.filter(id = videoId).all().values_list('videoaddr','imageaddr')) # imageaddr
        #timestamp = list(models.Timestamp.objects.filter(id = videoId).all().values())
        self.finalDict['id'] = videoId
        self.finalDict['metadata'] = metadataList
        self.finalDict['keyword'] = keywordList
        self.finalDict['thumbnail'] = None

        filePath = DB.session.query(Videopath).filter(Videopath.id == videoId).first().imageAddr.split('media')[1]

        count = 0
        imageList = os.listdir(DB.session.query(Videopath).filter(Videopath.id == videoId).first().imageAddr)
        for file in imageList:
            if file.split(".")[1] == "jpg":
                count+=1
                if count > 1:
                    fileName = file
                    self.finalDict['thumbnail'] = os.path.join(filePath, fileName)
                    break

        if self.finalDict['thumbnail'] == None:
            self.finalDict['thumbnail'] = '/static/img/defThumbnail.jpg'
        
        #self.finalDict['filePath']=filePath
        #self.finalDict['timestamp']=timestamp

        return self.finalDict #해도 되고 밖에서 Total.finalDict 해도 되고 

# 각 videoId에서 narrative를 뽑아낸다.
def extractType(videoIdList):
    typeList = set()
    for videoId in videoIdList:
        if (DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().narrative):
            types = DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().narrative
            types = types.split(',')
            for c in types:
                typeList.add(c)

    return sorted(typeList)

# 각 videoId에서 Categories를 뽑아낸다.
def extractCategories(videoIdList):
    categoryList = set()
    for videoId in videoIdList:
        if (DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().category):
            category = DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().category
            category = category.split(', ')
            for c in category:
                if c != 'None' :
                    categoryList.add(c)

    return sorted(categoryList)

# 각 videoId에서 presentation 뽑아낸다.
def extractData(videoIdList):
    dataList = set()
    for videoId in videoIdList:
        if (DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().presentation):
            datas = DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().presentation
            datas = datas.split(', ')
            for c in datas:
                dataList.add(c)

    return sorted(dataList)    

from . import deepRank
from . import intent

# not DetailSearch
def search(All, T, K, P):
    weight = [0.3,0.3,0.2,0.2] # Title, Presenter, Keyword, Category    
    perc = {}
    if All != None:
        perc, weight = intent.doIntent(All)
    else:
        perc = deepRank.deepRank(weight, All, T, K, P) # return 예시: {80: [0, 0, 0], 21: [0, 0, 0.567], 22: [0, 0, 0.567], 77: [0, 0, 0.058]}

    videoIdList = []
    searchResultMeta = []
    tttt ={}
    # deepRank 결과, 검색 결과 영상이 없을 경우
    if type(perc) == type(None) or len(perc) == 0:
        return (videoIdList, searchResultMeta, tttt)

    rankDict = {}
    for videoid in perc:
        cnt = 0
        sum = 0
        for p in perc[videoid]:
            sum+=round(p*weight[cnt], 2)
            cnt+=1
        sum = round(sum, 2)
        # if sum == 0:
        #     continue
        rankDict[videoid]=sum
    print("VideoID and Ranking percent: "+str(rankDict)) #{80: 0.0, 21: 0.567, 22: 0.567, 77: 0.058, 78: 0.0}

    #value 큰 순서대로 딕셔너리 재배열
    sdict = sorted(rankDict.items(), key=lambda x: x[1], reverse=True)

    maxlist = dict(sdict) #list형태의 딕셔너리를 딕셔너리 형태로 전환

    a = Total()
    #searchResultMeta = []
    for j in maxlist:
        a.getVideoMetadataFromID(j) #id 받아오기
        searchResultMeta.append(a.finalDict)
        searchResultMeta.append(perc[j])

    for m in maxlist:
        newlist = []
        newlist = perc[m]
        newlist.append(maxlist[m])
        tttt[m] = newlist
    print("Ranking Result: "+ str(tttt))

    videoIdList = list(maxlist.keys())
    searchResultMeta = list(searchResultMeta)

    return (videoIdList, searchResultMeta, tttt)


# videoIdList를 받아와 filter search
def detailSearch(All, T, K, P, category, narrative, presentation):
    excpIdList = set()
    newVideoIdList = list()
    newVideoMetaList = list()
    newRankData = dict()
    
    # metadata와 rankdata를 다시 받기 위해 검색 재실행
    videoIdList, videoMetaList, rankData = search(All=All, T=T, P=P, K=K)

    # filter를 통해 빼는 것들의 index 받기
    for id in videoIdList:
        if len(category) != 0:
            for c in category:
                if DB.session.query(Metadatum).filter(and_(Metadatum.id == id, Metadatum.category.contains(c))).first() == None:
                    excpIdList.add(id)
        if narrative != "":
            if DB.session.query(Metadatum).filter(and_(Metadatum.id == id, Metadatum.narrative.contains(narrative))).first() == None:
                excpIdList.add(id)
        if presentation != "":
            if DB.session.query(Metadatum).filter(and_(Metadatum.id == id, Metadatum.presentation.contains(presentation))).first() == None:
                excpIdList.add(id)

    # id 제거
    for i in range(0, len(videoIdList)):
        if videoIdList[i] not in excpIdList:
            newVideoIdList.append(videoIdList[i])
            newVideoMetaList.append(videoMetaList[i*2])
            newRankData[videoIdList[i]] = rankData[videoIdList[i]]

    return (newVideoIdList, newVideoMetaList, newRankData)