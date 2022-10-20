import collections
from operator import and_
from this import s
from flask import Blueprint
from flask import render_template
from flask import current_app as app # app.config 사용을 위함

import platform
import re
from ..config import DB

from ..models import Keyword
from ..models import Videopath
from ..models import Metadatum
from ..models import Timestamp
from ..models import TotalSearch
from ..models import TitleSearch
from ..models import KeywordSearch
from ..models import PresenterSearch
from ..models import UpoladTime

import os

# 상수 설정
OS = platform.system()
bp = Blueprint('performance', __name__, url_prefix='/')

@bp.route('/performance/')
def ratio():
    # 메타데이터 비율 그래프
    categories_dict = {}
    categories=[]
    for res in Metadatum.query.with_entities(Metadatum.category).all():
        for c in res:
            categories.append(c)
    for item in categories:
        if item is None:
            continue
        words = re.split(r'[ ,:]',item)
        for word in words:
            if word in categories_dict:
                categories_dict[word] += 1
            else:
                categories_dict[word] = 1
    print(categories_dict)

    narrative_dict = {}
    narrative=[]
    for res in Metadatum.query.with_entities(Metadatum.narrative).all():
        for n in res:
            narrative.append(n)
    for item in narrative:
        if item is None:
            continue
        if item in narrative_dict:
            narrative_dict[item] += 1
        else:
            narrative_dict[item] = 1

    method_dict = {}
    method=[]
    for res in Metadatum.query.with_entities(Metadatum.method).all():
        for n in res:
            method.append(n)
    for item in method:
        if item is None:
            continue
        if item in method_dict:
            method_dict[item] += 1
        else:
            method_dict[item] = 1
            
    # for item in categories:
    #     words = re.split(r'[ ,:]',item)
    #     if words != "": categories2.append(words)
    #     if len(categories2) == 0:
    #         categories2 = None
    # print(categories2)


    # 업로드 시간 그래프
    uploadTime = []
    uploadSize = []
    for res in DB.session.query(UpoladTime).order_by(UpoladTime.size).limit(20):
        uploadTime.append(res.time)
        uploadSize.append(res.size)


    # 검색 단어 그래프
    totalWord = {}
    for res in DB.session.query(TotalSearch).order_by(TotalSearch.cnt.desc()).limit(10):
        totalWord[res.tKeyword] = res.cnt
    print("Total Search에서 나온 단어>>")
    print(totalWord)

    titleWord = {}
    keyWord = {}
    presenterWord = {}
    for res in DB.session.query(TitleSearch).order_by(TitleSearch.cnt.desc()).limit(10):
        titleWord[res.tiKeyword] = res.cnt
    for res in DB.session.query(KeywordSearch).order_by(KeywordSearch.cnt.desc()).limit(10):
        keyWord[res.kKeyword] = res.cnt
    for res in DB.session.query(PresenterSearch).order_by(PresenterSearch.cnt.desc()).limit(10):
        presenterWord[res.pKeyword] = res.cnt


    return render_template('/performance.html',
        code = 200,
        totalWord_total = totalWord.items(),
        titleWord_total = titleWord.items(),
        keyWord_total = keyWord.items(),
        presenterWord_total = presenterWord.items(),
        category = list(categories_dict.keys()),
        category_data = list(categories_dict.values()),
        narrative = list(narrative_dict.keys()),
        narrative_data = list(narrative_dict.values()),
        method = list(method_dict.keys()),
        method_data = list(method_dict.values()),
        upload_time = uploadTime,
        upload_size = uploadSize,
        totalWord = list(totalWord.keys()),
        totalWord_data = list(totalWord.values()),
        titleWord = list(titleWord.keys()),
        titleWord_data = list(titleWord.values()),
        presenterWord = list(presenterWord.keys()),
        presenterWord_data = list(presenterWord.values()),
        keyWord = list(keyWord.keys()),
        keyWord_data = list(keyWord.values()),
    )

@bp.route('/performance/detail/')
def performance_detail():
    return render_template('/performance_detail.html',
                           code=200,
                           metadatas=DB.session.query(Metadatum).all(),
                           paging=DB.session.query(Metadatum).count()
                           )

@bp.route('/performance/detail/<int:pk>', methods=['GET'])
def performance_detailFile(pk):

    # document_text = open("./logs/full.txt", 'r',encoding='UTF8')
    # text_string = document_text.read()
    # print("4$$$$$#1323412341")

    
    readdata = []
    with open("./logs/full.txt", "r" ,encoding='UTF8') as f:
        for line in f:
            readdata.append(line[20:].strip())

    # data = text_string.split('\n')[-5:]
    print(readdata)
    # print(text_string)

    counts = collections.Counter(readdata)
    sorted_dict = dict(sorted(counts.items(), key = lambda item: item[1], reverse = True))
    scriptsWord = list(sorted_dict.keys())[0:10]
    scriptsCnt = list(sorted_dict.values())[0:10]
    print(scriptsWord)
    print(scriptsCnt)
    print(sorted_dict)

    return render_template('/performance_charts.html',
        code = 200,
        pk = pk,
        scriptsWord = scriptsWord,
        scriptsCnt = scriptsCnt,
        metadatas=DB.session.query(Metadatum).filter(Metadatum.id == pk).all()
    )