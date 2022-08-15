from flask import url_for
from flask import request
from flask import redirect
from flask import Blueprint
from flask import render_template
from flask import send_from_directory

from hstack import models
from hstack import searchAll

import os
import re
import platform

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
            searchWords = []
            words = re.split(r'[ ,:]', word)
            for item in words:
                if item != "": searchWords.append(item)
            if len(searchWords) == 0:
                searchWords = None

            searchTitles = []
            word += (title + " ")
            words = re.split(r'[ ,:]', title)
            for item in words:
                if item != "": searchTitles.append(item)
            if len(searchTitles) == 0:
                searchTitles = None

            searchKeywords = []
            word += (keyword + " ")
            words = re.split(r'[ ,:]', keyword)
            for item in words:
                if item != "": searchKeywords.append(item)
            if len(searchKeywords) == 0:
                searchKeywords = None

            searchPresenters = []
            word += (presenter + " ")
            words = re.split(r'[ ,:]', presenter)
            for item in words:
                if item != "": searchPresenters.append(item)
            if len(searchPresenters) == 0:
                searchPresenters = None

            videoMetaList = []
            videoIdList = {}
            rankData = {}
            rankList = []

            # before
            categoryList = {}
            #videoIdList, videoMetaList, categoryList, typeList, dataList, rankData = searchAll.search(All=searchWords, T=searchTitles, P=searchPresenters, K=searchKeywords)
            videoIdList, videoMetaList, categoryList, typeList, dataList, rankData = searchAll.searchTest(All=searchWords, T=searchTitles, P=searchPresenters, K=searchKeywords)

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
                )