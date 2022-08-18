# 2022.04.28
# search(searchTexts)로 실행 -> list로 메타데이터 가져옴

from operator import index
import re
import os
import platform
from unicodedata import category

from importlib_metadata import MetadataPathFinder

from .models import Keyword
from .models import Videopath
from .models import Metadatum
from .models import Timestamp

from sqlalchemy import and_


# 상수 설정
OS = platform.system()

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
        print(videoId)
        self.finalDict = {} # 초기화
        keywordQ = and_(Keyword.id == videoId, Keyword.expose == True)
        
        mdlist = Metadatum.query.filter(Metadatum.id == videoId).first()              # values_list()로 하면 key없는 list형태로 반환
        mdlistDict = dict()
        mdlistDict['id'] = mdlist.id
        mdlistDict['title'] = mdlist.title
        mdlistDict['presenter'] = mdlist.presenter
        mdlistDict['category'] = mdlist.category
        mdlistDict['narrative'] = mdlist.narrative
        mdlistDict['method'] = mdlist.method
        mdlistDict['videoLength'] = mdlist.videoLength
        mdlistDict['videoFrame'] = mdlist.videoFrame
        mdlistDict['videoType'] = mdlist.videoType
        mdlistDict['videoSize'] = mdlist.videoSize
        mdlistDict['uploadDate'] = mdlist.uploadDate
        mdlistDict['voiceManRate'] = mdlist.voiceManRate
        mdlistDict['voiceWomanRate'] = mdlist.voiceWomanRate
        metadataList = list()
        metadataList.append(mdlistDict)
        
        keywordList = list()
        for kwlist in Keyword.query.filter(keywordQ).with_entities(Keyword.keyword).all(): # list형태
            for kw in kwlist:
                keywordList.append(kw)

        #filePath = list(models.Videopath.objects.filter(id = videoId).all().values_list('videoaddr','imageaddr')) # imageaddr
        #timestamp = list(models.Timestamp.objects.filter(id = videoId).all().values())
        self.finalDict['id'] = videoId
        self.finalDict['metadata'] = metadataList
        self.finalDict['keyword'] = keywordList
        self.finalDict['thumbnail'] = None

        if OS == 'Windows':
            filePath = Videopath.query.filter(Videopath.id == videoId).first().imageAddr.split('media')[1]
        else :
            filePath = Videopath.query.filter(Videopath.id == videoId).first().imageAddr.split('media')[2]

        count = 0
        imageList = os.listdir(Videopath.query.filter(Videopath.id == videoId).first().imageAddr.split("hstack\\")[1])
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

        


def searchTest(All, T, K, P):
    # searchTexts로 저장
    searchTexts = []
    if All != None:
        for i in All:
            searchTexts.append(i)
    else:
        if T != None:
            for i in T:
                searchTexts.append(i)
        if K != None:
            for i in K:
                searchTexts.append(i)
        if P != None:
            for i in P:
                searchTexts.append(i)

    titleSet = findAt(searchTexts, 0)
    presenterSet = findAt(searchTexts, 1)
    keywordSet = findAt(searchTexts, 2)
    categorySet = findAt(searchTexts, 3)
    
    weight = [0.3,0.3,0.2,0.2] # Title Presenter Keyword Category
    whatzero = []
    if len(titleSet) == 0:
        weight[0] = 0
        whatzero.append(0)
    if len(presenterSet) == 0:
        weight[1] = 0
        whatzero.append(1)
    if len(keywordSet) == 0:
        weight[2] = 0
        whatzero.append(2)
    if len(categorySet) == 0:
        weight[3] = 0
        whatzero.append(3)
    # weight 정리
    weight = organize_weight(weight, whatzero)
    # 검색 대상이 되는 비디오 리스트 = video (type = set)
    video = set()
    video = titleSet.union(presenterSet)
    video.update(keywordSet)
    video.update(categorySet)
    print(video)
    # id 당 T P K C 확률 구하기
    perc = {}
    for vi in video:
        print("$$$$$$$$$$$$$$$$$$")
        print(vi)
        in_perc = []
        if weight[0] != 0:  # T의 확률 구하기
            p = 0
            for searchText in searchTexts:
                if vi in titleSet:
                    p += 1
            if p > 0:
                in_perc.append(100)
            else:
                in_perc.append(0)
        else:
            in_perc.append(0)
        if weight[1] != 0: # P의 확률 구하기
            p = 0
            for searchText in searchTexts:
                if vi in presenterSet:
                    p += 1
            if p > 0:
                in_perc.append(100)
            else:
                in_perc.append(0)
        else:
            in_perc.append(0)
        if weight[2] != 0: # K의 확률 구하기
            if vi in keywordSet:
                p = 0
                for searchText in searchTexts:
                    print(searchText)
                    p += getKeywordPerc(vi,searchText)
                    print(p)
                in_perc.append(p*100)
            else:
                in_perc.append(0)
        else:
            in_perc.append(0)
        if weight[3] != 0: # C의 확률 구하기
            if vi in categorySet:
                p = 0
                for searchText in searchTexts:
                    p += getCategoryPerc(vi,searchText)
                in_perc.append(p*100)
            else:
                in_perc.append(0)
        else:
            in_perc.append(0)
        perc[vi] = in_perc
        #print(in_perc)
        #print(perc)
    print("^^^^^^^^^^^")
    print(in_perc)
    print(perc) #{80: [0, 0, 0], 21: [0, 0, 0.567], 22: [0, 0, 0.567], 77: [0, 0, 0.058]}
    # ranking 결과
    print(weight)
    rankDict = {}
    for videoid in perc:
        print("&&&&&&&&&&&&&&&")
        #print(videoid)
        #print(perc[videoid])
        cnt = 0
        sum = 0
        for p in perc[videoid]:
            sum+=round(p*weight[cnt],3)
            #print(round(p*weight[cnt]))
            cnt+=1
        #print("**!!")
        #print(sum)
        # if sum == 0:
        #     continue
        rankDict[videoid]=sum
    print("***************")
    print(rankDict)  #{80: 0.0, 21: 0.567, 22: 0.567, 77: 0.058, 78: 0.0}

    #value 큰 순서대로 딕셔너리 재배열
    sdict = sorted(rankDict.items(), key=lambda x: x[1], reverse=True)

    maxlist = dict(sdict) #list형태의 딕셔너리를 딕셔너리 형태로 전환
    print(maxlist.keys())


    a = Total()
    searchResultMeta = []
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(maxlist)
    for j in maxlist:
        print("////////////////////////")
        a.getVideoMetadataFromID(j) #id 받아오기
        searchResultMeta.append(a.finalDict)
        #print(a.finalDict)
        searchResultMeta.append(perc[j])
        #print(perc[j])

    tttt ={}
    print(maxlist)
    for m in maxlist:
        newlist = []
        newlist = perc[m]
        newlist.append(maxlist[m])
        tttt[m] = newlist
    print(tttt)

    videoIdList = list(maxlist.keys())
    searchResultMeta = list(searchResultMeta)
    categoryList = extractCategories(videoIdList)
    typeList = extractType(videoIdList)
    dataList = extractData(videoIdList)

    return (videoIdList, searchResultMeta, categoryList, typeList, dataList, tttt)

