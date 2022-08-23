from flask import request
from flask import Blueprint
from flask import render_template
from flask import send_from_directory

from hstack import searchAll

# from sqlalchemy import SQLAlchemy
from hstack.config import DB
from hstack.models import TotalSearch
from hstack.models import TitleSearch
from hstack.models import PresenterSearch
from hstack.models import KeywordSearch

import os
import re
import datetime # 로그파일 시간

bp = Blueprint('search', __name__, url_prefix='/')


@bp.route('/data/<path:filepath>')
def data(filepath):
    return send_from_directory('../media', filepath.replace("\\", '/')[1:])


@bp.route('/search/', methods=['GET'])
def searchFile():
    word = request.args.get('searchText')
    title = request.args.get('searchTextTitle') if request.args.get('searchTextTitle') != None else ""
    keyword = request.args.get('searchTextKeyword') if request.args.get('searchTextKeyword') != None else ""
    presenter = request.args.get('searchTextPresenter') if request.args.get('searchTextPresenter') != None else ""
    isDetail = request.args.get('isDetail')

    print("###############################")
    print(word)
    print(title)
    print(keyword)
    print(presenter)
    print(isDetail)

    if word == None and title == None and keyword == None and presenter == None:
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
        searchWords = []
        words = re.split(r'[ ,:]', word)
        for item in words:
            if item != "":
                searchWords.append(item)

                #DB에서 전체 단어 검색
                print(TotalSearch.query.filter(TotalSearch.tKeyword == item))
                
                # [Logging] 전체 검색 LOG 파일 생성 (필요 없으면 삭제해도 됨)
                file = open(os.path.join('logs', 'full.txt'),'a+', encoding='UTF-8') #a : 이어쓰기
                date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(item)
                file.write(date+" "+item+"\n")
                file.close()

                # 요기 까지
                searchWords.append(item)
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

            videoIdList, videoMetaList, rankData = searchAll.detailSearch(
                All=searchWords,
                T=searchTitles,
                P=searchPresenters,
                K=searchKeywords,
                category=category,
                narrative=narrative,
                method=method
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
            
        print(rankList)

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
