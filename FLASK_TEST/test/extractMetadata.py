# extractMetadata.py
#
# video를 통해 metadata를 추출합니다.
# 


# Api calls
from flask import request
from flask import current_app as app # app.config 사용을 위함
from flask_restx import Resource, Namespace

import os
from urllib.parse import urlparse
from werkzeug.utils import secure_filename

Upload = Namespace('Upload')

@Upload.route('/upload')
class ExtractMetadata(Resource):
    def post(self):
        content_type = request.headers.get('Content-Type')
        fileTitle = request.form.get("title")
        filePresenter = request.form.get("presenter")
        uploadedFile = request.files["videoFile"]

        # if filename Duplicates
        uploadName = secure_filename(uploadedFile.filename)
        fileDirPath = os.path.join(app.config.get('UPLOAD_FILE_DIR'), uploadName.split('.')[0])
        dupNum = 1
        while os.path.exists(fileDirPath):
            splitedName = uploadName.split('.')
            uploadName = splitedName[0] + "_" + str(dupNum) + '.' + splitedName[1]
            dupNum += 1
            fileDirPath = os.path.join(app.config.get('UPLOAD_FILE_DIR'), uploadName.split('.')[0])

        os.makedirs(fileDirPath, 777, True)
        os.chmod(fileDirPath, 0o777)
        uploadURL = os.path.join(fileDirPath, uploadName)
        uploadedFile.save(uploadURL)
        
        totalDic = extract(fileTitle, filePresenter, uploadURL)
        return totalDic




# Todo Works
import os
import cv2
import threading
import background as bg

from test import calTime
from test import sttService
from test import opencvService
from test import keywordService
from test import categoryService
from test import indexingService

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