def getCategoryPerc(videoid, searchText):
    k_v=[]
    k_v2=[]
    for res in Metadatum.query.filter(Metadatum.id == videoid).with_entities(Metadatum.category_percent).all():
        for k in res:
            words = re.split(r'[ ,:]', k)
            for w in words:
                k_v.append(float(w))
    for res in Metadatum.query.filter(Metadatum.id == videoid).filter(Metadatum.category.contains(searchText)).with_entities(Metadatum.category).all():
        for k in res:
            words = re.split(r'[ ,:]', k)
            for w in words:
                k_v2.append(w)
    # print(k_v)
    # print(k_v2)
    # print(max(k_v))
    cnt=0
    for k in k_v2:
        if k == searchText:
            break
        cnt += 1
    # print(")))))__")
    # print(cnt)

    if max(k_v) == 0 or k_v2 == 0:
        return 0
    m = round(1/max(k_v),3)
    # print(m)
    # print(round(k_v[cnt]*m,3))
    return round(k_v[cnt]*m,3)
def getKeywordPerc(videoid, searchText):
    # keyword의 값 구해보기 예시: 77번
    # keyword는 포함이 아니라 정확히 같은 경우, 즉 1개만 나올때만 해야함
    # 이게 맞나싶지만 확률을 구하기 위해선 그래야 함
    # 누가 나 좀 살려줘
    
    # k_v --> keyword의 전체 확률 리스트
    # k_v2 --> searchText의 확률
    k_v=[]
    k_v2 = 0
    for res in Keyword.query.filter(Keyword.id == videoid).with_entities(Keyword.percent).all():
        for k in res:
            k_v.append(k)
    for res in Keyword.query.filter(Keyword.id == videoid).filter(Keyword.keyword.contains(searchText)).with_entities(Keyword.percent).all():
        for k in res:
            k_v2 = k
    # max 값 구하고 싶다면 아래처럼 - Django에서
    # obj = models.Keywords.objects.filter(id = 77).aggregate(percent=Max('percent'))
    # print(obj)
    # print(obj['percent'])
    
    print(k_v)
    print(k_v2)
    print(max(k_v))

    if max(k_v) == 0 or k_v2 == 0:
        return 0
    m = round(1/max(k_v),3)
    print(m)
    return round(k_v2*m,3)

def organize_weight(weight, whatzero):
    n = 4 - len(whatzero)
    sum = 0
    while len(whatzero)>0:
        p = whatzero.pop()
        if p==2:
            sum += round(0.2 / n,2)
        elif p == 3:
            sum += round(0.2 / n,2)
        elif p==0:
            sum += round(0.3 / n,2)
        elif p==1:
            sum += round(0.3 / n,2)
    #print(sum)
    c = 0
    for w in weight:
        if w != 0:
            weight[c] += sum
        c+=1
    #print(weight)
    return weight                  
