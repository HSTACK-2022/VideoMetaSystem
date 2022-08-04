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
# - extBasicInfo(videoId) : 기본 metadata 추출
# - getImage(videoId) : 장면 추출
# - getPPTImage(videoId) : 각 장면에서 ppt / lecture인 경우만 추출
#
# parameters
# - videoId : DB Table들의 key로 쓰이는 video의 고유 id
# 
# return
# - True : 작업이 정상적으로 완료된 경우
# - False : 중간에 오류가 발생한 경우

import os
import cv2
from datetime import datetime

from .config import OS
from . import sceneText


def doOpencvService(fileURL, finalDic) :
    # create dirs
    imagePath = os.path.join(os.path.dirname(fileURL), 'Image')
    os.makedirs(imagePath, 0o777, True)
    os.chmod(imagePath, 0o777)

    getImage(fileURL, imagePath)
    sceneText.sceneSeperate(imagePath)
    type = sceneText.sceneText(imagePath, os.path.dirname(fileURL))
    
    # L, N, P, A
    # method : PPT, lecture / others
    # narrative : Application / others
    if type == "P" or type == "L":
        finalDic['method'] = 'PPT'
    else:
        finalDic['method'] = '실습'

    if type == "A":
        finalDic['narrative'] = 'Application'
    else:
        finalDic['narrative'] = 'Description'

    finalDic['imageAddr'] = imagePath


def getPPTImage(imagePath):
    pptImage = set()
    imageList = os.listdir(imagePath)
    print(imageList)

    for image in imageList:
        if image.startswith("L") or image.startswith("P"):
            imageSrc = os.path.join(imagePath, image)
            pptImage.add(imageSrc)
    
    return pptImage


import cv2
from cv2 import FORMATTER_FMT_NUMPY 
import numpy as np
import os

def getImage(fileURL, imagePath):
    global cap, totalFrameNum, fps, width, height

    cap = cv2.VideoCapture(fileURL)
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
            saveImage(imagePath, currFrame, 0)
            continue
        
        if (frameNum % fps == 0) :
            
            if not ret: break
                 
            #print("total : ", totalFrameNum , "frameNum : ", frameNum)
            psnrV = getPSNP(prevFrame, currFrame)
            # print("psnrV: ",psnrV)
            
            if psnrV < CHANGE_DETECT_AUDIO and psnrV > 0:
                changeFrame = currFrame.copy()
                saveImage(imagePath, changeFrame, frameNum / fps)
                
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