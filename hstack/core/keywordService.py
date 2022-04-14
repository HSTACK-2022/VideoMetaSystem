# getKeyword.py
# 키워드 -> 전처리

# 필요 모듈 -> knolpy{JPype(파일 필요), numpy}, nltk, sklearn, scipy
# 환경변수 경로체크! 가상환경 경로가 환경변수에 잘 있다면 없애도 됩니다.
# 요런식으로 쓰면 됩니당
# mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath)

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


from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from krwordrank.word import summarize_with_keywords

import konlpy
import nltk
import sys
from konlpy.tag import Okt 
from . import models

# 환경변수가 제대로 안돼서 넣음
#sys.path.append("C:\capstone\capstone\mhenv\Lib\site-packages")
verbose = False # 프로그램 진행을 보이는 정도

def getKeyword(videoId, min_count, max_length):
    filePath = models.Videopath.objects.get(id = videoId).textaddr

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


#print(mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath))