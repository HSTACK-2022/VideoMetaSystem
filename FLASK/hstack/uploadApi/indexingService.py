# indexingService.py
#
# audioScriptFile과 PPT의 OCR 결과값으로부터 index를 추출합니다.
# extractMetadata.py에 의해 호출됩니다.
# 
# uses
# - doIndexingService(videoId)
#
# parameters
# - videoId : DB Table들의 key로 쓰이는 video의 고유 id
# 
# return
# - True : 작업이 정상적으로 완료된 경우
# - False : 중간에 오류가 발생한 경우
#
#################################################################################
#
# from
# https://bab2min.tistory.com/552
# https://bab2min.tistory.com/570
#
# window
# - 문맥으로 사용할 단어의 개수.
#   기본값 5로 주면 특정 단어의 좌우 5개씩, 총 10개 단어를 문맥으로 사용합니다.
#
# coef
#  - 동시출현 빈도를 weight에 반영하는 비율. 기본값은 1.0로, 동시출현 빈도를 weight에 전부 반영. 
#    0.0일 경우 빈도를 반영하지 않고 모든 간선의 weight을 1로 동일하게 간주합니다.
#
# threshold
#  - 문서 요약시 관련있는 문장으로 여길 최소 유사도값.
#    기본값은 0.005이고, 이 값보다 작은 유사도를 가지는 문장쌍은 관련없는문장으로 처리합니다.
#

import os
import re
from unittest import result
import networkx

from . import calTime
from datetime import datetime
 
class RawSentence:
    def __init__(self, textIter):
        if type(textIter) == str: self.textIter = textIter.split('\n')
        else: self.textIter = textIter
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')
 
    def __iter__(self):
        for line in self.textIter:
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s: continue
                yield s
 
class RawSentenceReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')
 
    def __iter__(self):
        for line in open(self.filepath, encoding='utf-8'):
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s: continue
                yield s
 
class RawTagger:
    def __init__(self, textIter, tagger = None):
        if tagger:
            self.tagger = tagger
        else :
            from konlpy.tag import Komoran
            self.tagger = Komoran()
        if type(textIter) == str: self.textIter = textIter.split('\n')
        else: self.textIter = textIter
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')
 
    def __iter__(self):
        for line in self.textIter:
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a,b:a+b, ch[::2], ch[1::2]):
                if not s: continue
                yield self.tagger.pos(s)
 
class RawTaggerReader:
    def __init__(self, filepath, tagger = None):
        if tagger:
            self.tagger = tagger
        else :
            from konlpy.tag import Komoran
            self.tagger = Komoran()
        self.filepath = filepath
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')
 
    def __iter__(self):
        for line in open(self.filepath, encoding='utf-8'):
            ch = self.rgxSplitter.split(line)
            for s in map(lambda a,b:a+b, ch[::2], ch[1::2]):
                if not s: continue
                yield self.tagger.pos(s)

