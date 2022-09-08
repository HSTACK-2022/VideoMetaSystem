from ast import keyword
from email.policy import default
from tkinter.messagebox import QUESTION
from winreg import QueryInfoKey
from flask import request
from flask import Blueprint
from flask import render_template
from flask import current_app as app  # app.config 사용을 위함

import os
import re
import platform
import datetime

from ..config import DB

from ..models import Keyword
from ..models import Videopath
from ..models import Metadatum
from ..models import Timestamp
from ..models import TotalSearch
from ..models import TitleSearch
from ..models import KeywordSearch
from ..models import PresenterSearch
from ..models import UploadTime

from ..datetime2sec import datetime2sec

# 상수 설정
OS = platform.system()
bp = Blueprint('performance', __name__, url_prefix='/')


@bp.route('/performance/')
def ratio():
    # 메타데이터 비율 그래프
    categories_dict = {}
    categories = []
    for res in Metadatum.query.with_entities(Metadatum.category).all():
        for c in res:
            categories.append(c)
    for item in categories:
        if item is None:
            continue
        words = re.split(r'[ ,:]', item)
        for word in words:
            if word in categories_dict:
                categories_dict[word] += 1
            else:
                categories_dict[word] = 1
    print(categories_dict)

    narrative_dict = {}
    narrative = []
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
    method = []
    for res in Metadatum.query.with_entities(Metadatum.presentation).all():
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
    for res in DB.session.query(UploadTime).order_by(UploadTime.size).limit(20):
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

    # detailWord = {}
    # for t in titleWord:
    #     if t in detailWord:
    #         detailWord[t] = detailWord[t]+titleWord[t]
    #     else:
    #         detailWord[t] = titleWord[t]
    # for k in keyWord:
    #     if k in detailWord:
    #         detailWord[k] = detailWord[k]+keyWord[k]
    #     else:
    #         detailWord[k] = keyWord[k]
    # for p in presenterWord:
    #     if p in detailWord:
    #         detailWord[p] = detailWord[p]+presenterWord[p]
    #     else:
    #         detailWord[p] = presenterWord[p]

    return render_template('/performance.html',
                           code=200,
                           category=list(categories_dict.keys()),
                           category_data=list(categories_dict.values()),
                           narrative=list(narrative_dict.keys()),
                           narrative_data=list(narrative_dict.values()),
                           method=list(method_dict.keys()),
                           method_data=list(method_dict.values()),
                           upload_time=uploadTime,
                           upload_size=uploadSize,
                           totalWord=list(totalWord.keys()),
                           totalWord_data=list(totalWord.values()),
                           totalWord_total=totalWord.items(),
                           titleWord=list(titleWord.keys()),
                           titleWord_data=list(titleWord.values()),
                           titleWord_total=titleWord.items(),
                           presenterWord=list(presenterWord.keys()),
                           presenterWord_data=list(presenterWord.values()),
                           presenterWord_total=presenterWord.items(),
                           keyWord=list(keyWord.keys()),
                           keyWord_data=list(keyWord.values()),
                           keyWord_total=keyWord.items()
                           )



@bp.route('/performance/search/')
def performance_search():
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

    return render_template('/performance_search.html',
                           code=200,
                           totalWord=list(totalWord.keys()),
                           totalWord_data=list(totalWord.values()),
                           totalWord_total=totalWord.items(),
                           titleWord=list(titleWord.keys()),
                           titleWord_data=list(titleWord.values()),
                           titleWord_total=titleWord.items(),
                           presenterWord=list(presenterWord.keys()),
                           presenterWord_data=list(presenterWord.values()),
                           presenterWord_total=presenterWord.items(),
                           keyWord=list(keyWord.keys()),
                           keyWord_data=list(keyWord.values()),
                           keyWord_total=keyWord.items()
                           )

