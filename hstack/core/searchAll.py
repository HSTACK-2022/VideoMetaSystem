# 2022.04.28
# search(searchTexts)로 실행 -> list로 메타데이터 가져옴

import os
import platform
from re import I
from unicodedata import category

from . import models
from unicodedata import category
from django.db.models import Q


# 상수 설정
OS = platform.system()

class Total:

    resultVideoIDList = set()
    finalDict = {}
    rankcount = {} # 정확도 합 카운트
    rankDict = {} #rank 딕셔너리
    rankDetail = [] #정확도 detail 텍스트
    detail = {}


    def searchWordFromDB(self,searchTexts):
        #resultVideoIDList = set()
        for searchText in searchTexts:
            # 쿼리셋.values('필드이름') : 해당 필드와 값들을 딕셔너리로 제공 ex : [{'id': 1234}, {'id': 5678}, {'id': 1212}]
            # 쿼리셋.values_list('필드이름') : 해당 필드의 값들을 튜플로 제공
            # 쿼리셋.values_list('필드이름', flat=True) : 해당 필드의 값들을 리스트로 제공

            # [1234, 5678, 1212] << 이런 식으로 나올 것이라 예상
            for k in models.Keywords.objects.filter(keyword__contains = searchText).exclude(expose = 0).values_list('id', flat=True):
                self.resultVideoIDList.add(k)    # id를 resultVideoIDList 집합에 저장
            for ti in models.Metadata.objects.filter(title__contains = searchText).values_list('id', flat=True).distinct():
                self.resultVideoIDList.add(ti)
            for p in models.Metadata.objects.filter(presenter__contains = searchText).values_list('id', flat=True).distinct():
                self.resultVideoIDList.add(p)
            for to in models.Timestamp.objects.filter(subtitle__contains = searchText).values_list('id', flat=True):
               self.resultVideoIDList.add(to)


    # 입력 값 일치율대로 점수 부여
    def getrank(self, searchTexts, videoId): #ranking algo
        self.rankcount = {"keyword":0,"title":0,"present":0,"subtitle":0} #rank 알고리즘 초기화
        for searchText in searchTexts:
            for k in models.Keywords.objects.filter(id = videoId).filter(keyword__contains = searchText).values_list('id', flat=True):
                self.rankcount["keyword"] += 5
            for ti in models.Metadata.objects.filter(id = videoId).filter(title__contains = searchText).values_list('id', flat=True).distinct():
                self.rankcount["title"] = 50
                self.rankDetail.append("제목일치")
            for p in models.Metadata.objects.filter(id = videoId).filter(presenter__contains = searchText).values_list('id', flat=True).distinct():
                self.rankcount["present"] = 50
                self.rankDetail.append("발표자일치")
            for to in models.Timestamp.objects.filter(id = videoId).filter(subtitle__contains = searchText).values_list('id', flat=True):
                self.rankcount["subtitle"] += 5

        print("bbbbbbbbbbbbbbbb"+str(self.rankDetail)+str(sum(self.rankcount.values())))
        return(sum(self.rankcount.values()), self.rankDetail)


    def getVideoMetadataFromID(self, videoId):
        # 아래는 단어찾은 비디오 id로 메타데이터 얻는 법
        # values_list() - 쿼리셋을 튜플로 변환 # [(5, 'post #1'), (6, 'title #1'), (7, 'title #2')]
        # values_list('title') # [('post #1',), ('title #1',), ('title #2',)]
        # values_list는 flat가능 -> 튜플이 아닌 리스트로 값 반환 그러나 값이 여러개일때는 사용X
        # values_list() - [5, 6, 7]  # values_list('title', flat=True) - ['post #1', 'title #1', 'title #2']
        print(videoId)
        self.finalDict = {} # 초기화
        keywordQ = Q()
        keywordQ &= Q(id = videoId)
        keywordQ &= Q(expose=True)
        metadataList = list(models.Metadata.objects.filter(id = videoId).all().values()) # values_list()로 하면 key없는 list형태로 반환
        keywordList = list(models.Keywords.objects.filter(keywordQ).all().values_list('keyword', flat=True).distinct()) # list형태
        #filePath = list(models.Videopath.objects.filter(id = videoId).all().values_list('videoaddr','imageaddr')) # imageaddr
        #timestamp = list(models.Timestamp.objects.filter(id = videoId).all().values())
        self.finalDict['id'] = videoId
        self.finalDict['metadata'] = metadataList
        self.finalDict['keyword'] = keywordList

        if OS == 'Windows':
            filePath = "\\media" + models.Videopath.objects.get(id = videoId).imageaddr.split('media')[1]
        else :
            filePath = "/media" + models.Videopath.objects.get(id = videoId).imageaddr.split('media')[1]

        fileName = os.listdir(models.Videopath.objects.get(id = videoId).imageaddr)[0]
        self.finalDict['thumbnail'] = os.path.join(filePath, fileName)
        #self.finalDict['filePath']=filePath
        #self.finalDict['timestamp']=timestamp

        return self.finalDict #해도 되고 밖에서 Total.finalDict 해도 되고 

    # 2022년 5월 16일 videoIdList를 받아와 filter search를 할 때 쓰임
    def getDetailVideoList(videoId, search_type, search_detail_type):
        finalDict = {} # 초기화
        keywordQ = Q()
        keywordQ &= Q(id = videoId)
        keywordQ &= Q(expose=True)
        if search_type == "category":
            if models.Metadata.objects.filter(id = videoId).filter(category = search_detail_type).exists():
                metadataList = list(models.Metadata.objects.filter(id = videoId).all().values())
                keywordList = list(models.Keywords.objects.filter(keywordQ).all().values_list('keyword', flat=True).distinct())
                finalDict['id'] = videoId
                finalDict['metadata'] = metadataList 
                finalDict['keyword']=keywordList
                if OS == 'Windows':
                    filePath = "\\media" + models.Videopath.objects.get(id = videoId).imageaddr.split('media')[1]
                else :
                    filePath = "/media" + models.Videopath.objects.get(id = videoId).imageaddr.split('media')[1]

                fileName = os.listdir(models.Videopath.objects.get(id = videoId).imageaddr)[0]
                finalDict['thumbnail'] = os.path.join(filePath, fileName)
        elif search_type == "method":
            if models.Metadata.objects.filter(id = videoId).filter(method = search_detail_type).exists():
                metadataList = list(models.Metadata.objects.filter(id = videoId).all().values())
                keywordList = list(models.Keywords.objects.filter(keywordQ).all().values_list('keyword', flat=True).distinct())
                finalDict['id'] = videoId
                finalDict['metadata'] = metadataList
                finalDict['keyword']=keywordList
                if OS == 'Windows':
                    filePath = "\\media" + models.Videopath.objects.get(id = videoId).imageaddr.split('media')[1]
                else :
                    filePath = "/media" + models.Videopath.objects.get(id = videoId).imageaddr.split('media')[1]
                    
                fileName = os.listdir(models.Videopath.objects.get(id = videoId).imageaddr)[0]
                finalDict['thumbnail'] = os.path.join(filePath, fileName)

        return finalDict
        

