import datetime
import json
from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import send_from_directory
from pyparsing import Word

from hstack.models import Videopath
from hstack.models import Metadatum
from hstack.models import Keyword
from hstack.models import Timestamp
from sqlalchemy import and_

from hstack import searchAll
from hstack import makePPT

import os
import re
import platform

OS = platform.system()
bp = Blueprint('detail', __name__, url_prefix='/')

@bp.route('/detail/data/<path:filepath>')
def data(filepath):
    return send_from_directory('../media', filepath.split('media\\')[1].replace("\\", '/'))


@bp.route('/detail/<int:pk>', methods=['GET', 'POST'])
def detailFile(pk):
    videoPath = Videopath.query.filter(Videopath.id == pk).first().videoAddr 
    textPath = Videopath.query.filter(Videopath.id == pk).first().textAddr
    print(pk)
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    try:
        with open(textPath, 'r', encoding='UTF-8-sig') as f:
            scripts = f.readlines()
    except FileNotFoundError as err:
        print(err)
        scripts = []

    keywordQ = and_(Keyword.id == pk, Keyword.expose == True)

    if request.method == 'POST':
        word = request.form
        words = str(word)
        print (word)

    return render_template( '/detail.html',
        videoaddr = videoPath,
        scripts = scripts,
        #images = pptImage,
        #pptFile = pptFile,
        #sKeyword = ScriptSearch.query.filter(ScriptSearch.sKeyword == words),
        keywords = Keyword.query.filter(keywordQ).all(),
        metadatas = Metadatum.query.filter(Metadatum.id == pk).all(),
        timestamps =  Timestamp.query.filter(Timestamp.id == pk).all(),
    )


@bp.route('/detail/<int:pk>/ProcessUserinfo/<string:keywordinfo>', methods=['POST'])
def ProcessUserinfo(keywordinfo, pk):
    videoID = str(pk)
    print(videoID)

    #videoID = str(Videopath.q)
    keywordinfo = json.loads(keywordinfo)
    keyword = keywordinfo
    print()
    print(keyword)
    print()
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ')
    
    f = open("media\\Uploaded\\LogFile\\log_"+videoID+".txt", 'a')
    f.write(date+keyword+"\n")
    f.close()
    return('/')