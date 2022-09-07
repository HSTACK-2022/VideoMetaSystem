# Api calls
from flask import jsonify
from flask import request
from flask_restx import Resource, Namespace

from datetime import datetime
import time as t

from . import extractMetadata
from .models import Videopath
from .models import Metadatum
from .models import Keyword
from .models import Timestamp
from .models import UploadTime
from .config import DB


Upload = Namespace('Upload')

@Upload.route('')
class ExtractMetadata(Resource):
    def post(self):
        startTime = t.time()

        fileTitle = request.form.get('title')
        print(fileTitle)
        filePresenter = request.form.get("presenter")
        print(filePresenter)
        uploadURL = request.form.get('uploadURL')
        print(uploadURL)
        password = request.form.get('password')
        print(password)
        canSearch = request.form.get('canSearch')
        print(canSearch)
        
        totalDic = extractMetadata.extract(fileTitle, filePresenter, uploadURL)

        extracted = 2 if (canSearch == 'True') else 0
        
        # DB 저장
        # Videopath
        videoPath = Videopath(
            title = totalDic["title"],
            videoAddr = totalDic["videoAddr"],
            audioAddr = totalDic["audioAddr"],
            textAddr = totalDic["textAddr"],
            imageAddr = totalDic["imageAddr"],
            extracted = extracted,
            password = password
        )
        DB.session.add(videoPath)
        DB.session.commit()
            
        id = videoPath.id

        # metadata
        category = ""
        categoryPerc = ""
        for c in totalDic["category"]:
            category += (c + ", ")
            categoryPerc += ((str)(round(totalDic["category"][c], 3)) + ", ")

        metadata = Metadatum(
            id = id,
            title = totalDic["title"],
            presenter = totalDic["presenter"],
            category = category[0:-2],
            category_percent = categoryPerc[0:-2],
            narrative = totalDic["narrative"],
            presentation = totalDic["presentation"],
            videoLength = totalDic["videoLength"],
            videoFrame = totalDic["videoFrame"],
            videoSize = totalDic["videoSize"],
            videoType = totalDic["videoType"],
            uploadDate = datetime.now().date()
        )

        DB.session.add(metadata)
        DB.session.commit()

        # keyword, timestamp
        for key in totalDic["keyword"]:
            k = Keyword(
                id = id,
                keyword = key,
                percent = float(totalDic["keyword"][key]),
                expose = 1,
                sysdef = 1
            )
            DB.session.add(k)
            DB.session.flush()

        for time in totalDic["index"]:
            i = Timestamp(
                id = id,
                time = time,
                subtitle = totalDic["index"][time],
                expose = 1,
                sysdef = 1
            )
            DB.session.add(i)
            DB.session.flush()

        DB.session.commit()

        # upload_time
        endTime = t.time()
        sizeMB = round(float(totalDic["videoSize"])/1048576, 2)
        uploadTime = UploadTime(
            id = id,
            time = endTime - startTime,
            size = sizeMB  # byte to MB
        )
        DB.session.add(uploadTime)
        DB.session.commit()

        return jsonify(totalDic)