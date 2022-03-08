import os
import json
import base64
import requests

from pathlib import Path
from http.client import HTTPConnection
from urllib.error import HTTPError

# 상수 설정
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
languageCode = "korean"
audioContents = None
accessKey = ["2d40b072-37f1-4317-9899-33e0b3f5fb90","80ff5736-f813-4686-aca6-472739d8ebe0","25833dd1-e685-4f13-adc6-c85341d1bac5",
            "40c498a8-7d33-4909-9b60-427b3d0ccf8b", "0913ccd7-0cd1-4455-8b60-7940aa54f7be"]

# 파일의 경로를 받아 텍스트파일로 바꾼다.
def doSttService(audioFilePath):
    # 지금은 임시로 파일명을 저장했지만
    # 나중에는 audioFile을 자신의 DB에 저장해두고 그 key값에 맞게 txt 파일 이름을 지정해야 할 것.
    #filePath = rootFilePath + "test" + ".txt"
    sttResult = audio2text(audioFilePath, 0)
    #res2file = content2file(sttResult, filePath, True)
    	
    return sttResult

    
# AudioPath를 주면 STT 작업을 해서 뱉는다.
def audio2text(audioFilePath, i) :
    result = None

    #audioFile 추출
    try :
        BASE_DIR = os.getcwd().replace("/", "\\")
        FILE_DIR = os.path.dirname(audioFilePath).replace("/", "\\")
        FILE_NAME = os.path.basename(audioFilePath).replace("/", "\\")
        path = BASE_DIR + FILE_DIR + "\\" + FILE_NAME
        file = open(path, 'rb')
        audioBytes = bytearray(file.read())
        #byte[] audioBytes = Files.readAllBytes(path)
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

'''
# Stream을 읽어오는 코드
def readStream(in) :
        StringBuilder sb = new StringBuilder()
        BufferedReader r = new BufferedReader(new InputStreamReader(in),1000)
        for (String line = r.readLine(); line != null; line =r.readLine()) :
            sb.append(line)
        in.close()
        return sb.toString()
'''
    
# Contents와 FilePath를 주면 파일에 적어서 뱉는다.
def content2file(contents, filePath, isFirst):
    f = open(filePath, "a")
    	
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