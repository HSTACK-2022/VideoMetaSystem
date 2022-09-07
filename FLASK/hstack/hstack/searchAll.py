# 2022.04.28
# search(searchTexts)로 실행 -> list로 메타데이터 가져옴

import re
import os

from .config import OS
from .config import DB

from .models import Keyword
from .models import Videopath
from .models import Metadatum
from .models import Timestamp

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
        print(videoId)
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

        if OS == 'Windows':
            filePath = DB.session.query(Videopath).filter(Videopath.id == videoId).first().imageAddr.split('media')[1]
        else :
            filePath = DB.session.query(Videopath).filter(Videopath.id == videoId).first().imageAddr.split('media')[2]

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


def getCategoryPerc(videoid, searchText):
    k_v=[]
    k_v2=[]
    for res in DB.session.query(Metadatum).filter(Metadatum.id == videoid).with_entities(Metadatum.category_percent).all():
        for k in res:
            words = re.split(r'[ ,:]', k)
            for w in words:
                if w == '': k_v.append(0.0)
                else:       k_v.append(float(w))
    for res in DB.session.query(Metadatum).filter(Metadatum.id == videoid).filter(Metadatum.category.contains(searchText)).with_entities(Metadatum.category).all():
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
    k_v2=0
    for res in DB.session.query(Keyword).filter(Keyword.id == videoid).with_entities(Keyword.percent).all():
        for k in res:
            k_v.append(k)
    for res in DB.session.query(Keyword).filter(Keyword.id == videoid).filter(Keyword.keyword.contains(searchText)).with_entities(Keyword.percent).all():
        for k in res:
            k_v2 = k
    # max 값 구하고 싶다면 아래처럼 - Django에서
    # obj = models.Keywords.objects.filter(id = 77).aggregate(percent=Max('percent'))
    # print(obj)
    # print(obj['percent'])
    
    #print(k_v)
    #print(k_v2)
    #print(max(k_v))

    if max(k_v) == 0 or k_v2 == 0:
        return 0
    m = round(1/max(k_v),3)
    print(round(k_v2*m,3))
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


# 특정 단어가 들어있는 video들을 찾는다.
def findAt(searchTexts, index):
    result = set()
    for searchText in searchTexts:
        if index == 0:
            for title in DB.session.query(Metadatum).filter(Metadatum.title.contains(searchText)).with_entities(Metadatum.id).all():
                for ti in title:
                    result.add(ti)
        elif index == 1:
            for pre in DB.session.query(Metadatum).filter(Metadatum.presenter.contains(searchText)).with_entities(Metadatum.id).all():
                for p in pre:
                    result.add(p)
        elif index == 2:
            for key in DB.session.query(Keyword).filter(and_(Keyword.keyword.contains(searchText), Keyword.expose!=0)).with_entities(Keyword.id).all():
                for k in key:
                    result.add(k)
        elif index == 3:
            for cat in DB.session.query(Metadatum).filter((Metadatum.category.contains(searchText))).with_entities(Metadatum.id).all():
                for c in cat:
                    result.add(c)

    return result


# 각 videoId에서 narrative를 뽑아낸다.
def extractType(videoIdList):
    typeList = set()
    for videoId in videoIdList:
        if (DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().narrative):
            types = DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().narrative
            types = types.split(',')
            print(types)
            for c in types:
                typeList.add(c)

    return typeList

# 각 videoId에서 Categories를 뽑아낸다.
def extractCategories(videoIdList):
    categoryList = set()
    for videoId in videoIdList:
        if (DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().category):
            category = DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().category
            category = category.split(', ')
            print(category)
            for c in category:
                categoryList.add(c)

    return categoryList

# 각 videoId에서 presentation(method)를 뽑아낸다.
def extractData(videoIdList):
    dataList = set()
    for videoId in videoIdList:
        if (DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().presentation):
            datas = DB.session.query(Metadatum).filter(Metadatum.id == videoId).first().presentation
            datas = datas.split(', ')
            print(datas)
            for c in datas:
                dataList.add(c)

    return dataList    


# not DetailSearch
def search(All, T, K, P):
    # searchTexts로 저장
    searchTexts = {}    # 0-All, 1-title, 2-presenter, 3-keyword
    searchText = []
    titleSet = set()
    presenterSet = set()
    keywordSet = set()
    categorySet = set()
    if All != None:
        for i in All:
            #searchTexts.append(i)
            searchText.append(i)
        searchTexts[0] = searchText
        titleSet = findAt(searchTexts[0], 0)
        presenterSet = findAt(searchTexts[0], 1)
        keywordSet = findAt(searchTexts[0], 2)
        categorySet = findAt(searchTexts[0], 3)
            
    else:
        if T != None:
            searchText = []
            for i in T:
                searchText.append(i)
            searchTexts[1] = searchText
            titleSet = findAt(searchTexts[1], 0)
        if K != None:
            searchText = []
            for i in K:
                searchText.append(i)
            searchTexts[3] = searchText
            keywordSet = findAt(searchTexts[3], 2)
        if P != None:
            searchText = []
            for i in P:
                searchText.append(i)
            searchTexts[2] = searchText
            presenterSet = findAt(searchTexts[2], 1)
        categorySet = set()

    # titleSet = findAt(searchTexts, 0)
    # presenterSet = findAt(searchTexts, 1)
    # keywordSet = findAt(searchTexts, 2)
    # categorySet = findAt(searchTexts, 3)
    
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

    # 검색 결과가 없는 경우 return
    if (len(whatzero) == 4):
        return {}, {}, {}

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
            if All == None:
                s_Texts = searchTexts[1]
            else:
                s_Texts = searchTexts[0]
            for searchText in s_Texts:
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
            if All == None:
                s_Texts = searchTexts[2]
            else:
                s_Texts = searchTexts[0]
            for searchText in s_Texts:
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
                if All == None:
                    s_Texts = searchTexts[3]
                else:
                    s_Texts = searchTexts[0]
                for searchText in s_Texts:
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
                for searchText in searchTexts[0]:
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
        cnt = 0
        sum = 0
        for p in perc[videoid]:
            sum+=round(p*weight[cnt], 2)
            cnt+=1
        sum = round(sum, 2)     # 59.730000000000000000004 방지
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
        a.getVideoMetadataFromID(j) #id 받아오기
        searchResultMeta.append(a.finalDict)
        #print(a.finalDict)
        searchResultMeta.append(perc[j])
        #print(perc[j])

    tttt ={}
    #print(maxlist)
    for m in maxlist:
        newlist = []
        newlist = perc[m]
        newlist.append(maxlist[m])
        tttt[m] = newlist
    print(tttt)

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
        if category != "":
            if DB.session.query(Metadatum).filter(and_(Metadatum.id == id, Metadatum.category.contains(category))).first() == None:
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

    print(newVideoMetaList)

    return (newVideoIdList, newVideoMetaList, newRankData)
    