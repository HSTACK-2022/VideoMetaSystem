from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import current_app as app # app.config 사용을 위함

import re
import os
import platform
from urllib import response
from urllib.parse import urlparse
from werkzeug.utils import secure_filename

from .. import extractMetadata

# 상수 설정
bp = Blueprint('main', __name__, url_prefix='/')

#@bp.route('/')
#def home():
#    return render_template('home.html')

@bp.route('/', methods=['GET', 'POST'])
def uploadFile():
    if request.method == "POST":
        existError = {}
        fileTitle = request.form.get("fileTitle")
        filePresenter = request.form.get("presenter")
        uploadedFile = request.files["videoFile"]

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

        #extractMetadata.extract("title", "presenter", ".\\media\\Uploaded\\algo\\algo.mp4")
        extractMetadata.extract(fileTitle, filePresenter, uploadURL)
        return render_template('success.html')

        
    return render_template('upload.html', error="")