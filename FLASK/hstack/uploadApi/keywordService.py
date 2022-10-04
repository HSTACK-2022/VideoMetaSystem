# keywordService.py
#
# keyword를 추출하고, 그 keyword를 통해 category을 얻어냅니다.
# extractMetadata.py에 의해 호출됩니다.
#
# uses
# - doKeywordService(fileURL)
# - mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath)
# - extractCategory(fileURL)
#
# parameters
# - fileURL : video 파일의 경로
# - totalDic : 키워드와 확률을 저장할 딕셔너리
# - audioScriptPath : audio에서 추출한 text 파일의 경로
# - videoScriptPath : video에서 추출한 keyword의 경로
# - videoIndexScriptPath : video에서 추출한 index의 경로
#
# return
# - totalDic : 키워드와 그 확률을 넣어 반환합니다.
#
#
# 필요 모듈 -> knolpy{JPype(파일 필요), numpy}, nltk, sklearn, scipy
# 환경변수 경로체크! 가상환경 경로가 환경변수에 잘 있다면 없애도 됩니다.
#
#
#
# <<03.30 수정 1차 내용>>
# -> getKeyword return 값을 리스트로 줌
# -> getKeyword 함수의 매개변수 이름 videoPath를 filePath 로 변경
# -> mergeKeyword 함수 구현 (return KEYWORD LIST)
#
# <<04.01 수정 2차 내용>> 
# -> mergeKeyword에서 1.음성스크립트에서 키워드를 뽑는 경우랑  2.영상+음성인 경우로 나눔
# 1. mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath)
# 2. mergeKeyword(audioScriptPath, NULL, NULL)
#
# <<09.15 수정 3차 내용>>
# -> 기존 videoScriptPath(OCR)과 videoIndexScriptPath(Index) 사용 중지 (04.01 수정 폐지)
# 영상으로부터 추출된 두 파일에 저장된 값이 안정적이지 않고
# audioScript 파일만으로 충분히 키워드 추출이 가능하다는 판단에 따라
# audioScript 파일을 이용하여 키워드를 추출합니다.
# -> 키워드 확률 추가
# konlpy를 이용한 키워드 추출시 나오는 확률 값을 바탕으로,
# 전체 키워드의 확률 값을 조정합니다.
# 추출된 키워드의 모든 확률을 더한 값이 1이 되도록 조정합니다.




# 테스트 위한 변수
min_count = 2   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 10 # 단어의 최대 길이

import os

def doKeywordService(fileURL, totalDic):
    dirName = os.path.dirname(fileURL)
    audioScript = os.path.join(dirName, "fullScript.txt")
    videoScript = os.path.join(dirName, "keyword.txt")
    videoIndexScript = os.path.join(dirName, "keyword_line.txt")
    
    isVideoScript = os.path.isfile(videoScript)
    isVideoIndexScript = os.path.isfile(videoIndexScript)

    #if (isVideoScript and isVideoIndexScript):
    #    keywords = mergeKeyword(audioScript, videoScript, videoIndexScript)
    #else :
    #    keywords = mergeKeyword(audioScript, None, None)

    totalDic['keyword'] = getKeyword(fileURL, audioScript, min_count, max_length)


from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from krwordrank.word import summarize_with_keywords

import konlpy
import nltk
import sys
from konlpy.tag import Okt 
from .models import Metadatum
# 환경변수가 제대로 안돼서 넣음
#sys.path.append("C:\capstone\capstone\mhenv\Lib\site-packages")
verbose = False # 프로그램 진행을 보이는 정도
def byte_transform(bytes, to, bsize=1024):
     a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
     r = float(bytes)
     for i in range(a[to]):
         r = r / bsize
     return round(r,2)

def getKeyword(fileURL, filePath, min_count, max_length):
    if(filePath == None):
        return
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
    
    size = os.path.getsize(fileURL)
    size = byte_transform(size,'m')
    min_count = int(size / 3)
    keywords = summarize_with_keywords(texts, min_count, max_length=10,
    beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
    #keywords = summarize_with_keywords(texts) # with default arguments
    print(keywords)
    #print(keywords.keys())
    print('\n')
    # for word in keywords:
    #     splitWord = word.split(':')[0]
    #     keyword_list.append(splitWord+' ')
    #     #print(splitWord, end=" ")
    return postProcessing(keywords)


def postProcessing(keyword_list):
    okt = Okt()
    noun = 'Noun'
    alpha = 'Alpha'
    adjective = 'Adjective'
    #final_keywordList = []
    final_keywordDict = {}
    sum = 0

    for k in keyword_list.keys():
        #print(keyword_list[k])
        for word in okt.pos(''.join(k), join=True):
            if noun in word or alpha in word:
                #print(word.split('/')[0], end=" ")
                percent = round(keyword_list[k],3)
                sum += percent
                final_keywordDict[(word.split('/')[0])] = percent
            
    for f in final_keywordDict:
        final_keywordDict[f] = round(final_keywordDict[f]/sum,3)
    print(final_keywordDict)
    # for word in okt.pos(''.join(keyword_list.keys()), join=True):
    #     print(word)
    #     if noun in word or alpha in word:
    #         #print(word.split('/')[0], end=" ")
    #         final_keywordList.append(word.split('/')[0])

    return final_keywordDict

def mergeKeyword(audioScriptPath, videoScriptPath, videoIndexScriptPath):
    audioScriptKeyword = []
    videoScriptKeyword = []
    videoIndexScriptKeyword = []
    audioScriptKeyword = getKeyword(audioScriptPath, min_count, max_length)
    print("audioScriptKeyword >> "+' '.join(audioScriptKeyword))
    set1 = set(audioScriptKeyword)

    # check is videoScriptPath valid
    content = ""
    if (videoScriptPath != None):
        content = open(videoScriptPath, 'r', encoding="utf-8-sig").readline().split("\n")[0]
        print(content == "")

    if (videoScriptPath!=None and videoIndexScriptKeyword!=None and content != ""):
        videoScriptKeyword = getKeyword(videoScriptPath,min_count,max_length)
        print("videoScriptKeyword >> "+' '.join(videoScriptKeyword))
        #videoIndexScriptKeyword = getKeyword(videoIndexScriptPath,min_count,max_length)
        #print("videoIndexScriptKeyword >> "+' '.join(videoIndexScriptKeyword))
        set2 = set(videoScriptKeyword)
        set1Inter2 = set1.union(set2)
        return (list(set1Inter2))

        #set3 = set(videoIndexScriptKeyword)
        #return (list(set3.union(set1Inter2)))
    
    return list(set1)