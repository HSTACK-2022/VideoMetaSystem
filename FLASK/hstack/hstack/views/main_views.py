from aiohttp import FormData
from attr import dataclass
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template

import requests
import platform
from urllib.parse import urlparse
from werkzeug.utils import secure_filename
from requests_toolbelt import MultipartEncoder

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
        uploadedFile = request.files["videoFile"]

        if (fileTitle == ""):
            existError['nameError'] = "영상 제목을 입력해주세요."
        if (filePresenter == ""):
            existError['presenterError'] = "영상 소유자를 입력해주세요."
        if (secure_filename(uploadedFile.filename) == ""):
            existError['fileError'] = "영상 파일을 첨부해주세요."

        if existError:
            return render_template('upload.html', error=existError)

        # API로 request
        data = {'title':fileTitle, 'presenter':filePresenter}
        files = [('videoFile', ('solid.mp4', open('./media/Uploaded/Video/solid.mp4', 'rb'), 'video/mp4'))]
        headers = {'Content-Type' : 'multipart/form-data'}
        res = requests.post('http://127.0.0.1:8000/upload', headers=headers, data=data, files=files)
        print(res)
        
        return redirect(url_for('main.home'))
                        
    return render_template('upload.html', error="")