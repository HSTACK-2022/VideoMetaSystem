# main.py
#
# uploadApi로 request가 들어오면
# 영상에서 메타데이터를 추출하고, 그 값을 DB에 저장합니다.
# 외부(본 프로젝트에서는 주로 hstack)에 의해 호출됩니다.
# 
# uses / parameters
# - POST로 아래의 값 전달
# - title : 영상의 제목
# - filePresenter : 영상 업로더 (제공자)
# - uploadURL : 영상이 업로드 된 서버 내의 경로
# - password : 영상 편집시 업로더 인증을 위한 비밀번호
# - canSearch : 검색을 허용할 것인지에 대한 flag
# 
# * canSearch는 추후 uploadApi만을 단독으로 사용할 경우를 위한 변수이며,
# 22.09.15 기준 현재 프로젝트에서는 hstack만 uploadApi를 호출하기 때문에
# canSearch의 값은 항상 true로 고정되어 있습니다.
# 
#
# return
# - finalDic : 영상의 메타데이터를 json 형태로 반환합니다.
# - DB : 메타데이터와 영상 업로드에 소요된 시간을 DB에 저장합니다.

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
            title=totalDic["title"],
            videoAddr=totalDic["videoAddr"],
            audioAddr=totalDic["audioAddr"],
            textAddr=totalDic["textAddr"],
            imageAddr=totalDic["imageAddr"],
            extracted=extracted,
            password=password
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
            id=id,
            title=totalDic["title"],
            presenter=totalDic["presenter"],
            category=category[0:-2],
            category_percent=categoryPerc[0:-2],
            narrative=totalDic["narrative"],
            presentation=totalDic["presentation"],
            videoLength=totalDic["videoLength"],
            videoFrame=totalDic["videoFrame"],
            videoSize=totalDic["videoSize"],
            videoType=totalDic["videoType"],
            uploadDate=datetime.now().date()
        )

        DB.session.add(metadata)
        DB.session.commit()

        # keyword, timestamp
        for key in totalDic["keyword"]:
            k = Keyword(
                id=id,
                keyword=key,
                percent=float(totalDic["keyword"][key]),
                expose=1,
                sysdef=1
            )
            DB.session.add(k)
            DB.session.flush()

        for time in totalDic["index"]:
            i = Timestamp(
                id=id,
                time=time,
                subtitle=totalDic["index"][time],
                expose=1,
                sysdef=1
            )
            DB.session.add(i)
            DB.session.flush()

        DB.session.commit()

        # upload_time
        endTime = t.time()
        sizeMB = round(float(totalDic["videoSize"])/1048576, 2)
        uploadTime = UploadTime(
            id=id,
            time=endTime - startTime,
            size=sizeMB  # byte to MB
        )
        DB.session.add(uploadTime)
        DB.session.commit()

        return jsonify(totalDic)
