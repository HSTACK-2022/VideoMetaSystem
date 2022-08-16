from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import send_file
from flask import render_template
from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy

from hstack.config import OS
from hstack.config import DB
from hstack.models import Videopath
from hstack.models import Metadatum
from hstack.models import Keyword
from hstack.models import Timestamp
from sqlalchemy import and_

from hstack import makePPT
import os

bp = Blueprint('detail', __name__, url_prefix='/')

@bp.route('/detail/data/<path:filepath>')
def data(filepath):
    print(filepath)
    return send_from_directory('../media', filepath.split('media\\')[1].replace("\\", '/'))

@bp.route('/detail/download/<string:path>/<string:title>')
def download(path, title):
    filepath = os.path.join('..', 'media', 'Uploaded', path, title+".pptx")
    print(filepath)
    return send_file(filepath)

@bp.route('/detail/<int:pk>', methods=['GET'])
def detailFile(pk):
    videoPath = Videopath.query.filter(Videopath.id == pk).first().videoAddr 
    textPath = Videopath.query.filter(Videopath.id == pk).first().textAddr.split("hstack\\")[1]

    try:
        with open(textPath, 'r', encoding='UTF-8-sig') as f:
            scripts = f.readlines()
    except FileNotFoundError as err:
        print(err)
        scripts = []

    print("############################")
    print(textPath)

    keywordQ = and_(Keyword.id == pk, Keyword.expose == True)

    # 이미지 받아오기
    pptImage = makePPT.getPPTImage(videoPath)

    # PPT 파일 생성
    title = Videopath.query.filter(Videopath.id == pk).first().title
    makePPT.getPPTFile(videoPath, title)

    # PPT 파일을 얻기 위한 폴더명 얻기
    pptPath = os.path.dirname(videoPath.split('Uploaded\\')[1])
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(pptPath)

    return render_template( '/detail.html',
        videoaddr = videoPath,
        scripts = scripts,
        images = pptImage,
        pptPath = pptPath,
        keywords = Keyword.query.filter(keywordQ).all(),
        metadatas = Metadatum.query.filter(Metadatum.id == pk).all(),
        timestamps =  Timestamp.query.filter(Timestamp.id == pk).all(),
    )

@bp.route('/detail/<int:pk>/edit', methods=['POST', 'GET'])
def editFile(pk):

    if request.method == "POST":
        sysKEList = request.form.getlist("sysKEList")
        sysKCList = request.form.getlist("sysKCList")

        newUserKEList = request.form.getlist("newUserKEList")
        newUserKCList = request.form.getlist("newUserKCList")
        userKEList = request.form.getlist("userKEList")
        userKCList = request.form.getlist("userKCList")
        
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(sysKEList)
        print(sysKCList)
        print(newUserKEList)
        print(newUserKCList)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        

        for i in range(len(sysKEList)):
            DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.keyword.like(sysKCList[i]), Keyword.sysdef == 1)).update({"expose" : sysKEList[i]}, synchronize_session="fetch")
            DB.session.flush()
        for i in range(len(userKEList)):
            DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.keyword.like(userKCList[i]), Keyword.sysdef == 0)).update({"expose" : userKEList[i]}, synchronize_session="fetch")
            DB.session.flush()
        for i in range(len(newUserKCList)):
            k = Keyword(
                id = Videopath.query.filter(Videopath.id == pk).first().id,
                keyword = newUserKCList[i],
                expose = newUserKEList[i],
                sysdef = 0
            )
            DB.session.add(k)
            DB.session.flush()

        DB.session.commit()
    
    videoPath = Videopath.query.filter(Videopath.id == pk).first().videoAddr 
    textPath = Videopath.query.filter(Videopath.id == pk).first().textAddr.split("hstack\\")[1]

    try:
        with open(textPath, 'r', encoding='UTF-8-sig') as f:
            scripts = f.readlines()
    except FileNotFoundError as err:
        print(err)
        scripts = []

    # 이미지 받아오기
    pptImage = makePPT.getPPTImage(videoPath)

    return render_template( 'success.html',
        pk = pk,
        videoaddr = videoPath,
        scripts = scripts,
        images = pptImage,
        keywords =  DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.sysdef == 1)).all(),
        userkeywords =  DB.session.query(Keyword).filter(and_(Keyword.id == pk, Keyword.sysdef == 0)).all(),
        metadatas = Metadatum.query.filter(Metadatum.id == pk).all(),
        timestamps =  Timestamp.query.filter(Timestamp.id == pk).all(),
    )