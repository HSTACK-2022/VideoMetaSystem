# sceneText.py
#
# 추출된 이미지에서 글자를 추출합니다.
# 영상의 narrative와 presentation을 결정합니다.
# tensorflow를 이용하여 이미지를 N, L, P, A 4가지로 구분합니다.
# opencvService.py에 의해 호출됩니다.
# 
# uses
# - sceneText(imagePath, textPath) : 이미지에서 글자를 추출해 textPath에 저장
# - sceneSeperate(imagePath) : 추출된 장면들을 N, L, P, A로 구분 및 narrative, presentation 결정
#
#
# parameters
# - imagePath : 이미지 파일(장면)들이 저장된 경로
# 
# return
# - None.
# - 여기에서 추출된 keyword.txt와 keyword_line.txt를 바탕으로 키워드를 추출할 수도 있습니다.
# - 이 값을 opencvService.py에 전달해 narrative, presentation 값을 저장합니다. 


from . import calTime
from .config import OS
from .config import MODEL_DIR

from pykospacing import Spacing
from pyrsistent import CheckedKeyTypeError
from lib2to3 import pytree
import cv2
import pytesseract
import os
import numpy
import subprocess


keyword_list = []
checkIndexDup = []

def sceneText(imagePath, textPath):  
    global keyword_list
    global checkIndexDup
        
    # for encoding langs
    #sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8') 
    #sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    if OS == 'Windows':
        pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe" #[Minhwa]경로지정
        #pytesseract.pytesseract.tesseract_cmd = "E:/tools/Tesseract/tesseract.exe" #[Dayeon]경로지정
    config = ('-l eng+kor --oem 3 --psm 4')
    video_info = dict()

    count = 0
    typeCount = [0, 0, 0, 0]        #순서대로 L, N, PPT, A

    imageList = os.listdir(imagePath)
    for images in imageList:
        imageName = images.split(".jpg")[0]
        images = os.path.join(imagePath, images)
        print(images)

        # 이론, 실습을 체크해 이론인 경우에만 OCR
        if imageName.startswith("P"):
            typeCount[2] += 1
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

            save_file(img_string2, os.path.join(textPath, "keyword.txt"))
            save_file_2Line(time, img_string, os.path.join(textPath, "keyword_line.txt"))
            

            keyword_k = img_string.replace("\n", " ")
            keyword = spaceText(keyword_k)
            
            video_info[time] = keyword_list[count]
            count += 1
        
        elif imageName.startswith("A"):     typeCount[3] += 1
        elif imageName.startswith("N"):     typeCount[1] += 1
        elif imageName.startswith("L"):     typeCount[0] += 1

    dic = no_dup(video_info)   
    print(dic)
    keyword_list.clear
    checkIndexDup.clear

    #type에 따라 return값 변경
    maxIndex = numpy.argmax(typeCount)
    if maxIndex == 0:   return "L"
    elif maxIndex == 1: return "N"
    elif maxIndex == 2: return "P"
    elif maxIndex == 3: return "A"
    else:               return "E"

# 이론/실습 구분
def sceneSeperate(imagePath):
    print(MODEL_DIR)
    
    # call ImageSeperate function.
    result = subprocess.Popen(['python', MODEL_DIR, '-f', imagePath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    exitcode = result.returncode
    if exitcode != 0:
        print(exitcode, out.decode('utf-8-sig'), err.decode('utf-8-sig'))
    else:
        print('Completed')

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