#searchTexts = ["황기", "메모리"]   
def search(searchTexts):
    a = Total()
    a.resultVideoIDList = set() # 두번째를 위해 초기화
    a.searchWordFromDB(searchTexts) # 찾고자 하는 단어를 가진 메타데이터 비디오id를 (resultVideoIDList) set으로 가져옴
    
    #resultVideoIDList
    searchResultMeta = []

    maxlist = [] # 알고리즘을 거친 후의 id 리스트
    rankDict = {} # 정확도 보내는 딕셔너리
    tttt = []

    #ranking algorithm
    for i in list(a.resultVideoIDList): # (resultVideoIDList)에 저장되어 있는 id로 메타데이터 가져옴
        if models.Videopath.objects.get(id = i).extracted == 1 or models.Videopath.objects.get(id = i).extracted == 2:
            # for rank algorithm.
            print(i) #id
            print(tttt)
            a.getrank(searchTexts,i) #해당 videoId의 정확도
            a.rankDetail = [] #초기화
            rankDict[i], a.detail[i] = a.getrank(searchTexts,i)
            print(a.detail[i])
            tttt.append(a.detail[i])

    print(searchResultMeta)

    #value 큰 순서대로 딕셔너리 재배열
    sdict = sorted(rankDict.items(), key=lambda x: x[1], reverse=True)

    maxlist = dict(sdict) #list형태의 딕셔너리를 딕셔너리 형태로 전환
    for j in maxlist:
        a.getVideoMetadataFromID(j) #id 받아오기
        searchResultMeta.append(a.finalDict)
        rankDict[i], a.detail[i] = a.getrank(searchTexts,i)
        print(a.detail)
        print(a.rankDetail)

    videoIdList = list(a.resultVideoIDList)
    searchResultMeta = list(searchResultMeta)
    categoryList = extractCategories(videoIdList)

    return (videoIdList, searchResultMeta, categoryList, a.detail)


# 2022년 5월 16일 videoIdList를 받아와 filter search를 할 때 쓰임
def detailSearch(videoIdList, search_type, search_detail_type):
    searchResultMeta = []
    newVideoIdList = list()
    for i in videoIdList:
        if models.Videopath.objects.get(id = i).extracted == 1 or models.Videopath.objects.get(id = i).extracted == 2:
            res = Total.getDetailVideoList(i, search_type, search_detail_type)
            if len(res) != 0:
                searchResultMeta.append(res)
                newVideoIdList.append(i)

    #print(searchResultMeta)
    return (newVideoIdList, searchResultMeta)


# 각 videoId에서 Categories를 뽑아낸다.
def extractCategories(videoIdList):
    categoryList = set()
    for videoId in videoIdList:
        category = models.Metadata.objects.get(id = videoId).category
        print(category)
        categoryList.add(category)

    return categoryList
