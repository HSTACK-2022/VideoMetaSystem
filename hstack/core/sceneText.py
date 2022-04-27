# sceneText.py
#
# 추출된 이미지에서 글자를 추출합니다.
# 
# uses
# - sceneText(videoId)
#
# parameters
# - videoId : DB Table들의 key로 쓰이는 video의 고유 id
# 
# return
# - None.
# - 추후 DB의 videopath.imageaddr/keyword.txt, keyword_line.txt를 이용, 키워드를 추출해 낼 수 있습니다.


from . import models
from . import calTime

from pykospacing import Spacing
from pyrsistent import CheckedKeyTypeError
from lib2to3 import pytree
import cv2
import pytesseract
import sys
import io
import os
import math
import subprocess

keyword_list = []
checkIndexDup = []

def sceneText(videoId):  
    videopath = models.Videopath.objects.get(id=videoId)
    dbimagepath = videopath.imageaddr
    imagepath = os.listdir(videopath.imageaddr)
    print(imagepath)

    global keyword_list
    global checkIndexDup
        
    # for encoding langs
    #sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8') 
    #sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    pytesseract.pytesseract.tesseract_cmd = "E:/tools/Tesseract/tesseract.exe"
    config = ('-l eng+kor --oem 3 --psm 4')
    video_info = dict()

    count = 0
    pCount = 0
    tCount = 0

    #test code
    for images in imagepath:
        imageName = images.split(".jpg")[0]
        images = os.path.join(dbimagepath, images)

        # 이론, 실습을 체크해 이론인 경우에만 OCR
        if imageName.startswith("P"):
            pCount += 1
            #img = cv2.imread(sceneCutter.imgName[i], cv2.IMREAD_COLOR)
            img = cv2.imread(images, cv2.IMREAD_COLOR)
            img_gray = gray_scale(img)
            img_threshold = image_threshold(img_gray)
            img_range = range_scale(img_threshold)
            img_string = pytesseract.image_to_string(img_range,config=config)
            img_string2 = pytesseract.image_to_string(img_threshold,config=config)

            #time = changeTime(sceneCutter.videoTime[i])
            imageName = imageName.split("P")[1]
            print("time : ", imageName)
            time = calTime.calSec2Time(int(imageName))

            save_file(img_string2, os.path.join(dbimagepath, "keyword.txt"))
            save_file_2Line(time, img_string, os.path.join(dbimagepath, "keyword_line.txt"))
            

            keyword_k = img_string.replace("\n", " ")
            keyword = spaceText(keyword_k)
            
            video_info[time] = keyword_list[count]
            count += 1
        
        else :
            tCount += 1

    dic = no_dup(video_info)   
    print(dic)
    keyword_list.clear
    checkIndexDup.clear

    if pCount > tCount:
        return "P"
    elif pCount < tCount:
        return "T"

def gray_scale(image):
    result = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    return result

def image_threshold(image):
    ret, result = cv2.threshold(image,172 ,255, cv2.THRESH_BINARY)
    return result

def range_scale(image):
    h,w = image.shape
    result = image[0:140, 0:w]
    # cv2.rectangle(result, (0,0),(100-1,w-1),(0,255,0))
    # cv2.imshow("roi",result)
    # cv2.waitKey(0)
    return result
    
def save_file(text, path):
    fix_text = spaceText(text)
    f = open(path,'a',encoding='UTF-8-sig')
    f.write(fix_text+"\n")
    f.close()

# 띄어쓰기 교정
def spaceText(text):
    fixed_text = text.replace(" ","") # 띄어쓰기가 없는 문장 임의로 만들기
    spacing = Spacing()
    kospacing_text = spacing(fixed_text) # 띄어쓰기 문법 수정
    return kospacing_text

# 키워드 추출 text 저장
def save_file_2Line(time, text, path):
    global keyword, keyword_list, checkIndexDup
    list=text.split('\n')
    
    if(len(list)==1):
        if(len(list[0])>=10):
            pass
        else:
            keyword = list[0]
    elif (len(list)==2):
        if(len(list[0])>=10):
            keyword = list[1]
        elif(len(list[1])>=10):
            keyword = list[0]
        else:
            keyword = list[0]+list[1]
    else:
        if(len(list[0])>=10):
            keyword = list[1]
        if(len(list[1])>=10):
            keyword = list[0]
        if(len(list[2])>=10):
            keyword = list[0]+list[1]
        else:
            keyword = list[0]+list[1]+list[2]
    # keyword = list[0]+list[1]+list[2]
    
  
    print(keyword)
    
    spacing = spaceText(keyword)
    keyword_list.append(spacing)
    count = len(checkIndexDup)
    countIndex = 0
    print(count)

    for index in checkIndexDup :
        if index == spacing : 
            break
        else:
            countIndex += 1

    if count == countIndex:
        checkIndexDup.append(spacing)
        f = open(path, 'a', encoding='UTF-8-sig')
        f.write(time + ' :: ' + spacing+"\n")
        f.close()

def no_dup(my_dict):
    seen = []
    result = dict()
    for key, val in my_dict.items():
        if val not in seen:
            seen.append(val)
            result[key] = val
    return result


# 이론/실습 구분
def sceneSeperate(videoId):
    videopath = models.Videopath.objects.get(id=videoId)
    imagepath = videopath.imageaddr

    modelPath = os.path.join(os.getcwd(), "tensorflow\\ImageSeperate\\test.py")
    
    #>python tensorflow\ImageSeperate\test.py -f dirname
    result = subprocess.Popen(['python', modelPath, '-f', imagepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    exitcode = result.returncode
    if exitcode != 0:
        print(exitcode, out.decode('utf8'), err.decode('utf8'))
    else:
        print('Completed')