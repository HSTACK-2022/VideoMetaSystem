from flask import Blueprint
from flask import send_file
from flask import render_template
from flask import send_from_directory

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
    videoPath = DB.session.query(Videopath).filter(Videopath.id == pk).first().videoAddr 
    textPath = DB.session.query(Videopath).filter(Videopath.id == pk).first().textAddr

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
    title = DB.session.query(Videopath).filter(Videopath.id == pk).first().title
    makePPT.getPPTFile(videoPath, title)

    # PPT 파일을 얻기 위한 폴더명 얻기
    pptPath = os.path.dirname(videoPath.split('Uploaded\\')[1])
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(pptPath)

    return render_template( 'detail.html',
        pk = pk,
        videoaddr = videoPath,
        scripts = scripts,
        images = pptImage,
        pptPath = pptPath,
        keywords = DB.session.query(Keyword).filter(keywordQ).all(),
        metadatas = DB.session.query(Metadatum).filter(Metadatum.id == pk).all(),
        timestamps =  DB.session.query(Timestamp).filter(Timestamp.id == pk).all(),
    )