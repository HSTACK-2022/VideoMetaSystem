import os
import re
import platform
from unicodedata import category

from asgiref.sync import sync_to_async
from numpy import extract

from core.opencvService import getPPTImage

from . import models
from .models import Post, Category

from django import forms
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView , DetailView, CreateView, UpdateView
from django.db.models import Q

from urllib import response
from urllib.parse import urlparse

from core import searchAll
from core import extractMetadata
from core import rankAlgo

# 상수 설정
OS = platform.system()
renderAppName = "Core" if OS == 'Windows' else 'core'

# for backend.
def home(request):
    return render(request, renderAppName + '/test_home.html') 

# video(file) upload
def uploadFile(request):
    if request.method == "POST":
        existError = {}
        fileTitle = request.POST["fileTitle"]
        filePresenter = request.POST["presenter"]
        uploadedFile = request.POST.get("videoFile", None)

        if (fileTitle == ""):
            existError['nameError'] = "영상 제목을 입력해주세요."
        if (filePresenter == ""):
            existError['presenterError'] = "영상 소유자를 입력해주세요."
        if (uploadedFile == ""):
            existError['fileError'] = "영상 파일을 첨부해주세요."
        else:
            uploadedFile = request.FILES["videoFile"]

        if existError:
            return render(request, renderAppName + '/test_upload.html', context={"error" : existError}) 

        # Fetching the form data
        # Saving the information in the database
        else :
            document = models.Document(
                title = fileTitle,
                uploadedFile = uploadedFile
            )
            document.save()

            if OS == "Windows" : 
                dir_name = os.path.dirname(os.path.abspath(__file__)).split("\\core")[0]
                file_name = urlparse(document.uploadedFile.url).path.replace("/", "\\")
                videopath = dir_name + file_name

            else : 
                dir_name = os.path.dirname(os.path.abspath(__file__)).split("/core")[0]
                file_name = urlparse(document.uploadedFile.url).path
                videopath = dir_name + file_name
            
            # DB에 Video 저장
            models.Videopath.objects.create(
                title = fileTitle,
                videoaddr = videopath
            )
            videoId = models.Videopath.objects.get(videoaddr=videopath).id

            models.Metadata.objects.create(
                id = models.Videopath.objects.get(id=videoId),
                title = fileTitle,
                presenter = filePresenter,
                uploaddate = document.dateTimeOfUpload
            )

            if OS == 'Windows':
                videoPath4Play = "..\\..\\..\\media" + videopath.split("media")[1]
            else:
                videoPath4Play = "../../../media" + videopath.split("media")[1]
            print(videoPath4Play)

            extractMetadata.extractMetadata(videoId)

            return redirect('Core:home')
                        
    return render(request, renderAppName + '/test_upload.html') 


# 업로드 후 ~ User 확인 전의 영상 목록들
def uploadLists(request):
    videoIdList = models.Videopath.objects.filter(extracted = True).values_list('id', flat=True).distinct()
    categoryList = searchAll.extractCategories(videoIdList)
    typeList = searchAll.extractType(videoIdList)
    dataList = searchAll.extractData(videoIdList) 
    videoMetaList = list()
    for i in videoIdList: # (resultVideoIDList)에 저장되어 있는 id로 메타데이터 가져옴
        videoMetaList.append(searchAll.Total().getVideoMetadataFromID(i))

    print("********************")
    print(videoIdList)
    print(categoryList)
    print(videoMetaList)
    
    if not videoIdList :
        return render(request, renderAppName + '/test_uploadLists.html', context={'code' : 404})
    else :
        return render(request, renderAppName + '/test_uploadLists.html',
            context={
                'code' : 200,
                'categoryList' : categoryList,
                "typeList" : typeList,
                "dataList" : dataList,
                'videoMetaList' : videoMetaList,
                'videoIdList' : videoIdList,
            })

# 각 영상의 상세페이지 (/test/detail/pk)
def detailFile(request, pk):
    videoPath = models.Videopath.objects.get(id = pk).videoaddr
    if OS == 'Windows':
        videoPath4Play = "..\\..\\..\\media" + videoPath.split("media")[1]
    else:
        videoPath4Play = "../../../media" + videoPath.split("media")[1]
    
    textPath = models.Videopath.objects.get(id = pk).textaddr
    try:
        with open(textPath, 'r', encoding='UTF-8-sig') as f:
            scripts = f.readlines()
    except FileNotFoundError as err:
        print(err)
        scripts = []

    keywordQ = Q()
    keywordQ &= Q(id = pk)
    keywordQ &= Q(expose=True)

    # 이미지 받아오기
    pptImage = getPPTImage(pk)

    return render(
        request,
        renderAppName + '/test_detail.html',
        {
            'videoaddr' : videoPath4Play,
            'scripts' : scripts,
            'images' : pptImage,
            'keywords' : models.Keywords.objects.filter(keywordQ).all().values(),
            'metadatas' : models.Metadata.objects.filter(id = pk).all().values(),
            'timestamps' : models.Timestamp.objects.filter(id = pk).all().values(),
        }
    )

