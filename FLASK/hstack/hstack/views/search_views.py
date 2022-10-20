# search_views.py
#
# 영상 검색 목록 router
#
#
# [routes]
# - data(filepath)
#   : '/search/data/<path:filepath>'
#   : 이미지 파일 전송.
#   : filepath 경로에 있는 파일을 파일 시스템에서 찾아 전달.
#
# - searchFile()
#   : '/search/', method=['GET']
#   : searchAll()을 호출하여 검색 결과를 제공합니다.
#   : Category, Narrative, Presentation에 대해 필터가 주어진 경우 필터 결과를 전달합니다.


from flask import request
from flask import Blueprint
from flask import render_template
from flask import send_from_directory

from hstack import intent
from hstack import searchAll

# from sqlalchemy import SQLAlchemy
from hstack.config import DB, OS
from hstack.models import TotalSearch
from hstack.models import TitleSearch
from hstack.models import PresenterSearch
from hstack.models import KeywordSearch
from hstack.models import SearchSatisfy

import os
import re
import datetime  # 로그파일 시간

bp = Blueprint('search', __name__, url_prefix='/')


@bp.route('/data/<path:filepath>')
def data(filepath):
    if OS == "Windows":
        return send_from_directory('../media', filepath.replace("\\", '/')[1:])
    else :
        return send_from_directory('../media', filepath)

@bp.route('/search/satisfy/<int:value>')
def satisfySave(value):
    DB.session.query(SearchSatisfy).filter(SearchSatisfy.val == value).update({'cnt': SearchSatisfy.cnt+1})
    DB.session.commit()

