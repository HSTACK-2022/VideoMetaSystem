import datetime
from distutils.log import debug
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import send_from_directory
from flask import json

from hstack.models import Videopath
from hstack.models import Metadatum
from hstack.models import Keyword
from hstack.models import Timestamp
from hstack.models import ScriptSearch
from sqlalchemy import and_

from hstack import searchAll
from hstack import makePPT


import os
import re
import platform


from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

OS = platform.system()
bp = Blueprint('detail', __name__, url_prefix='/')


@bp.route('/detail/data/<path:filepath>')
def data(filepath):
    return send_from_directory('../media', filepath.split('media\\')[1].replace("\\", '/'))


@bp.route('/detail/<int:pk>', methods=['GET'])
def detailFile(pk):
    videoPath = Videopath.query.filter(Videopath.id == pk).first().videoAddr
    textPath = Videopath.query.filter(Videopath.id == pk).first().textAddr
    # scriptSearch = request.args.get("searchScriptKeyword")
    scriptSearch = "ss"
    print(videoPath)
    try:
        with open(textPath, 'r', encoding='UTF-8-sig') as f:
            scripts = f.readlines()

            # if scriptSearch == None:
            #     print("none..")

            # elif len(ScriptSearch.query.filter(
            #         and_(ScriptSearch.sKeyword == scriptSearch, ScriptSearch.id)).all()) != 0:
            #     db.session.query(ScriptSearch).filter(and_(
            #         ScriptSearch.sKeyword == scriptSearch, ScriptSearch.id == pk)).update({'cnt': ScriptSearch.cnt+1})
            #     db.session.commit()
            #     print("elif..")

            # else:
            #     ss = ScriptSearch(id=pk, sKeyword=scriptSearch, cnt=1)
            #     db.session.add(ss)
            #     db.session.commit()
            #     print("else..")

    except FileNotFoundError as err:
        print(err)
        scripts = []

    keywordQ = and_(Keyword.id == pk, Keyword.expose == True)

    # 이미지 받아오기
    #pptImage = getPPTImage(pk)

    # PPT 파일 받아오기
    #pptFile = makePPT.getPPTFile(pk)

    return render_template('/detail.html',
                           videoaddr=videoPath,
                           videoaddr2=videoPath.replace('\\', "/"),
                           scripts=scripts,
                           #images = pptImage,
                           #pptFile = pptFile,
                           keywords=Keyword.query.filter(keywordQ).all(),
                           metadatas=Metadatum.query.filter(
                               Metadatum.id == pk).all(),
                           timestamps=Timestamp.query.filter(
                               Timestamp.id == pk).all(),
                           )


@bp.route('/detail/<int:pk>/ProcessKeywordinfo/<string:keywordinfo>', methods=['POST'])
def ProcessUserinfo(keywordinfo, pk):
    videoID = str(Videopath.query.filter(Videopath.id == pk).first().id)
    print(videoID)

    #videoID = str(Videopath.q)
    keywordinfo = json.loads(keywordinfo)
    keyword = keywordinfo
    print()
    print(keyword)
    print()
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')

    f = open("media\\Uploaded\\Log\\log_"+videoID+".txt", 'a')
    f.write(date+keyword+"\n")
    f.close()
    return('/')


if __name__ == '__main__':
    bp.run(debug=True)