# 업로드 완료 된 영상의 상세페이지 (/test/success/pk)
def success(request, pk):
    if request.method == "POST":
        sysKEList = request.POST.getlist("sysKEList")
        sysKCList = request.POST.getlist("sysKCList")

        newUserKEList = request.POST.getlist("newUserKEList")
        newUserKCList = request.POST.getlist("newUserKCList")
        userKEList = request.POST.getlist("userKEList")
        userKCList = request.POST.getlist("userKCList")

        
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        print(sysKEList)
        print(sysKCList)
        print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")

        for i in range(len(sysKEList)):
            models.Keywords.objects.filter(id = pk).filter(keyword = sysKCList[i], sysdef=1).update(expose=sysKEList[i])
        for i in range(len(userKEList)):
            models.Keywords.objects.filter(id = pk).filter(keyword = userKCList[i], sysdef=0).update(expose=userKEList[i])
        for i in range(len(newUserKCList)):
            models.Keywords.objects.create(
                id = models.Videopath.objects.get(id=pk),
                keyword = newUserKCList[i],
                expose = newUserKEList[i],
                sysdef = 0
            )
        


    videoPath = models.Videopath.objects.get(id = pk).videoaddr
    if OS == 'Windows':
        videoPath4Play = "..\\..\\..\\media" + videoPath.split("media")[1]
    else:
        videoPath4Play = "../../../media" + videoPath.split("media")[1]
    
    textPath = models.Videopath.objects.get(id = pk).textaddr
    try:
        with open(textPath, 'r', encoding='UTF-8-sig') as f:
            scripts = f.readlines()
    except FileNotFoundError as err:
        print(err)
        scripts = []

    return render(
        request,
        renderAppName + '/test_success.html',
        {
            'pk' : pk,
            'videoaddr' : videoPath4Play,
            'scripts' : scripts,
            'keywords' : models.Keywords.objects.filter(id = pk).filter(sysdef = 1).all().values(),
            'userkeywords' : models.Keywords.objects.filter(id = pk).filter(sysdef = 0).all().values(),
            'metadatas' : models.Metadata.objects.filter(id = pk).all().values(),
            'timestamps' : models.Timestamp.objects.filter(id = pk).all().values(),
        }
    )

# search
def searchFile(request):
    if request.method == "GET":
        word = request.GET["searchText"]
        if word == "":
            return render(request, renderAppName + '/test_search.html',
                context={
                    'code': 404,
                    'searchWord' : ""
                })

        else :
            searchWords = []
            words = re.split(r'[ ,:]', word)
            for item in words:
                if item != "": searchWords.append(item)

            videoMetaList = []
            videoIdList = {}
            rankData = {}
            rankList = []

            # before
            categoryList = {}
            videoIdList, videoMetaList, categoryList, typeList, dataList, rankData = searchAll.search(searchWords)

            for j in videoIdList:
                rankDict = {}
                rankDict['id'] = j
                rankDict['title'] = rankData[j][0]
                rankDict['presenter'] = rankData[j][1]
                rankDict['index'] = rankData[j][2]
                rankDict['keyword'] = rankData[j][3]
                rankDict['total'] = rankData[j][4]
                rankList.append(rankDict)
            
            #print(rankList)

            if not videoIdList :
                return render(request, renderAppName + '/test_search.html',
                    context={
                        'code' : 404,
                        'searchWord' : word
                    })
            else :
                return render(request, renderAppName + '/test_search.html',
                    context={
                        'code' : 200,
                        'categoryList' : categoryList,
                        "typeList" : typeList,
                        "dataList" : dataList,
                        'videoMetaList' : videoMetaList,
                        'videoIdList' : videoIdList,
                        'searchWord' : word,
                        'rankData': rankList,
                    })

# category detail search
def detailSearch(request):
    word = request.POST['searchWord']
    stringvideoIdList = request.POST['videoIdList']
    search_type = request.POST['search_type']   # category , method, narrative
    search_detail_type = request.POST['search_detail_type'] # IT, 지리, 식물, ...
    videoIdList = stringvideoIdList[1:-1]
    videoIdList = videoIdList.replace(" ", "") # 공백 제거
    videoIdList = videoIdList.replace("'", "") # 작은 따옴표 제거
    videoIdList = videoIdList.split(',')
    newVideoIdList = list()

    #word = word.replace(" ", "") # 공백 제거
    #word = word.replace("'", "") # 작은 따옴표 제거
    #word = word.split(',')

    videoMetaList = []
    rankData = {}
    rankList = []
    newVideoIdList, videoMetaList, categoryList, typeList, dataList, rankData = searchAll.detailSearch(videoIdList, search_type, search_detail_type, word)

    print(">>>>>>>>>>>>>>>>>>>")
    print(rankData)
    for j in newVideoIdList:
        rankDict = {}
        rankDict['id'] = j
        rankDict['title'] = rankData[j][0]
        rankDict['presenter'] = rankData[j][1]
        rankDict['index'] = rankData[j][2]
        rankDict['keyword'] = rankData[j][3]
        rankDict['total'] = rankData[j][4]
        rankList.append(rankDict)

    print(type(videoMetaList[0]['id']))
    print(type(rankList[0]['id']))
    print(videoMetaList[0]['id'] == rankList[0]['id'])
    print(videoMetaList[0])

    print(rankList)

    if not videoIdList :
        return render(request, renderAppName + '/test_search.html',
            context={
                'code' : 404,
                'searchWord' : word
            })
    else :
        return render(request, renderAppName + '/test_search.html',
            context={
                'code' : 200,
                'categoryList' : categoryList,
                "typeList" : typeList,
                "dataList" : dataList,
                'videoMetaList' : videoMetaList,
                'videoIdList' : newVideoIdList,
                'searchWord' : word,
                'rankData': rankList,
            })