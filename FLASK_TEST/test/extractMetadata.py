# extractMetadata.py
#
# video를 통해 metadata를 추출합니다.
# 

import os
import cv2
import threading
import background as bg

from test import calTime
from test import sttService
from test import opencvService

@bg.task
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

        print(totalDic)
        return True
        
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