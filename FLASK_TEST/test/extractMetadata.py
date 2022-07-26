# extractMetadata.py
#
# video를 통해 metadata를 추출합니다.
# 

from flask import current_app as app # app.config 사용을 위함

import os
import cv2
import platform

from . import calTime
from . import sttService


def extract(title, presenter, fileURL):
    totalDic = dict()
    totalDic['title'] = title
    totalDic['presenter'] = presenter
    totalDic['videoAddr'] = fileURL

    # 기본 정보 추출
    basicDic = extBasicInfo(fileURL)
    print(basicDic)

    # Audio 추출
    audioDic = sttService.doSttService(fileURL)
    print(audioDic)



# fileURL를 받아 기본 정보 저장
def extBasicInfo(fileURL) :    
    #ffmpeg -i algo.mp4 2>&1 | find "Duration"
    print(fileURL)
    resDic = dict()

    cap = cv2.VideoCapture(fileURL)
    wFrame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hFrame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))

    resDic['videoLength'] = calTime.calSec2Time(length)
    resDic['videoFrame'] = str('%d*%d' %(wFrame, hFrame))
    resDic['videoSize'] = str(os.path.getsize(fileURL))
    resDic['videoType'] = str(os.path.splitext(fileURL)[1])

    return resDic