def findAt(searchTexts, index):
    result = set()
    for searchText in searchTexts:
        if index == 0:
            for title in Metadatum.query.filter(Metadatum.title.contains(searchText)).with_entities(Metadatum.id).all():
                for ti in title:
                    result.add(ti)
        elif index == 1:
            for pre in Metadatum.query.filter(Metadatum.presenter.contains(searchText)).with_entities(Metadatum.id).all():
                for p in pre:
                    result.add(p)
        elif index == 2:
            for key in Keyword.query.filter(and_(Keyword.keyword.contains(searchText), Keyword.expose!=0)).with_entities(Keyword.id).all():
                for k in key:
                    result.add(k)
        elif index == 3:
            for cat in Metadatum.query.filter((Metadatum.category.contains(searchText))).with_entities(Metadatum.id).all():
                for c in cat:
                    result.add(c)

    #print(result)
    if len(result) == 0:
        return set()
    else:
        return result

# 2022년 5월 16일 videoIdList를 받아와 filter search를 할 때 쓰임
def detailSearch(videoIdList, search_type, search_detail_type, All, T, K, P):
    searchResultMeta = []
    newVideoIdList = list()

    # searchTexts로 저장
    searchTexts = []
    if All != None:
        for i in All:
            searchTexts.append(i)
    else:
        if T != None:
            for i in T:
                searchTexts.append(i)
        if K != None:
            for i in K:
                searchTexts.append(i)
        if P != None:
            for i in P:
                searchTexts.append(i)
    
    for i in videoIdList:
        if models.Videopath.objects.get(id = i).extracted == 1 or models.Videopath.objects.get(id = i).extracted == 2:
            res = Total.getDetailVideoList(i, search_type, search_detail_type)
            if len(res) != 0:
                #searchResultMeta.append(res)
                newVideoIdList.append(i)

            ##
    maxlist = [] # 알고리즘을 거친 후의 id 리스트
    rankDict = {} # 정확도 보내는 딕셔너리
    tttt = {}
    a = Total()
    #ranking algorithm
    for i in list(newVideoIdList): # (resultVideoIDList)에 저장되어 있는 id로 메타데이터 가져옴
        if models.Videopath.objects.get(id = i).extracted == 1 or models.Videopath.objects.get(id = i).extracted == 2:
            #print(i) #id
            # a.getrank(searchTexts,i) #해당 videoId의 정확도
            a.rankDetail = [] #초기화
            rank, details, isValid = a.getrank(i, All=All, T=T, K=K, P=P)

            if isValid:
                rankDict[i] = rank
                a.detail[i] = details
                tttt[i] = a.detail[i]

            # perc 값이 0인 경우 유효하지 않은 값이기 때문에 제거해야한다.
            if not isValid:
                print("&&&&&&&&&&& NOT VALID &&&&&&&&&&&&&")


    # for i in rangelist(a.resultVideoIDList):
    #     print(rankDict[i]['전체스코어'])

    #value 큰 순서대로 딕셔너리 재배열
    sdict = sorted(rankDict.items(), key=lambda x: x[1], reverse=True)

    maxlist = dict(sdict) #list형태의 딕셔너리를 딕셔너리 형태로 전환
    print(maxlist.keys())
    for j in maxlist:
        a.getVideoMetadataFromID(j) #id 받아오기
        searchResultMeta.append(a.finalDict)
        searchResultMeta.append(a.detail[j])

    newVideoIdList = list(maxlist.keys())
    print(newVideoIdList)
    ##
    
    categoryList = extractCategories(newVideoIdList)
    typeList = extractType(newVideoIdList)
    dataList = extractData(newVideoIdList)

    return (newVideoIdList, searchResultMeta, categoryList, typeList, dataList, tttt)


# 각 videoId에서 narrative를 뽑아낸다.
def extractType(videoIdList):
    typeList = set()
    for videoId in videoIdList:
        if(Metadatum.query.filter(Metadatum.id == videoId).first().narrative):
            types = Metadatum.query.filter(Metadatum.id == videoId).first().narrative
            types = types.split(',')
            print(types)
            for c in types:
                typeList.add(c)

    return typeList

# 각 videoId에서 Categories를 뽑아낸다.
def extractCategories(videoIdList):
    categoryList = set()
    for videoId in videoIdList:
        if(Metadatum.query.filter(Metadatum.id == videoId).first().category):
            category = Metadatum.query.filter(Metadatum.id == videoId).first().category
            category = category.split(',')
            print(category)
            for c in category:
                categoryList.add(c)

    return categoryList

# 각 videoId에서 method를 뽑아낸다.
def extractData(videoIdList):
    dataList = set()
    for videoId in videoIdList:
        print(Metadatum.query.filter(Metadatum.id == videoId).first().method)
        if(Metadatum.query.filter(Metadatum.id == videoId).first().method):
            datas = Metadatum.query.filter(Metadatum.id == videoId).first().method
            datas = datas.split(',')
            print(datas)
            for c in datas:
                dataList.add(c)

    return dataList    