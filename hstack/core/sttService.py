# sttService.py
# 음원 파일을 sec단위로 분할, STT API로 전송합니다.
# 
# call : doSttService(videoId)
# return : textFilePath
# videoId : VideoPath, Metadata에 공통으로 사용되는 key (id)
# 
# STT KEY는 secrets.json에 저장되어 있습니다.

import os
import math
import json
import base64
import urllib3
import platform
import threading
import subprocess

from pathlib import Path
from mutagen.wave import WAVE
from http.client import HTTPConnection, ImproperConnectionState
from urllib.error import HTTPError
from core import audioService
from . import models

# 상수 설정
OS = platform.system()

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
languageCode = "korean"
audioContents = None
audioFile = None

# API KEY 설정
def initSttService():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    secretFile = os.path.join(BASE_DIR, 'secrets.json')
    with open(secretFile) as f:
        secrets = json.loads(f.read())

    def get_secret(setting, secrets=secrets):
        try:
            return secrets[setting]
        except KeyError:
            error_msg = "Set the {} environment variable".format(setting)
            raise ImproperConnectionState(error_msg)

    return get_secret("STT_API_KEY")


# 파일의 경로를 받아 음원을 추출하고 텍스트파일로 바꾼다.
def doSttService(videoId):
    global accessKey
    accessKey = initSttService()

    audioFilePath = audioService.getFullAudioFile(videoId)
    print(audioFilePath)
    
    if audioFilePath!=None:
        successed = splitAudio(audioFilePath, 10)
        if successed != None :
            sttResult = pcm2text(successed)
            return sttResult
    else:
        return False

# Audio를 조각낸다.
def splitAudio(audioFilePath, sec):
    audioLen = WAVE(audioFilePath).info.length              #파일의 전체 길이 알아오기
    audioName = os.path.basename(audioFilePath).split('.')[0]    # 파일의 이름만 가져오기 - test.wav 이면 test만
    os.mkdir(os.path.dirname(audioFilePath) + "/" + audioName)

    if OS == "Windows" :
        audioPath = os.path.dirname(audioFilePath).replace("/", "\\") + "\\" + audioName + "\\"
    else :
        audioPath = os.path.dirname(audioFilePath) + "/" + audioName + "/"

    count = 0
    for i in range(0, math.ceil(audioLen), 10):
        startTime = 0 if (i == 0) else (i + 1)
        endTime = audioLen if (i + 10 > audioLen) else (i + 10)
        #newAudioFilePath = audioPath + audioName + str(count) + ".wav"
        newAudioFilePath = audioPath + str(count) + ".wav"

        result = subprocess.Popen(
            ['ffmpeg', '-i', audioFilePath, '-ss', str(startTime), '-t', str(sec),
            '-acodec', 'copy', newAudioFilePath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = result.communicate()
        exitcode = result.returncode
        if exitcode != 0:
            print(exitcode, out.decode('utf8'), err.decode('utf8'))
            return None
        else:
            print('%d Completed' %count)

        count+=1

    return audioPath

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
    f = open(filePath, "a", encoding="UTF-8-sig")
    	
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
def pcm2text(audioFilePath) : 
    if OS == "Windows" : 
        FILE_DIR = os.path.dirname(audioFilePath).replace("/", "\\").split('\\Audio')[0]
        fileName = Path(audioFilePath).stem + ".txt"
        textPath = FILE_DIR + "\\Text\\" + fileName
    else :
        FILE_DIR = os.path.dirname(audioFilePath).split('/Audio')[0]
        fileName = Path(audioFilePath).stem + ".txt"
        textPath = FILE_DIR + "/Text/" + fileName

    print('****************************************')
    print(FILE_DIR)

    endNum = len(os.listdir(audioFilePath))

    if sttAsync(audioFilePath, endNum) == True :
        if resultFileWrite(textPath, endNum) == True :
            return textPath
    return False

# 비동기적으로 pcm 파일을 text로 변환한다.
def sttAsync(audioPath, endNum):
    for i in range(0, endNum):
        if i%5 == 0:
            audioPath_0.append(audioPath+str(i)+".wav")
        elif i%5 == 1:
            audioPath_1.append(audioPath+str(i)+".wav")
        elif i%5 == 2:
            audioPath_2.append(audioPath+str(i)+".wav")
        elif i%5 == 3:
            audioPath_3.append(audioPath+str(i)+".wav")
        elif i%5 == 4:
            audioPath_4.append(audioPath+str(i)+".wav")
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
        threadResult.append(audio2text(threadAudioPath[i],num)) # num -> keyNum
        # result of Pcm2Text = new Pcm2Text().pcm2text(String.valueOf(audioPath.get(i)),keys[number]
        # print("@@@@" + str(resultVector))

# thread 결과물 textPath에 저장
def resultFileWrite(textPath, endNum):
    try : 
        for j in range(int(endNum/5)+1):
            for i in range (0,5):
                if i==0 and j==0:
                    #sttService.content2file(str((5 * j) + i) + "\n" + resultVector[i][j], filePath, True)
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