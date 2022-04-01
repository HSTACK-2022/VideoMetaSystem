# keyword.py
# 키워드 -> 전처리

# 필요 모듈 -> JPype(파일 필요), konlpy, nltk, numpy, sklearn, krwordrank
# 환경변수 경로체크! 가상환경 경로가 환경변수에 잘 있다면 없애도 됩니다.
# 요런식으로 쓰면 됩니당
# getKeyword(videoPath,min_count,max_length)

from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from krwordrank.word import summarize_with_keywords

import konlpy
import nltk
import sys
from konlpy.tag import Okt 

# 환경변수가 제대로 안돼서 넣음
#sys.path.append("C:\capstone\capstone\mhenv\Lib\site-packages")
#sys.path.append("E:\\Capstone\\myenv\\Lib\\site-packages")

#min_count = 3   # 단어의 최소 출현 빈도수 (그래프 생성 시)
#max_length = 10 # 단어의 최대 길이
verbose = True # 프로그램 진행을 보이는 정도
#videoPath = '../cache/sample2.txt'

# 키워드를 얻어옴
def getKeyword(videoPath, min_count = 3, max_length = 10):
    wordrank_extractor = KRWordRank(min_count, max_length , verbose)
    beta = 0.85    # PageRank의 decaying factor beta
    max_iter = 10
    texts = []
    keyword_list = []
    with open(videoPath, 'r', encoding='UTF8') as f:
        for line in f:
            texts.append(line)

    texts = [normalize(text, english=False , number=True) for text in texts ]
    stopwords ={'ERROR','할','단어'}
    #keywords = summarize_with_keywords(texts, min_count=5, max_length=10,
    #beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
    keywords = summarize_with_keywords(texts) # with default arguments
    #print(keywords)
    for word in keywords:
        splitWord = word.split(':')[0]
        keyword_list.append(splitWord+' ')
        print(splitWord, end=" ")
    word = postProcessing(keyword_list)
    return word

# 전처리 함수
def postProcessing(keyword_list):
    okt = Okt()
    noun = 'Noun'
    alpha = 'Alpha'
    for word in okt.pos(''.join(keyword_list), join=True):
        if noun in word or alpha in word:
            print(word.split('/')[0], end=" ")
            return word

