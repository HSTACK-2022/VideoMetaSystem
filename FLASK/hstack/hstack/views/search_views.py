from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import send_from_directory

from hstack import models
from hstack import searchAll

# from sqlalchemy import SQLAlchemy
from hstack.models import TotalSearch
from hstack.models import TitleSearch
from hstack.models import PresenterSearch
from hstack.models import KeywordSearch

import os
import re
import platform
import datetime # 로그파일 시간

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


OS = platform.system()
bp = Blueprint('search', __name__, url_prefix='/')


@bp.route('/data/<path:filepath>')
def data(filepath):
    return send_from_directory('../media', filepath.replace("\\", '/')[1:])


@bp.route('/search/', methods=['GET', 'POST'])
def searchFile():
    if request.method == "GET":
        word = request.args.get("searchText")
        title = request.args.get('searchTextTitle')
        keyword = request.args.get('searchTextKeyword')
        presenter = request.args.get('searchTextPresenter')

        print("###############################")
        print(word)
        print(title)
        print(keyword)
        print(presenter)

        if word == None and title == None and keyword == None and presenter == None:
            return render_template('search.html',
                                   code=404,
                                   searchWord="",
                                   categoryList="",
                                   typeList="",
                                   dataList="",
                                   videoMetaList="",
                                   videoIdList="",
                                   searchWordDetailTitle="",
                                   searchWordDetailKeyword="",
                                   searchWordDetailPresenter="",
                                   rankData="",
                                   )

        else:
            searchWords = []
            words = re.split(r'[ ,:]', word)
            for item in words:
                if item != "":
                    print(TotalSearch.query.filter( #DB에서 전체 단어 검색
                        TotalSearch.tKeyword == item))

                    #전체 검색 LOG 파일 생성 (필요 없으면 삭제해도 됨)
                    file = open('log\\total.txt','a',encoding='UTF-8') #a : 이어쓰기
                    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(item)
                    file.write(date+" "+item+"\n")
                    file.close()
                    # 요기 까지

                    searchWords.append(item)
                    if len(TotalSearch.query.filter(TotalSearch.tKeyword.contains(item)).all()) != 0:
                        db.session.query(TotalSearch).filter(
                            TotalSearch.tKeyword == item).update({'cnt': TotalSearch.cnt+1})
                        db.session.commit()

                    else:
                        ts = TotalSearch(tKeyword=item, cnt=1)
                        db.session.add(ts)
                        db.session.commit()

            if len(searchWords) == 0:
                searchWords = None

            searchTitles = []
            word += (title + " ")
            words = re.split(r'[ ,:]', title)
            for item in words:
                if item != "":
                    searchTitles.append(item)

                    #제목 세부 검색 DB 생성
                    if len(TitleSearch.query.filter(TitleSearch.tiKeyword.contains(item)).all()) != 0:
                        db.session.query(TitleSearch).filter(
                            TitleSearch.tiKeyword == item).update({'cnt': TitleSearch.cnt+1})
                        db.session.commit()

                    else:
                        tis = TitleSearch(tiKeyword=item, cnt=1)
                        db.session.add(tis)
                        db.session.commit()

            if len(searchTitles) == 0:
                searchTitles = None

            searchKeywords = []
            word += (keyword + " ")
            words = re.split(r'[ ,:]', keyword)
            for item in words:
                if item != "":
                    searchKeywords.append(item)

                    #키워드 세부 검색 DB 생성
                    if len(KeywordSearch.query.filter(KeywordSearch.kKeyword.contains(item)).all()) != 0:
                        db.session.query(KeywordSearch).filter(
                            KeywordSearch.kKeyword == item).update({'cnt': KeywordSearch.cnt+1})
                        db.session.commit()

                    else:
                        ks = KeywordSearch(kKeyword=item, cnt=1)
                        db.session.add(ks)
                        db.session.commit()

            if len(searchKeywords) == 0:
                searchKeywords = None

            searchPresenters = []
            word += (presenter + " ")
            words = re.split(r'[ ,:]', presenter)
            for item in words:
                if item != "":
                    searchPresenters.append(item)

                    #발표자 세부 검색 DB 생성
                    if len(PresenterSearch.query.filter(PresenterSearch.pKeyword.contains(item)).all()) != 0:
                        db.session.query(PresenterSearch).filter(
                            PresenterSearch.pKeyword == item).update({'cnt': PresenterSearch.cnt+1})
                        db.session.commit()

                    else:
                        ps = PresenterSearch(pKeyword=item, cnt=1)
                        db.session.add(ps)
                        db.session.commit()

            if len(searchPresenters) == 0:
                searchPresenters = None

            videoMetaList = []
            videoIdList = {}
            rankData = {}
            rankList = []

            # before
            categoryList = {}
            videoIdList, videoMetaList, categoryList, typeList, dataList, rankData = searchAll.search(
                All=searchWords, T=searchTitles, P=searchPresenters, K=searchKeywords)

            for j in videoIdList:
                rankDict = {}
                rankDict['id'] = j
                rankDict['title'] = rankData[j][0]
                rankDict['presenter'] = rankData[j][1]
                rankDict['keyword'] = rankData[j][2]
                rankDict['total'] = rankData[j][3]
                rankList.append(rankDict)

            print(rankList)

            if not videoIdList:
                return render_template('search.html',
                                       code=404,
                                       searchWord=word,
                                       categoryList="",
                                       typeList="",
                                       dataList="",
                                       videoMetaList="",
                                       videoIdList="",
                                       searchWordDetailTitle="",
                                       searchWordDetailKeyword="",
                                       searchWordDetailPresenter="",
                                       rankData="",
                                       )
            else:
                return render_template('search.html',
                                       code=200,
                                       categoryList=categoryList,
                                       typeList=typeList,
                                       dataList=dataList,
                                       videoMetaList=videoMetaList,
                                       videoIdList=videoIdList,
                                       searchWord=word,
                                       searchWordDetailTitle=title,
                                       searchWordDetailKeyword=keyword,
                                       searchWordDetailPresenter=presenter,
                                       rankData=rankList,
                                       )