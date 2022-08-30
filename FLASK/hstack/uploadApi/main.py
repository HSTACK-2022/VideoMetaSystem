# Api calls
from flask import jsonify
from flask import request
from flask_restx import Resource, Namespace

from datetime import datetime

from . import extractMetadata
from .models import Videopath
from .models import Metadatum
from .models import Keyword
from .models import Timestamp
from .config import DB


Upload = Namespace('Upload')

@Upload.route('')
class ExtractMetadata(Resource):
    def post(self):
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

        if (canSearch == 'True') :
            # DB 저장
            videoPath = Videopath(
                title = totalDic["title"],
                videoAddr = totalDic["videoAddr"],
                audioAddr = totalDic["audioAddr"],
                textAddr = totalDic["textAddr"],
                imageAddr = totalDic["imageAddr"],
                extracted = 2,
                password = password
            )
            
            DB.session.add(videoPath)
            DB.session.commit()
            
            id = videoPath.id

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
                method = totalDic["method"],
                videoLength = totalDic["videoLength"],
                videoFrame = totalDic["videoFrame"],
                videoSize = totalDic["videoSize"],
                videoType = totalDic["videoType"],
                uploadDate = datetime.now().date()
            )
            DB.session.add(metadata)
            DB.session.commit()

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

        return jsonify(totalDic)