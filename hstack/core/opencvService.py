# opencvService.py
#
# opencv를 이용해 video에서 기본적인 metadata들을 추출합니다.
# 비디오에서 장면추출을 할 수 있습니다.
# - type
# - frame
# - size (bytes)
# - length (HH:MM:SS)
# 
# uses
# - extBasicInfo(videoId)
# - getImage(videoId)
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
from . import sceneText

from . import models
from . import calTime
from datetime import datetime


# 상수 설정
OS = platform.system()

# videoId를 받아 기본 정보 저장
def extBasicInfo(videoId) :
    videoPath = models.Videopath.objects.get(id = videoId).videoaddr
    
    #ffmpeg -i algo.mp4 2>&1 | find "Duration"
    cap = cv2.VideoCapture(videoPath)
    wFrame = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    hFrame = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS))
    size = os.path.getsize(videoPath)
    type = os.path.splitext(videoPath)[1]

    print(wFrame, hFrame, length, size, type)

    try :
        models.Metadata.objects.filter(id = videoId).update(
            videolength = datetime.strptime(calTime.calSec2Time(length), '%H:%M:%S'),
            videoframe = str('%d*%d' %(wFrame, hFrame)),
            videosize = str(size),
            videotype = str(type)
        )
        return True
    except Exception as e :
        print(e)
        return False

def doOpencvService(videoId) :
    videoPathObj = models.Videopath.objects.get(id=videoId)     #DB에서 videoId에 해당하는 객체를 가져옴
    videoFilePath = videoPathObj.videoaddr              #DB에서 videoAddr 추출
    videoName = os.path.basename(videoFilePath).replace("/", "\\").split('.')[0]

    if OS == "Windows" : 
        imagePath = videoFilePath.split('Video\\')[0] + "Image\\" + videoName
    else : 
        imagePath = videoFilePath.split('Video/')[0] + "Image/" + videoName

    os.mkdir(imagePath)
    models.Videopath.objects.filter(id=videoId).update(imageaddr = imagePath)

    getImage(videoId)
    sceneText.sceneSeperate(videoId)
    method = sceneText.sceneText(videoId)

    if method == "P":
        models.Metadata.objects.filter(id=videoId).update(method="PPT")
    else:
        models.Metadata.objects.filter(id=videoId).update(method="실습")


from . import models

import cv2
from cv2 import FORMATTER_FMT_NUMPY 
import numpy as np
import os

def getImage(videoId):
    global cap, totalFrameNum, fps, width, height

    videopath = models.Videopath.objects.get(id=videoId)
    imagepath = videopath.imageaddr
    cap = cv2.VideoCapture(videopath.videoaddr)
    totalFrameNum = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))    # 초당 프레임 수 
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 프레임 너비
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))    # 프레임 높이

    frameNum = -1
    psnrV = 0 
    CHANGE_DETECT_AUDIO = 15.0
    
    prevFrame = np.zeros((height,width,3), np.uint8)
    currFrame = np.zeros((height,width,3), np.uint8)
    changeFrame =np.zeros((height,width,3), np.uint8)

    print(cap.isOpened())
    
    while(cap.isOpened()):
        frameNum+=1
        ret, img = cap.read(currFrame)
        
        if frameNum < 1:
            prevFrame = currFrame.copy()
            changeFrame = currFrame.copy()
            saveImage(imagepath, currFrame, 0)
            continue
        
        if (frameNum % fps == 0) :
            
            if not ret: break
                 
            #print("total : ", totalFrameNum , "frameNum : ", frameNum)
            psnrV = getPSNP(prevFrame, currFrame)
            # print("psnrV: ",psnrV)
            
            if psnrV < CHANGE_DETECT_AUDIO and psnrV > 0:
                changeFrame = currFrame.copy()
                saveImage(imagepath, changeFrame, frameNum / fps)
                
            prevFrame = currFrame.copy()         
            
def saveImage(dirpath, res, sec):
    path = os.path.join(dirpath, "%d.jpg" %sec)  # 이미지 저장 경로 변경 필요
    print(path)
    #print(path, end=" ** ")
    #imgName.append(path)
    #videoTime.append(sec)
    bool = cv2.imwrite(path, res)
    print(bool)

def getPSNP(I1, I2):
    s1 = np.zeros((I1.shape[0],I2.shape[1],3), np.uint8)
    
    diff = cv2.absdiff(I1,I2,s1)
    s1 = np.float32(s1)
    s1 = cv2.multiply(s1,s1)
    
    s1_h = s1.shape[0]
    s1_w = s1.shape[1]
    s1_bpp = s1.shape[2]
    
    s=cv2.sumElems(s1)
    ## i dont know...
    sse = s[0] + s[1] +s[2]
    #print("sse : ",sse)
    
    if sse <= 1e-10 :
        return 0
    
    mse = sse / np.double(3 * width * height)
    psnr = 10.0 * np.log10((255*255)/mse)
    
    return psnr