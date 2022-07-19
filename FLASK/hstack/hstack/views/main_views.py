from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template

from hstack import models
#from hstack import extractMetadata

import re
import os
import platform
from urllib import response
from urllib.parse import urlparse
from werkzeug.utils import secure_filename

# 상수 설정
OS = platform.system()
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/upload/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == "POST":
        existError = {}
        fileTitle = request.form.get("fileTitle")
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

        # Fetching the form data
        # Saving the information in the database
        else :
            document = models.Document(
                title = fileTitle,
                uploadedFile = uploadedFile
            )
            document.save()

            if OS == "Windows" : 
                dir_name = os.path.dirname(os.path.abspath(__file__)).split("\\core")[0]
                file_name = urlparse(document.uploadedFile.url).path.replace("/", "\\")
                videopath = dir_name + file_name

            else : 
                dir_name = os.path.dirname(os.path.abspath(__file__)).split("/core")[0]
                file_name = urlparse(document.uploadedFile.url).path
                videopath = dir_name + file_name
            
            # DB에 Video 저장
            models.Videopath.objects.create(
                title = fileTitle,
                videoaddr = videopath
            )
            videoId = models.Videopath.objects.get(videoaddr=videopath).id

            models.Metadata.objects.create(
                id = models.Videopath.objects.get(id=videoId),
                title = fileTitle,
                presenter = filePresenter,
                uploaddate = document.dateTimeOfUpload
            )

            if OS == 'Windows':
                videoPath4Play = "..\\..\\..\\media" + videopath.split("media")[1]
            else:
                videoPath4Play = "../../../media" + videopath.split("media")[2]
            print(videoPath4Play)

            #extractMetadata.extractMetadata(videoId)

            return redirect(url_for('home'))
                        
    return render_template('upload.html', error="")