@bp.route('/search/', methods=['GET'])
def searchFile():
    word = request.args.get('searchText')
    title = request.args.get('searchTextTitle') if request.args.get('searchTextTitle') != None else ""
    keyword = request.args.get('searchTextKeyword') if request.args.get('searchTextKeyword') != None else ""
    presenter = request.args.get('searchTextPresenter') if request.args.get('searchTextPresenter') != None else ""
    isDetail = request.args.get('isDetail')

    print("검색: ")
    print("검색 문장/단어: "+word)
    print("세부 검색: ")
    print("title: "+title+" keyword: "+keyword+" presenter: "+presenter)

    if word == "" and title == "" and keyword == "" and presenter == "":
        return render_template('search.html',
            code = 404,
            searchWord = "",
            categoryList = "",
            typeList = "",
            dataList = "",
            videoMetaList = "",
            videoIdList = "",
            searchWordDetailTitle = "",
            searchWordDetailKeyword = "",
            searchWordDetailPresenter = "",
            rankData = "",
        )

    else :
        # if totalSearch
        searchWords = intent.findWord(word)

        # [Logging] 전체 검색 DB (필요 없으면 삭제해도 됨)
        for item in searchWords:
            if len(TotalSearch.query.filter(TotalSearch.tKeyword.contains(item)).all()) != 0:
                DB.session.query(TotalSearch).filter(TotalSearch.tKeyword == item).update({'cnt': TotalSearch.cnt+1})
            else:
                ts = TotalSearch(tKeyword=item, cnt=1)
                DB.session.add(ts)
            DB.session.commit()

        if len(searchWords) == 0:
            searchWords = None

        # if title/presenter/keyword Search
        # titleSearch
        searchTitles = []
        word = word + title + " " if title != "" else word
        words = re.split(r'[ ,:]', title)
        for item in words:
            if item != "":
                searchTitles.append(item)

                # [Logging] 제목 세부 검색 DB 생성
                if len(TitleSearch.query.filter(TitleSearch.tiKeyword.contains(item)).all()) != 0:
                    DB.session.query(TitleSearch).filter(TitleSearch.tiKeyword == item).update({'cnt': TitleSearch.cnt+1})
                else:
                    tis = TitleSearch(tiKeyword=item, cnt=1)
                    DB.session.add(tis)
                DB.session.commit()

        if len(searchTitles) == 0:
            searchTitles = None

        # keywordSearch
        searchKeywords = []
        word = word + keyword + " " if keyword != "" else word
        words = re.split(r'[ ,:]', keyword)
        for item in words:
            if item != "":
                searchKeywords.append(item)

                # [Logging] 키워드 세부 검색 DB 생성
                if len(KeywordSearch.query.filter(KeywordSearch.kKeyword.contains(item)).all()) != 0:
                    DB.session.query(KeywordSearch).filter(KeywordSearch.kKeyword == item).update({'cnt': KeywordSearch.cnt+1})
                else:
                    ks = KeywordSearch(kKeyword=item, cnt=1)
                    DB.session.add(ks)
                DB.session.commit()

        if len(searchKeywords) == 0:
            searchKeywords = None

        # presenterSearch
        searchPresenters = []
        word = word + presenter + " " if presenter != "" else word
        words = re.split(r'[ ,:]', presenter)
        for item in words:
            if item != "":
                searchPresenters.append(item)

                # [Logging] 발표자 세부 검색 DB 생성
                if len(PresenterSearch.query.filter(PresenterSearch.pKeyword.contains(item)).all()) != 0:
                    DB.session.query(PresenterSearch).filter(PresenterSearch.pKeyword == item).update({'cnt': PresenterSearch.cnt+1})
                else:
                    ps = PresenterSearch(pKeyword=item, cnt=1)
                    DB.session.add(ps)
                DB.session.commit() 

        if len(searchPresenters) == 0:
            searchPresenters = None

        # get Rank
        videoMetaList = []
        videoIdList = {}
        rankData = {}
        rankList = []

        # if DetailSearch
        if isDetail == "True":
            category = request.args.get('category')
            narrative = request.args.get('narrative')
            method = request.args.get('method')

            categories = re.split(r'[ ,:]', category)
            categorySet = set()
            for c in categories:
                if (c != ''):
                    categorySet.add(c)
            categorySet = sorted(categorySet)
            
            category = ""
            for c in categorySet:
                category += c + ", "

            videoIdList, videoMetaList, rankData = searchAll.detailSearch(
                All=searchWords,
                T=searchTitles,
                P=searchPresenters,
                K=searchKeywords,
                category=categorySet,
                narrative=narrative,
                presentation=method
            )

        # if not detailSearch    
        else :
            category = ""
            narrative = ""
            method = ""

            videoIdList, videoMetaList, rankData = searchAll.search(
                All=searchWords,
                T=searchTitles,
                P=searchPresenters,
                K=searchKeywords
            )

        # get Specific Lists    
        categoryList = searchAll.extractCategories(videoIdList)
        typeList = searchAll.extractType(videoIdList)
        dataList = searchAll.extractData(videoIdList)

        for j in videoIdList:
            rankDict = {}
            rankDict['id'] = j
            rankDict['title'] = rankData[j][0]
            rankDict['presenter'] = rankData[j][1]
            rankDict['keyword'] = rankData[j][2]
            rankDict['category'] = rankData[j][3]
            rankDict['total'] = rankData[j][4]
            rankList.append(rankDict)

        if not videoIdList :
            return render_template('search.html',
                code = 404,
                searchWord = word,
                categoryList = "",
                typeList = "",
                dataList = "",
                videoMetaList = "",
                videoIdList = "",
                searchWordDetailTitle = "",
                searchWordDetailKeyword = "",
                searchWordDetailPresenter = "",
                rankData = "",
                category = "",
                narrative = "",
                method = ""
            )
        else :
            return render_template('search.html',
                code = 200,
                categoryList = categoryList,
                typeList = typeList,
                dataList = dataList,
                videoMetaList = videoMetaList,
                videoIdList = videoIdList,
                searchWord = word,
                searchWordDetailTitle = title,
                searchWordDetailKeyword = keyword,
                searchWordDetailPresenter = presenter,
                rankData = rankList,
                category = category,
                narrative = narrative,
                method = method
            )