# opencvService.py
#
# opencv를 이용해 영상에서 장면을 추출합니다.
# tensorflow를 이용하여 이미지를 N, L, P, A 4가지로 구분합니다.
# extractMetadata.py에 의해 호출됩니다.
# 
# uses
# - doOpencvService(fileURL, finalDic) : 영상에서 장면 추출 및 구분
# - getImage(fileURL, imagePath) : 영상에서 장면을 추출하여 imagePath에 저장
# - saveImage(dirpath, res, sec) : res값을 해당 장면이 등장한 시간(sec)와 함께 dirpath에 저장 (ex: 0.jpg -> 0초에 나온 장면)
# - getPSNP(I1, I2) : 두 이미지 I1, I2의 차이 값 (PSNR)을 구함
#
# parameters
# - fileURL : 비디오 파일이 저장된 경로
# - finalDic : 이미지의 경로와 Narrative, Presentation을 저장할 딕셔너리
# 
# return
# - totalDic : 카테고리의 종류와 확률을 넣어 반환합니다.

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
    # presentation : PPT, lecture / others
    # narrative : Application / others
    if type == "P" or type == "L":
        finalDic['presentation'] = 'Static'
    else:
        finalDic['presentation'] = 'Dynamic'

    if type == "A":
        finalDic['narrative'] = 'Application'
    else:
        finalDic['narrative'] = 'Description'

    finalDic['imageAddr'] = imagePath


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