class TextRank:
    def __init__(self, **kargs):
        self.graph = None
        self.window = kargs.get('window', 5)
        self.coef = kargs.get('coef', 1.0)
        self.threshold = kargs.get('threshold', 0.01)
        self.dictCount = {}
        self.dictBiCount = {}
        self.dictNear = {}
        self.nTotal = 0
 
 
    def load(self, sentenceIter, wordFilter = None):
        def insertPair(a, b):
            if a > b: a, b = b, a
            elif a == b: return
            self.dictBiCount[a, b] = self.dictBiCount.get((a, b), 0) + 1
 
        def insertNearPair(a, b):
            self.dictNear[a, b] = self.dictNear.get((a, b), 0) + 1
 
        for sent in sentenceIter:
            for i, word in enumerate(sent):
                if wordFilter and not wordFilter(word): continue
                self.dictCount[word] = self.dictCount.get(word, 0) + 1
                self.nTotal += 1
                if i - 1 >= 0 and (not wordFilter or wordFilter(sent[i-1])): insertNearPair(sent[i-1], word)
                if i + 1 < len(sent) and (not wordFilter or wordFilter(sent[i+1])): insertNearPair(word, sent[i+1])
                for j in range(i+1, min(i+self.window+1, len(sent))):
                    if wordFilter and not wordFilter(sent[j]): continue
                    if sent[j] != word: insertPair(word, sent[j])
 
    def loadSents(self, sentenceIter, tokenizer = None):
        #RawSentenceReader('test7.txt'), lambda sent: filter(lambda x:x 'NNP', 'VV', 'VA'), tagger.pos(sent)
        import math
        def similarity(a, b):
            n = len(a.intersection(b))
            return n / float(len(a) + len(b) - n) / (math.log(len(a)+1) * math.log(len(b)+1))
 
        if not tokenizer: rgxSplitter = re.compile('[\\s.,:;-?!()"\']+')
        
        #~~~~~~~~~~~~~~~단어 넣기 수정~~~~~~~~~~~~~~~~~
        #인풋에 토큰들의 리스트의 리스트를 넣어주면 됩니다. 인풋은 결국 문장의 iterator로 처리되기 때문에, 문장의 리스트를 넣어도 작동하거든요.
        #토큰들의 리스트가 문장이라고 볼수 있기 때문에 토큰들의 리스트의 리스트를 넣어주시면 되겠습니다.
        
        sentSet = []
        #print(sentenceIter)
        for sent in filter(None, sentenceIter):
            if type(sent) == str:
                if tokenizer: s = set(filter(None, tokenizer(sent)))
                else: s = set(filter(None, rgxSplitter.split(sent)))  
            else: s = set(sent)
            if len(s) < 2: continue
            self.dictCount[len(self.dictCount)] = sent
            sentSet.append(s)
            #sentSet.append(sentSet2)

        #print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")    
        #print(sentSet) #단어 셋/ 집합
        #print("\n")   
    
           

        #각 문장을 정점으로하는 그래프를 생성
        #sentSet 내의 모든 두 쌍의 문장(sentSet[i]와 sentSet[j])에 대해 유사도를 계산하고, 
        #이 값이 특정한 threshold보다 높을 경우 i-j의 연결강도를 s로 설정

        for i in range(len(self.dictCount)):
            for j in range(i+1, len(self.dictCount)):
                s = similarity(sentSet[i], sentSet[j])
                if s < self.threshold: continue
                self.dictBiCount[i, j] = s
        #print("$$$$$$$$$$$$$$$$$$$$$$$")
        #print(self.dictCount)
   
 
    def getPMI(self, a, b):
        import math
        co = self.dictNear.get((a, b), 0)
        if not co: return None
        return math.log(float(co) * self.nTotal / self.dictCount[a] / self.dictCount[b])
 
    def getI(self, a):
        import math
        if a not in self.dictCount: return None
        return math.log(self.nTotal / self.dictCount[a])
 
    def build(self):
        self.graph = networkx.Graph()
        self.graph.add_nodes_from(self.dictCount.keys())
        for (a, b), n in self.dictBiCount.items():
            self.graph.add_edge(a, b, weight=n*self.coef + (1-self.coef))
 
    def rank(self):
        return networkx.pagerank(self.graph, weight='weight')
 
    def extract(self, ratio = 0.1):
        ranks = self.rank()
        #cand = sorted(ranks, key=ranks.get, reverse=True)[:int(len(ranks) * ratio)]
        cand = ['기능', '메모리', '세', '역할', '여러분', '것', '요청', '정도', '바로', '구조', '운영', '여기', '생각', '관리', '사용', '대표', '가지', '커널', '리소스', '체제', '형태', '프로', '문제', '입출력', '핵심', '한번', '뭔가', '실행', '하나', '정리', '우리', '파일', '그림', '단일', '자원']
        
        pairness = {}
        startOf = {}
        tuples = {}

       

        #cand 리스트에 있는 단어 목록들을 순회 
        #cand에는 텍스트 랭크를 기반으로 추출한 상위 N개의 키워드가 들어가 있
        for k in cand:
          
            tuples[(k,)] = self.getI(k) * ranks[k]
            #이 상위 N개의 키워드 간의 PMI를 계산하여 pairness에 저장
            #pairness의 key는 (키워드1, 키워드2)이고, value는 PMI값
            for l in cand:
                if k == l: continue
                pmi = self.getPMI(k, l)
                if pmi: pairness[k, l] = pmi
 
        for (k, l) in sorted(pairness, key=pairness.get, reverse=True):
            print(k[0], l[0] , pairness[k, l])
            if k not in startOf: startOf[k] = (k, l)
 
        for (k, l), v in pairness.items():
            pmis = v
            rs = ranks[k] * ranks[l]
            path = (k, l)
            tuples[path] = pmis / (len(path) - 1) * rs ** (1 / len(path)) * len(path)
            last = l


            #pairness에 저장된 값들을 활용해 키워드를 연장
            #예를 들어 pairness에 (키워드1, 키워드2)도 들어있고, (키워드2, 키워드3)도 들어있다면, 
            #이들을 연결해 (키워드1, 키워드2, 키워드3) 으로 확장
            while last in startOf and len(path) < 7:
                if last in path: break
                pmis += pairness[startOf[last]]
                last = startOf[last][1]
                rs *= ranks[last]
                path += (last,)
                tuples[path] = pmis / (len(path) - 1) * rs ** (1 / len(path)) * len(path)
 
        used = set()
        both = {}
        for k in sorted(tuples, key=tuples.get, reverse=True):
            if used.intersection(set(k)): continue
            both[k] = tuples[k]
            for w in k: used.add(w)
 
        return both
 
    def summarize(self, ratio = 0.333):
        r = self.rank()
        ks = sorted(r, key=r.get, reverse=True)[:int(len(r)*ratio)]
        #print(ks)
        return '\n'.join(map(lambda k:self.dictCount[k], sorted(ks)))


