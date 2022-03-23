import os
import math
import json
import base64
import requests
import threading
import subprocess

from pathlib import Path
from mutagen.wave import WAVE
from http.client import HTTPConnection
from urllib.error import HTTPError
from asyncio.windows_events import NULL

# 상수 설정
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
languageCode = "korean"
audioContents = None
accessKey = ["2d40b072-37f1-4317-9899-33e0b3f5fb90","80ff5736-f813-4686-aca6-472739d8ebe0","25833dd1-e685-4f13-adc6-c85341d1bac5",
            "40c498a8-7d33-4909-9b60-427b3d0ccf8b", "0913ccd7-0cd1-4455-8b60-7940aa54f7be"]

audioFile = None
isAudioExt = False

# 파일의 경로를 받아 음원을 추출하고 텍스트파일로 바꾼다.
def doSttService(videoFilePath):
    # 지금은 임시로 파일명을 저장했지만
    # 나중에는 audioFile을 자신의 DB에 저장해두고 그 key값에 맞게 txt 파일 이름을 지정해야 할 것.
    #filePath = rootFilePath + "test" + ".txt"
    audioFilePath = video2audio(videoFilePath)
    isAudioExt = True

    successed = splitAudio(audioFilePath, 10)
    if successed != None :
        sttResult = pcm2text(successed)
        return sttResult

    else :
        return None

# 통 오디오 파일을 받아오는 함수
def getFullAudioFile():
    if isAudioExt:
        return audioFile
    else :
        return None


#상대경로를 절대경로로 변환하는 함수
def getRealDirPath(path):
    BASE_DIR = os.getcwd().replace("/", "\\")
    FILE_DIR = os.path.dirname(path).replace("/", "\\")
    path = BASE_DIR + FILE_DIR + "\\"
    return path


#비디오 파일을 받아 오디오 파일로 바꾼다.
def video2audio(videoFilePath):
    WORK_DIR = getRealDirPath(videoFilePath)
    videoName = os.path.basename(videoFilePath).replace("/", "\\")
    audioName = videoName.split('.')[0] + ".wav"
    videoPath = WORK_DIR + videoName 
    audioPath = WORK_DIR.split('Video\\')[0] + "Audio\\" + audioName

    #Sampling rate:16000 / mono channel 
    result = subprocess.Popen(['ffmpeg', '-y',
        '-i', videoPath, '-vn', '-acodec', 'pcm_s16le', '-ar', '16k', '-ac', '1', '-ab', '128k', audioPath],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    exitcode = result.returncode
    if exitcode != 0:
        print(exitcode, out.decode('utf8'), err.decode('utf8'))
    else:
        print('Completed')

    return audioPath


# Audio를 조각낸다.
def splitAudio(audioFilePath, sec):
    audioLen = WAVE(audioFilePath).info.length              #파일의 전체 길이 알아오기

    # 파일의 이름만 가져오기 - E:/2022_CAPSTONE/test.wav 이면 test만 추출
    audioName = os.path.basename(audioFilePath).split('.')[0]

    os.mkdir(os.path.dirname(audioFilePath) + "/" + audioName)
    audioPath = os.path.dirname(audioFilePath).replace("/", "\\") + "\\" + audioName + "\\"

    count = 0
    for i in range(0, math.ceil(audioLen), 10):
        startTime = 0 if (i == 0) else (i + 1)
        endTime = audioLen if (i + 10 > audioLen) else (i + 10)
        #newAudioFilePath = audioPath + audioName + str(count) + ".wav"
        newAudioFilePath = audioPath + str(count) + ".wav"

        result = subprocess.Popen(
            ['ffmpeg', '-i', audioFilePath, '-ss', str(startTime), '-t', str(endTime),
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

    #audioFile 추출
    try :
        file = open(audioFilePath, 'rb')
        audioBytes = bytearray(file.read())
        audioContents = base64.b64encode(audioBytes).decode('utf8')
    except IOError as e :
        e.printStackTrace()

    #header, body 작성
    header = {'Content-Type' : 'application/json', 'charset' : 'UTF-8'}
    argument = {"language_code" : languageCode, "audio" : audioContents}
    body = {"access_key" : accessKey[i], "argument" : argument}
 
    url = None
    responseCode : int = None
    responBody : str = None

    try :
        response = requests.post(openApiURL, headers = header, data=json.dumps(body))
        response.raise_for_status       #오류 발생시 예외 발생
            
        responseCode = response.status_code 
        if (responseCode == 200) :
            responBody = response.json()["return_object"]['recognized']
            print(responBody)
            result = responBody
        else :
            result = "ERROR: " + str(responseCode)
 
    except HTTPError as e :
        e.printStackTrace()
    except IOError as e : 
        e.printStackTrace()
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
def pcm2text(audioFilePath) : 
    FILE_DIR = os.path.dirname(audioFilePath).replace("/", "\\").split('\\Audio')[0]
    from pathlib import Path
    fileName = Path(audioFilePath).stem + ".txt"
    #audioName = os.path.basename(audioFilePath).replace("/", "\\")
    #textName = audioName.split('.')[0] + ".txt"
    textPath = FILE_DIR + "\\Text\\" + fileName
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
        # result of Pcm2Text = 
            # new Pcm2Text().pcm2text(String.valueOf(audioPath.get(i)),keys[number]
        print("@@@@" + str(resultVector))

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
        return True
    except Exception as e:
        print(e)
        return False
