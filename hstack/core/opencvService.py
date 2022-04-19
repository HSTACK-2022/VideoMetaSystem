# opencvService.py
#
# opencv를 이용해 video에서 기본적인 metadata들을 추출합니다.
# - type
# - frame
# - size (bytes)
# - length (HH:MM:SS)
# 
# uses
# - extBasicInfo(videoId)
#
# parameters
# - videoId : DB Table들의 key로 쓰이는 video의 고유 id
# 
# return
# - True : 작업이 정상적으로 완료된 경우
# - False : 중간에 오류가 발생한 경우


import os
import cv2
import platform

from . import models
from . import getRealPath
from datetime import datetime

# 상수 설정
OS = platform.system()

# videoId를 받아 기본 정보 저장
def extBasicInfo(videoId) :
    videoPath = models.Videopath.objects.get(id = videoId).videoaddr

    #비디오 파일을 받아 오디오 파일로 바꾼다.
    WORK_DIR = getRealPath.getRealDirPath(videoPath)

    if OS == "Windows" : 
        videoName = os.path.basename(videoPath).replace("/", "\\")
        videoPath = WORK_DIR + videoName 
    else : 
        videoName = os.path.basename(videoPath)
        videoPath = WORK_DIR + videoName 
    
    cap = cv2.VideoCapture(videoPath)
    wFrame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hFrame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))
    size = os.path.getsize(videoPath)
    type = os.path.splitext(videoPath)[1]

    try :
        models.Metadata.objects.filter(id = videoId).update(
            videolength = calSec2Time(length),
            videoframe = str('%d*%d' %(wFrame, hFrame)),
            videosize = str(size),
            videotype = str(type)
        )
        return True
    except Exception as e :
        print(e)
        return False


def calSec2Time(sec):
    hour = sec // 3600
    sec -= hour * 3600
    min = sec // 60
    sec -= min  * 60
    dateStr = str('%d:%d:%d' %(hour, min, sec))
    dateRes = datetime.strptime(dateStr, '%H:%M:%S')
    
    return dateRes