@bp.route('/performance/metadata/')
def performance_metadata():
    # 메타데이터 비율 그래프
    categories_dict = {}
    categories = []
    for res in Metadatum.query.with_entities(Metadatum.category).all():
        for c in res:
            categories.append(c)
    for item in categories:
        if item is None:
            continue
        words = re.split(r'[ ,:]', item)
        for word in words:
            if word in categories_dict:
                categories_dict[word] += 1
            else:
                categories_dict[word] = 1
    print(categories_dict)

    narrative_dict = {}
    narrative = []
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
    method = []
    for res in Metadatum.query.with_entities(Metadatum.presentation).all():
        for n in res:
            method.append(n)
    for item in method:
        if item is None:
            continue
        if item in method_dict:
            method_dict[item] += 1
        else:
            method_dict[item] = 1

    # 업로드 시간 그래프
    uploadTime = []
    uploadSize = []
    for res in DB.session.query(UploadTime).order_by(UploadTime.size).limit(20):
        uploadTime.append(res.time)
        uploadSize.append(res.size)

    return render_template('/performance_metadata.html',
                           code=200,
                           category=list(categories_dict.keys()),
                           category_data=list(categories_dict.values()),
                           narrative=list(narrative_dict.keys()),
                           narrative_data=list(narrative_dict.values()),
                           method=list(method_dict.keys()),
                           method_data=list(method_dict.values()),
                           upload_time=uploadTime,
                           upload_size=uploadSize
                           )

@bp.route('/performance/videoviews/')
def performance_videoviews():
    # 모든 객체의 id를 가져온다.
    allVideo = DB.session.query(Videopath).all()
    idViewDict = dict()
    idTimeDict = dict()
    
    for video in allVideo:
        idViewDict[video.id] = 0
        idTimeDict[video.id] = 0


    # 각 객체별 log파일 open : 조회수 count
    datetime_format = "%H:%M:%S"

    for key in idViewDict:
        logPath = os.path.join(app.config.get('UPLOAD_LOG_DIR'), str(key)+".txt")
        if os.path.isfile(logPath):
            viewCnt = 0
            timeCnt = 0
            startTime = 0
            endTime = 0
            log = open(logPath, 'r', encoding='utf-8-sig')
            scripts = log.readlines()
            for line in scripts: 
                cmd = line.split(' ')
                if (cmd[2] == '*open\n'):
                    startTime = datetime.datetime.strptime(cmd[1], datetime_format)
                elif (cmd[2] == '*close\n'):
                    viewCnt += 1
                    endTime = datetime.datetime.strptime(cmd[1], datetime_format)
                    timeCnt += datetime2sec(endTime - startTime)

            idViewDict[key] = viewCnt
            idTimeDict[key] = round(timeCnt / viewCnt, 2)

    idViewList = sorted(idViewDict.items(), key = lambda item: item[1], reverse = True)
    idViewMeta = list()
    for key, value in idViewList:
        videoObj = DB.session.query(Metadatum).filter(Metadatum.id == key).first()
        valDict = dict()
        valDict['id'] = key
        valDict['views'] = value
        valDict['title'] = videoObj.title
        valDict['presenter'] = videoObj.presenter
        valDict['uploadDate'] = videoObj.uploadDate
        idViewMeta.append(valDict)

    print(idViewMeta)
    print(idTimeDict)


    return render_template('/performance_videoview.html',
                           code = 200,
                           idView = idViewMeta,
                           idTime = list(idTimeDict.keys()),
                           idTime_data = list(idTimeDict.values())
                           )



@bp.route('/performance/detail/')
def performance_datail():
    page = request.args.get('page', type=int, default=1)
    pagination = DB.session.query(Metadatum).paginate(
        page, per_page=10)  # 한 페이지에 5개 게시글 나열

    print("PAGEEEEEEEEEEEEEEEEEEEEEEE")
    print(pagination)
    print(pagination.items)
    return render_template('/performance_detail.html',
                           code=200,
                           metadatas=DB.session.query(Metadatum).all(),
                           paging=DB.session.query(Metadatum).count(),
                           pagination=pagination
                           )

@bp.route('/performance/detail/<int:pk>', methods=['GET'])
def performance_detailFile(pk):
    return render_template('/performance_charts.html',
        code = 200,
        pk = pk,
        metadatas=DB.session.query(Metadatum).filter(Metadatum.id == pk).all()
    )
