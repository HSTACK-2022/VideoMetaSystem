# extractMetadata.py
#
# 영상에서 메타데이터를 추출합니다.
# main.py에 의해 호출됩니다.
# 
# uses
# - extract(fileURL, finalDic) : 비디오 파일에서 메타데이터 추출
# - extBasicInfo(fileURL, finalDic) : 비디오 파일에서 FPS, 크기, 길이 등 기본 정보 추출
# 
# * extract() 호출시 나머지 함수 역시 호출됩니다.
#
# parameters
# - fileURL : 비디오 파일이 저장된 경로
# - finalDic : 메타데이터가 저장될 딕셔너리
#
# return
# - finalDic : 영상의 메타데이터를 넣어 반환합니다.


import os
import cv2
import threading

from . import calTime
from . import sttService
from . import opencvService
from . import keywordService
from . import categoryService
from . import indexingService

def extract(title, presenter, fileURL):
    try:
        totalDic = dict()
        totalDic['title'] = title
        totalDic['presenter'] = presenter
        totalDic['videoAddr'] = fileURL

        threads = []

        basic = threading.Thread(target=extBasicInfo, args=(fileURL, totalDic))
        audio = threading.Thread(target=sttService.doSttService, args=(fileURL, totalDic))
        image = threading.Thread(target=opencvService.doOpencvService, args=(fileURL, totalDic))

        basic.start()
        audio.start()
        image.start()

        threads.append(basic)
        threads.append(audio)
        threads.append(image)

        for t in threads:
            t.join()

        keywordService.doKeywordService(fileURL, totalDic)

        category = threading.Thread(target=categoryService.extractCategory, args=(fileURL, totalDic))
        indexing = threading.Thread(target=indexingService.doIndexingService, args=(fileURL, totalDic))

        category.start()
        indexing.start()

        threads.append(category)
        threads.append(indexing)

        for t in threads:
            t.join()

        print(totalDic)
        return totalDic
        
    except Exception as e:
        print(e)
        print("### extractMetaData : ERROR!! ###")
        return False


# fileURL를 받아 기본 정보 저장
def extBasicInfo(fileURL, finalDic) :    
    cap = cv2.VideoCapture(fileURL)
    wFrame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hFrame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))

    finalDic['videoLength'] = calTime.calSec2Time(length)
    finalDic['videoFrame'] = str('%d*%d' %(wFrame, hFrame))
    finalDic['videoSize'] = str(os.path.getsize(fileURL))
    finalDic['videoType'] = str(os.path.splitext(fileURL)[1])