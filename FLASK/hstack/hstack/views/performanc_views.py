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

    # 단어 그래프
    # 1. 단어 종류
    # 2. 제목, 키워드, 발표자 각 비율 + 전체
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
        category = list(categories_dict.keys()),
        category_data = list(categories_dict.values()),
        narrative = list(narrative_dict.keys()),
        narrative_data = list(narrative_dict.values()),
        method = list(method_dict.keys()),
        method_data = list(method_dict.values()),
        totalWord = list(totalWord.keys()),
        totalWord_data = list(totalWord.values()),
    )