# deepRank.py
#
# Deep Rank 알고리즘을 이용해 정확도를 계산합니다.
# 
# uses
# # - findAt(searchTexts, index) : searchTexts를 포함하는 영상들의 목록을 반환합니다.
# - organize_weight(weight, whatzero) : 검색의 가중치를 동적으로 조절합니다.
#
# - getCategoryPerc(videoid, searchText_list) : category의 확률을 계산합니다.
# - getKeywordPerc(videoid, searchText_list) : category의 확률을 계산합니다.
#
# return
# - (new)perc : 검색 결과 영상들의 id와 각 검색 파라미터의 확률을 반환합니다.

from .config import DB

from .models import Keyword
from .models import Metadatum

from sqlalchemy import and_
import re

def deepRank(weight, All, T, K, P):
    # searchTexts로 저장
    searchTexts = {}    # 0-All, 1-title, 2-presenter, 3-keyword
    searchText = []
    titleSet = set()
    presenterSet = set()
    keywordSet = set()
    categorySet = set()
    
    if All != None:
        for i in All:
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

    # weight(가중치) 정리 위해 결과가 나오지 않는 검색 파라미터 리스트 = whatzero
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
    # 검색 결과가 없는 경우, 빈 리스트 return
    if (len(whatzero) == 4):
        return {}

    # weight 정리
    weight = organize_weight(weight, whatzero)
    # 검색 대상이 되는 비디오 리스트 = video (type = set)
    video = set()
    video = titleSet.union(presenterSet)
    video.update(keywordSet)
    video.update(categorySet)
    print("video id list: "+str(video))
    print("organized weight: "+str(weight))
    # id 당 T P K C 확률 구하기
    perc = {}
    for vi in video:
        print("Retrieved video ID: "+str(vi))
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
                p = getKeywordPerc(vi,s_Texts)
                in_perc.append(round(p*100,2))
            else:
                in_perc.append(0)
        else:
            in_perc.append(0)
        if weight[3] != 0: # C의 확률 구하기
            if vi in categorySet:
                p = 0
                #s_Texts = searchTexts[0]
                p = getCategoryPerc(vi,searchTexts[0])
                in_perc.append(round(p*100,2))
            else:
                in_perc.append(0)
        else:
            in_perc.append(0)
        perc[vi] = in_perc
        #print(in_perc)
    # print(perc) #{80: [0, 0, 0], 21: [0, 0, 0.567], 22: [0, 0, 0.567], 77: [0, 0, 0.058]}
    # ranking 결과
    print("Ranking result: "+ str(perc))

    return perc

def organize_weight(weight, whatzero):
    n = 4 - len(whatzero)
    if n == 0:
        n = 1
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
    c = 0
    for w in weight:
        if w != 0:
            weight[c] += sum
        c+=1
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

# keyword 파라미터의 확률 구하기
def getKeywordPerc(videoid, searchText_list):
    searchText_perc=0   # searchText_perc --> searchText의 확률
    keywordPercFull=[]  # keywordPercFull --> keyword의 전체 확률 리스트
    for res in DB.session.query(Keyword).filter(Keyword.id == videoid).with_entities(Keyword.percent).all():
        for k in res:
            keywordPercFull.append(k)
    print("Video ID get keyword Percentage: "+str(videoid))

    resultKeyword = set() # resultKeyword, keyword 검색 결과 (percent, keyword)를 저장
    for searchText in searchText_list:
        for res in DB.session.query(Keyword).filter(Keyword.id == videoid).filter(Keyword.keyword.contains(searchText)).with_entities(Keyword.percent,Keyword.keyword).all():
            resultKeyword.add(res)
    # 검색을 끝낸 후, 검색 결과 중 percent를 합한다.
    for r in resultKeyword:
        searchText_perc += r[0]

    ## 가장 큰 수끼리의 합 = sum (예: 2단어를 검색할 시 제일 큰 두 수의 합이 가장 높은 확률=1로 치환하기 위함)
    n = len(searchText_list)
    keywordPercFull_bak = keywordPercFull[:]
    sum_list = []
    while n != 0:
        if len(keywordPercFull_bak) == 0:
            break
        max_percent = max(keywordPercFull_bak)
        sum_list.append(max_percent)
        keywordPercFull_bak.remove(max_percent)
        n -= 1
   
    sum = 0
    for i in range(0,len(sum_list)):
        sum += sum_list[i]
    sum = 1 if sum > 0.1 else sum

    if max(keywordPercFull) == 0 or searchText_perc == 0:
        return 0
    num = round(1 / len(searchText_list),1)     # 찾는 단어가 1개인 경우 가장 큰 확률을 1로, n개인 경우 가장 큰 확률을 1/n으로
    m = round(1/sum,3)
    print("get keyword result percentage: "+ str(round(searchText_perc*m,3)))
    return round(searchText_perc*m,3)

# category 파라미터의 확률 구하기
def getCategoryPerc(videoid, searchText_list):
    k_v=[]  # category 확률 전체 리스트
    k_v2=[] # category 종류 전체 리스트
    for res in DB.session.query(Metadatum).filter(Metadatum.id == videoid).with_entities(Metadatum.category_percent).all():
        for k in res:
            words = re.split(r'[ ,:]', k)
            for w in words:
                if len(w) != 0:     # category_percent가 여러개일 경우(0.4, 0.5) -> words ['0.4', '', '0.5'] -> words의 ''를 빼기 위함
                    k_v.append(float(w))
    for res in DB.session.query(Metadatum).filter(Metadatum.id == videoid).with_entities(Metadatum.category).all():
        for k in res:
            words = re.split(r'[ ,:]', k)
            for w in words:
                if len(w) != 0: 
                    k_v2.append(w)

    searchCategory_percent = 0
    for k in k_v2:
        for searchText in searchText_list:
            if k.lower() == searchText.lower():
                # db upload 실수로 category의 category percent가 들어가지지 않은 경우 
                # (예: 동물의 확률이 들어가 있지 않은 경우{IT,동물 - 0.3})
                if k_v2.index(k) >= len(k_v):
                    searchCategory_percent += 0
                else:
                    searchCategory_percent += k_v[k_v2.index(k)]
                if searchCategory_percent > 1:  # 예: 0.408, 0.595 확률일 경우 (숫자상 근소한 차이)
                    searchCategory_percent = 1

    ## 가장 큰 수끼리의 합 = sum (예: 2단어를 검색할 시 제일 큰 두 수의 합이 가장 높은 확률=1로 치환하기 위함)
    n = len(searchText_list)
    k_v_bak = k_v[:]
    sum_list = []
    while n != 0:
        if len(k_v_bak) == 0:
            break
        max_percent = max(k_v_bak)
        sum_list.append(max_percent)
        k_v_bak.remove(max_percent)
        n -= 1

    sum = 0
    for i in range(0,len(sum_list)):
        sum += sum_list[i]
    sum = 1 if sum > 1 else sum

    if max(k_v) == 0 or k_v2 == 0:
        return 0

    m = round(1/sum,3)
    print("Video ID get Category Percentage: "+str(videoid))
    print("get Category result percentage: "+ str(round(searchCategory_percent*m,3)))
    return round(searchCategory_percent*m,3)

