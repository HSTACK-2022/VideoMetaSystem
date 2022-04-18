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