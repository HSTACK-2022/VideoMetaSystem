from urllib.parse import urlencode
from flask import jsonify
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import current_app as app # app.config 사용을 위함

import os
import requests
import platform
import background

from werkzeug.utils import secure_filename

# 상수 설정
OS = platform.system()
bp = Blueprint('main', __name__, url_prefix='/')

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


@background.task
def send2API(title, presenter, password, uploadURL):
    # API로 request
    reqUrl = 'http://127.0.0.1:8000/upload'
    data = {'title' : title, 'presenter' : presenter, 'uploadURL' : uploadURL}
    res = requests.post(reqUrl, data=data)
    res.apparent_encoding
    print(res.encoding)
    print(res.text)
    print("password for Editing : " + password)