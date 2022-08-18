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
        searchWords = []
        words = re.split(r'[ ,:]', word)
        for item in words:
            if item != "": searchWords.append(item)
        if len(searchWords) == 0:
            searchWords = None

        searchTitles = []
        word = word + title + " " if title != "" else word
        words = re.split(r'[ ,:]', title)
        for item in words:
            if item != "": searchTitles.append(item)
        if len(searchTitles) == 0:
            searchTitles = None

        searchKeywords = []
        word = word + keyword + " " if keyword != "" else word
        words = re.split(r'[ ,:]', keyword)
        for item in words:
            if item != "": searchKeywords.append(item)
        if len(searchKeywords) == 0:
            searchKeywords = None

        searchPresenters = []
        word = word + presenter + " " if presenter != "" else word
        words = re.split(r'[ ,:]', presenter)
        for item in words:
            if item != "": searchPresenters.append(item)
        if len(searchPresenters) == 0:
            searchPresenters = None

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