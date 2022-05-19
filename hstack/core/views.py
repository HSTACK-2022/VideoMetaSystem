import os
import re
import platform

from asgiref.sync import sync_to_async

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
from core.extractMetadata import extractMetadata

# 상수 설정
OS = platform.system()
renderAppName = "Core" if OS == 'Windows' else 'core'

class UserForm(UserCreationForm): # 회원가입 페이지
    class Meta:
        model = User
        fields = ["username","password1",  "password2", "email"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            # 'password1' : forms.PasswordInput(attrs={'class': 'form-control'}),
            # 'password2' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'ID',
            # 'password1': '패스워드',
            # 'password2': '패스워드확인',
            'email': '이메일',
        }

class PostList(ListView): #포스트 목록 페이지
    model = Post
    ordering = '-pk' #최신 글 순서대로

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all() #카테고리 있을 경우 카운트 같은거
        context['no_category_post_count'] = Post.objects.filter(category=None).count() #카테고리 없는 미분류 항목
        return context
    
class PostDetail(DetailView): #포스트 상세 페이지
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all() #카테고리 있을 경우 카운트 같은거
        context['no_category_post_count'] = Post.objects.filter(category=None).count() #카테고리 없는 미분류 항목
        return context

class PostCreate(CreateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'head_video', 'category']

    def form_valid(self, form): # 로그인 = 작성자 확인
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user #로그인 되어있으면 얘로 보내줌
            return super(PostCreate, self).form_valid(form) #폼 리턴
        else: #로그인 하지 않은 회원이면
            return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        pk = self.object.id
        #loop = asyncio.new_event_loop()
        #loop.run_in_executor(createMetadata(pk, callbacktest))
        #loop.close()
        return f'/core/{pk}/'
        #return redirect('core:detail', pk)

class PostUpdate(LoginRequiredMixin, UpdateView): #포스트 수정 기능
    model = Post

    fields = ['title', 'hook_text', 'content', 'head_image', 'head_video', 'category']

    template_name = 'core/post_update_form.html'

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied #로그인 한 회원과 사용자가 일치하지 않을 경우 허가 거부 

class PostSearch(PostList): #검색 창
    paginate_by = None

    def get_queryset(self):
        q = self.kwargs['q']
        post_list = Post.objects.filter(
            Q(title__contains=q) | Q(content__contains=q)
        ).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search: {q} ({self.get_queryset().count()})'

        return context

def category_page(request, slug): #카테고리 분류 페이지
    #category = Category.objects.get(slug=slug)
    if slug == 'no_category' :
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

        return render(
            request,
            'core/post_list.html',
            {
                'post_list' : post_list,
                'categories' : Category.objects.all(),
                'no_category_post_count' : Post.objects.filter(category=None).count(),
                'category' : category,
            }
        )
        
def signup(request):

    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('/')
    else:
        form = UserForm()
    return render(request, 'core/signup.html',{'form': form})


# for backend.
def home(request):
    return render(request, renderAppName + '/test_home.html') 

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

            videoMetaList = {}
            videoIdList = {}
            videoIdList, videoMetaList = searchAll.search(searchWords)

            if not videoMetaList :
                return render(request, renderAppName + '/test_search.html',
                    context={
                        'code' : 404,
                        'searchWord' : word
                    })
            else :
                for video in videoMetaList:
                    print("****")
                    print(video['thumbnail'])

                return render(request, renderAppName + '/test_search.html',
                    context={
                        'code' : 200,
                        'videoMetaList' : videoMetaList,
                        'videoIdList' : videoIdList,
                        'searchWord' : word,
                    })

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

            videoPathForPlay = videoPath = "../media" + videopath.split("media")[1]
            print(videoPathForPlay)
            bools = extractMetadata(videoId)
            return render(request, renderAppName + '/success.html', context={"file" : videopath, "Metadata":bools})
                        
    return render(request, renderAppName + '/test_upload.html') 

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

    return render(
        request,
        renderAppName + '/test_detail.html',
        {
            'videoaddr' : videoPath4Play,
            'scripts' : scripts,
            'keywords' : models.Keywords.objects.filter(id = pk).all().values(),
            'metadatas' : models.Metadata.objects.filter(id = pk).all().values(),
            'timestamps' : models.Timestamp.objects.filter(id = pk).all().values(),
        }
    )






# for test.
def success(request):
    pk = 28     ######## 수정 필요

    if request.method == "POST":
        keywordButtonList = request.POST.getlist("keywordButtonList")
        keywordsBtn = request.POST.getlist("keywordsBtn")
        
        print(">>>>>>>>>>>>>>>>>>>")
        print(len(keywordButtonList))
        print(len(keywordsBtn))

        for i in range(len(keywordButtonList)):
            models.Keywords.objects.filter(id = pk).filter(keyword = keywordsBtn[i]).update(expose=keywordButtonList[i])
        


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
            'videoaddr' : videoPath4Play,
            'scripts' : scripts,
            'keywords' : models.Keywords.objects.filter(id = pk).all().values(),
            'metadatas' : models.Metadata.objects.filter(id = pk).all().values(),
            'timestamps' : models.Timestamp.objects.filter(id = pk).all().values(),
        }
    )
def test_successFinish(request):
    keywordButtonList = request.POST['keywordButtonList']
    print(keywordButtonList)

def test_minhwa(request):
    return render(
        request,
        renderAppName + '/test.html',
        {
            'keywords' : models.Keywords.objects.filter(id = 28).all().values(),
            'metadatas' : models.Metadata.objects.filter(id = 28).all().values(),
            'timestamps' : models.Timestamp.objects.filter(id = 28).all().values(),
        }
    )

from core import searchAll
def test_minhwa2(request):
    videoMetaList = searchAll.searchTest()
    videoIdList = searchAll.searchTest2()
    # for id in videoIdList:
    #     res = {}
    #     res[]
    print(videoIdList)
    return render(
        request,
        'Core/test2.html',
        {
            'videoMetaList' : videoMetaList,
            'videoIdList' : videoIdList,
        }
    )
def test_minhwa3(request):
    stringvideoIdList = request.POST['videoIdList']
    search_type = request.POST['search_type']   # category
    search_detail_type = request.POST['search_detail_type'] # IT, 지리, 식물, ...
    #print(category_type)
    #print(stringvideoIdList) # {14, 15, 16, 17, 18}
    videoIdList = stringvideoIdList[1:-1]
    videoIdList = videoIdList.replace(" ", "") # 공백 제거
    videoIdList = videoIdList.replace("'", "") # 작은 따옴표 제거
    videoIdList = videoIdList.split(',')
    newVideoIdList = list()

    newVideoIdList, videoMetaList = searchAll.detailSearch(videoIdList, search_type, search_detail_type)
    
    #print(videoIdList)

    for video in videoMetaList:
        print("****")
        print(video['thumbnail'])
        
    return render(request, renderAppName + '/test_search.html',
        context={
            'code' : 200,
            'videoMetaList' : videoMetaList,
            'videoIdList' : newVideoIdList,
        })