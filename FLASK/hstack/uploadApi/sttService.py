# sttService.py
#
# 오디오 파일을 ETRI의 STT API로 전송합니다.
# 오디오 파일을 텍스트 파일로 변환합니다.
# extractMetadata.py에 의해 호출됩니다.
# 
# uses
# - doSttService(fileURL, finalDic) : 비디오 파일을 오디오로 바꾼 뒤 텍스트 파일로 변환
# - audio2text(audioFilePath, i) : 10초단위 오디오 파일을 ETRI STT API로 전송
# - content2file(contents, filePath, isFirst) : content 내용을 filePath에 저장
# - pcm2text(audioFilePath, textPath) : 통 오디오 파일을 텍스트 파일로 변환
# - sttAsync(audioPath, endNum) : multi thread를 위한 함수.
# - threadWork(num) : multi thread를 위한 함수. 스레드 실행.
# - resultFileWrite(textPath, endNum) : multi thread의 결과를 취합하여 텍스트 파일에 저장.
# 
# * doSttService() 호출시 나머지 함수 역시 호출됩니다.
#
# parameters
# - fileURL : 비디오 파일이 저장된 경로
# - finalDic : 카테고리 값과 확률을 저장할 딕셔너리
# - accessKey : ETRI API에 접근하기 위한 키 (config.py에 명시)
# - keywordList : 영상에서 추출한 키워드의 리스트
# - responseData : getCategoryService()에서, ETRI API를 호출하여 얻은 결과값
# - each_tag : getCategoryFromJson()에서, 결과값을 후처리하여 얻은 태그값
# 
# return
# - totalDic : 카테고리의 종류와 확률을 넣어 반환합니다.

import os
import json
import base64
import urllib3
import threading

from pathlib import Path
from http.client import HTTPConnection, ImproperConnectionState
from urllib.error import HTTPError

from .config import OS
from .config import STT_API_KEY

from . import audioService


openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
languageCode = "korean"
audioContents = None
audioFile = None

# 파일의 경로를 받아 음원을 추출하고 텍스트파일로 바꾼다.
def doSttService(fileURL, finalDic):
    # get from config.py
    global accessKey
    accessKey = list(STT_API_KEY)

    # get Dir of SplitedAudioFile
    audioFilePath = audioService.video2splitedAudio(fileURL)
    finalDic['audioAddr'] = audioFilePath
    
    if audioFilePath!=None:
        textName = 'fullScript.txt'
        textPath = os.path.join(os.path.dirname(fileURL), textName)
        sttResult = pcm2text(audioFilePath, textPath)
        finalDic['textAddr'] = sttResult
        return finalDic
    else:
        return None

# AudioPath를 주면 STT 작업을 해서 뱉는다.
def audio2text(audioFilePath, i):
    result = None

    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()
    
    requestJson = {
        "access_key": accessKey[i],
        "argument": {
            "language_code": languageCode,
            "audio": audioContents
        }
    }
    
    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    
    if (str(response.status) == "200") :
        responBody = str(response.data, "utf-8")
        data = responBody.split("\"")[7]
        print(data)
        result = data
    else :
        result = "ERROR: " + str(response.status)

    return result

# Contents와 FilePath를 주면 파일에 적어서 뱉는다.
def content2file(contents, filePath, isFirst):
    f = open(filePath, "a", encoding="UTF-8")
    	
    try:
        # 이미 열려있던 파일이면 개행 후 시작하자.
        if (isFirst == False) :
            f.write("\n")
        f.write(contents)
        f.flush()
        f.close()
        return True
    except IOError as e :
        e.printStackTrace()
        return False


#이하 pcm2text
audioPath_0 = []
audioPath_1 = []
audioPath_2 = []
audioPath_3 = []
audioPath_4 = []
audioPathVector = []

result_0 = []
result_1 = []
result_2 = []
result_3 = []
result_4 = []
resultVector = []
threads = []

# audioPath와 filePath를 가지고 비동기적으로 파일변환
def pcm2text(audioFilePath, textPath) :
    endNum = len(os.listdir(audioFilePath))
    if sttAsync(audioFilePath, endNum) == True :
        if resultFileWrite(textPath, endNum) == True :
            return textPath
    return False

# 비동기적으로 pcm 파일을 text로 변환한다.
def sttAsync(audioPath, endNum):
    for i in range(0, endNum):
        if i%5 == 0:
            audioPath_0.append(os.path.join(audioPath, str(i)+".wav"))
        elif i%5 == 1:
            audioPath_1.append(os.path.join(audioPath, str(i)+".wav"))
        elif i%5 == 2:
            audioPath_2.append(os.path.join(audioPath, str(i)+".wav"))
        elif i%5 == 3:
            audioPath_3.append(os.path.join(audioPath, str(i)+".wav"))
        elif i%5 == 4:
            audioPath_4.append(os.path.join(audioPath, str(i)+".wav"))
    audioPathVector.append(audioPath_0)
    audioPathVector.append(audioPath_1)
    audioPathVector.append(audioPath_2)
    audioPathVector.append(audioPath_3)
    audioPathVector.append(audioPath_4)
    resultVector.append(result_0)
    resultVector.append(result_1)
    resultVector.append(result_2)
    resultVector.append(result_3)
    resultVector.append(result_4)

    try :
        for i in range(0, 5):
            th = threading.Thread(target=threadWork, args=([i]))
            th.start()
            threads.append(th)

        for thread in threads:
            thread.join()

        return True
    
    except Exception as e:
        print(e)
        return False

# thread 돌리기
def threadWork(num):
    threadAudioPath = audioPathVector[num]
    threadResult = resultVector[num]

    for i in range(0,len(threadAudioPath)):
        print(str(num) + ">>" + str(len(threadAudioPath)) + ">>" + str(threadAudioPath[i]))
        threadResult.append(audio2text(threadAudioPath[i], num)) # num -> keyNum
        # result of Pcm2Text = new Pcm2Text().pcm2text(String.valueOf(audioPath.get(i)),keys[number]
        # print("@@@@" + str(resultVector))

# thread 결과물 textPath에 저장
def resultFileWrite(textPath, endNum):
    try : 
        for j in range(int(endNum/5)+1):
            for i in range (0,5):
                if i==0 and j==0:
                    #sttService.content2file(str((5 * j) + i) + "\n" + resultVector[i][j], filePath, True)
                    print("##########################################")
                    print("##########################################")
                    print("##########################################")
                    print("##########################################")
                    content2file(resultVector[i][j], textPath, True)
                    continue
                elif(j>len(resultVector[i])-1):
                    continue
                #sttService.content2file(str((5 * j) + i) + "\n" + resultVector[i][j], filePath, False)
                content2file(resultVector[i][j], textPath, False)

        # 저장 후 기존 Vector clear
        for j in range(0,5):
            audioPathVector[j].clear()
            resultVector[j].clear()
        
        audioPathVector.clear()
        resultVector.clear()
        return True
    except Exception as e:
        print(e)
        return False