def doIndexingService(fileURL, totalDic):
    dirName = os.path.dirname(fileURL)
    audioScript = os.path.join(dirName, "fullScript.txt")
    
    resultDictionary = getIndexSentence(audioScript)

    '''
    videoIndexScript = os.path.join(dirName, "keyword_line.txt")
    isVideoIndexScript = os.path.isfile(videoIndexScript)

    if isVideoIndexScript:
        videoIndexScript = os.path.join(videopath.imageaddr, "keyword_line.txt")
        indexFromVideo = videoScript2Dic(videoIndexScript)
        resultDictionary.update(indexFromVideo)
    '''

    indexDict = dict()
    resultDictionary = sorted(resultDictionary.items())

    try :
        for item in resultDictionary :
            print(item[0])
            print(item[1])
            time = str(datetime.strptime(item[0], '%H:%M:%S')).split(' ')[1]
            indexDict[time] = item[1]

        totalDic['index'] = indexDict
        return True
    except Exception as e:
        print(e)
        print("### ERROR : doIndexingSerivce ###")
        return False


def getIndexSentence(audioScriptPath):
    resultDic = {}

    tr = TextRank()
    print('Load...')

    from konlpy.tag import Komoran
    tagger = Komoran()
    stopword = set([('있', 'VV'), ('하', 'VV'), ('되', 'VV')])
    tr.loadSents(RawSentenceReader(audioScriptPath), 
        lambda sent: filter(lambda x:x not in stopword and x[1] in ('NP','NNG', 'NNP', 'VV', 'VA'), tagger.pos(sent))) #대명사만 넣음 
    print('Build...') 
    #'NNG', 'NNP', 'VV', 'VA'

    tr.build()
    ranks = tr.rank()
    exList = []
    for k in sorted(ranks, key=ranks.get, reverse=True)[:10]:
        #문장번호/ TR/ 문장내용
        print("\t".join([str(k), str(ranks[k]), str(tr.dictCount[k])]))
        exList.append(str(tr.dictCount[k]))

    print("\n")
    print(tr.summarize(0.1),"\n") #문장 수 조절 

    if len(tr.summarize(0.1)) == 0:
        list = exList
    else:
        l = tr.summarize(0.1)
        list = l.split('\n') # k는 list
    try:
        audioScriptWithSecond = open(audioScriptPath, encoding='UTF-8-sig')
        
        vLineNum = 0
        for txtLine in audioScriptWithSecond:
            for alist in list:
                if txtLine.find(alist) >= 0:
                    time = calTime.calSec2Time(int(vLineNum) * 10)
                    print(vLineNum, alist)
                    resultDic[time]=alist.split('\n')[0]
                    vLineNum += 1
                    continue
            vLineNum += 1

        audioScriptWithSecond.close()
        print(">>>>>>>>>>>>>>>>>>>>>>>>>.")
        print(resultDic)
        return resultDic
    except:
        print('audio script file (with second) doesn\'t exist.')
        return None


def videoScript2Dic(videoIndexScript):
    resultDic = {}
    f = open(videoIndexScript, "r", encoding="UTF-8-sig")
    lines = f.readlines()
    	
    try:
        for line in lines:
            time = line.split(" :: ")[0]
            content = line.split(" :: ")[1].split("\n")[0]
            if content!=" ":
                resultDic[time] = content
        f.close()
        return resultDic
    except IOError as e :
        e.printStackTrace()
        return None