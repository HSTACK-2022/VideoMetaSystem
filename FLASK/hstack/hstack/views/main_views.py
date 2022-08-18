from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import current_app as app # app.config 사용을 위함

import pymysql
from sqlalchemy import exc

from hstack import searchAll
from hstack.config import DB
from hstack.models import Videopath
from hstack.models import Metadatum
from hstack.models import Keyword
from hstack.models import Timestamp

from datetime import datetime

import os
import requests
import background

from werkzeug.utils import secure_filename

# 상수 설정
bp = Blueprint('main', __name__, url_prefix='/')


# send to uploadAPI
#@background.task
def send2API(title, presenter, password, uploadURL):
    # API로 request
    reqUrl = 'http://127.0.0.1:8000/upload'
    data = {'title' : title, 'presenter' : presenter, 'uploadURL' : uploadURL}
    res = requests.post(reqUrl, data=data)
    res.apparent_encoding
    print(res.encoding)
    print(res.text)
    print("password for Editing : " + password)

    if (res.status_code == 200):
        jsonData = res.json()

        # DB 저장
        videoPath = Videopath(
            title = jsonData["title"],
            videoAddr = jsonData["videoAddr"],
            audioAddr = jsonData["audioAddr"],
            textAddr = jsonData["textAddr"],
            imageAddr = jsonData["imageAddr"],
            extracted = 2,
            password = password
        )
        
        DB.session.add(videoPath)
        DB.session.commit()
        
        id = videoPath.id

        category = ""
        categoryPerc = ""
        for c in jsonData["category"]:
            category += (c + ", ")
            categoryPerc += ((str)(round(jsonData["category"][c], 3)) + ", ")

        metadata = Metadatum(
            id = id,
            title = jsonData["title"],
            presenter = jsonData["presenter"],
            category = category[0:-2],
            category_percent = categoryPerc[0:-2],
            narrative = jsonData["narrative"],
            method = jsonData["method"],
            videoLength = jsonData["videoLength"],
            videoFrame = jsonData["videoFrame"],
            videoSize = jsonData["videoSize"],
            videoType = jsonData["videoType"],
            uploadDate = datetime.now().date()
        )
        DB.session.add(metadata)
        DB.session.commit()

        for key in jsonData["keyword"]:
            k = Keyword(
                id = id,
                keyword = key,
                percent = float(jsonData["keyword"][key]),
                expose = 1,
                sysdef = 1
            )
            DB.session.add(k)
            DB.session.flush()

        for time in jsonData["index"]:
            i = Timestamp(
                id = id,
                time = time,
                subtitle = jsonData["index"][time],
                expose = 1,
                sysdef = 1
            )
            DB.session.add(i)
            DB.session.flush()

        DB.session.commit()


@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/uploadFile/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == "POST":
        existError = {}
        fileTitle = request.form.get("title")
        filePresenter = request.form.get("presenter")
        password = request.form.get("password")
        uploadedFile = request.files["videoFile"]

        if (fileTitle == ""):
            existError['nameError'] = "영상 제목을 입력해주세요."
        if (filePresenter == ""):
            existError['presenterError'] = "영상 소유자를 입력해주세요."
        if (password == ""):
            existError['passwordError'] = "파일 수정을 위한 비밀번호를 입력해주세요."
        if (secure_filename(uploadedFile.filename) == ""):
            existError['fileError'] = "영상 파일을 첨부해주세요."

        if existError:
            return render_template('upload.html', error=existError)

        # save Video
        
        # if filename Duplicates
        uploadName = secure_filename(uploadedFile.filename)
        fileDirPath = os.path.join(app.config.get('UPLOAD_FILE_DIR'), uploadName.split('.')[0])
        dupNum = 1
        while os.path.exists(fileDirPath):
            splitedName = uploadName.split('.')
            uploadName = splitedName[0] + str(dupNum) + '.' + splitedName[1]
            dupNum += 1
            fileDirPath = os.path.join(app.config.get('UPLOAD_FILE_DIR'), uploadName.split('.')[0])

        os.makedirs(fileDirPath, 777, True)
        os.chmod(fileDirPath, 0o777)
        uploadURL = os.path.join(fileDirPath, uploadName)
        uploadedFile.save(uploadURL)

        # API로 request
        send2API(fileTitle, filePresenter, password, uploadURL)
        
        return redirect(url_for('main.home'))
                        
    return render_template('upload.html', error="")


@bp.route('/uploadFile/lists', methods=['GET', 'POST'])
def uploadList():
    if request.method == "GET":
        videoPathList = Videopath.query.filter(Videopath.extracted == True).all()
        videoIdList = list()
        for videopath in videoPathList:
            videoIdList.append(videopath.id)
        
        categoryList = searchAll.extractCategories(videoIdList)
        typeList = searchAll.extractType(videoIdList)
        dataList = searchAll.extractData(videoIdList)
        
        videoMetaList = list()
        for i in videoIdList: # (resultVideoIDList)에 저장되어 있는 id로 메타데이터 가져옴
            videoMetaList.append(searchAll.Total().getVideoMetadataFromID(i))

        print("********************")
        print(videoIdList)
        print(categoryList)
        print(videoMetaList)

        if not videoIdList :
            return render_template('uploadLists.html', code = 404)
        else :
            return render_template('uploadLists.html',
                code = 200,
                categoryList = categoryList,
                typeList = typeList,
                dataList = dataList,
                videoMetaList = videoMetaList,
                videoIdList = videoIdList
            )
    else:
        # 이하 detailSearch : 수정필요
        '''
        # POST인 경우에는 Category, Type, Method 등 필터가 있다.
        # 현재 videoIdList를 받아 필터링 후 return
        stringvideoIdList = request.POST['videoIdList']
        search_type = request.POST['search_type']   # category, method, narrative
        search_detail_type = request.POST['search_detail_type'] # IT, 지리, 식물, ...

        # 첫 filtering은 Queryset으로 온다. <Queryset ~~~ > 에서 ~~~만 나오도록. 흡사 list 출력 형태.
        if stringvideoIdList.startswith("<QuerySet"):
            videoIdList = stringvideoIdList[10:-1]
        else:
            videoIdList = stringvideoIdList

        videoIdList = re.split(r'[ \[\],\']', videoIdList)
        newVideoIdList = list()

        for videoId in videoIdList:
            if videoId != "":
                filterQ = Q()
                filterQ &= Q(id = videoId)
                if search_type == "category" :  filterQ &= Q(category__contains = search_detail_type)
                if search_type == "narrative" : filterQ &= Q(narrative = search_detail_type)
                if search_type == "method" :    filterQ &= Q(method = search_detail_type)
                if (not not models.Metadata.objects.filter(filterQ)) :
                    newVideoIdList.append(videoId)

        categoryList = searchAll.extractCategories(newVideoIdList)
        typeList = searchAll.extractType(newVideoIdList)
        dataList = searchAll.extractData(newVideoIdList) 
        newVideoMetaList = list()
        for i in newVideoIdList:         # (newVideoIdList)에 저장되어 있는 id로 메타데이터 가져옴
            newVideoMetaList.append(searchAll.Total().getVideoMetadataFromID(i))

        if not newVideoIdList :
            return render_template('uploadLists.html', code = 404)
        else :
            return render_template('uploadLists.html',
                code = 200,
                categoryList = categoryList,
                typeList = typeList,
                dataList = dataList,
                videoMetaList = newVideoMetaList,
                videoIdList = newVideoIdList
            )
        '''