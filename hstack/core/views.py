import asyncio
import imp
import os

from . import models
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from core.extractMetadata import extractMetadata
from urllib import response
from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post, Category
from django.core.exceptions import PermissionDenied

class UserForm(UserCreationForm):
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

    # def form_valid(self, form): # 로그인 = 작성자 확인
    #     current_user = self.request.user
    #     if current_user.is_authenticated:
    #         form.instance.author = current_user #로그인 되어있으면 얘로 보내줌
    #         return super(PostCreate, self).form_valid(form) #폼 리턴
    #     else: #로그인 하지 않은 회원이면
    #         response = super(PostCreate, self).form_valid(form)
    #         id_str = self.request.POST.get('id_str')
    #         if id_str:
    #             form.instance.author = id_str
    #         return response

class PostUpdate(LoginRequiredMixin, UpdateView):

    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'head_video', 'category']

    def dispatch(self, request, *args, **kwargs) :
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied #로그인 한 회원과 사용자가 일치하지 않을 경우 허가 거부 


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
            'player/post_list.html',
            {
                'post_list' : post_list,
                'categories' : Category.objects.all(),
                'no_category_post_count' : Post.objects.filter(category=None).count(),
                'category' : category,
            }
        )
        


#video(file) upload
def post_form(request):
    print("*******************************************")
    print("*******************************************")
    print("*******************************************")
    print("*******************************************")
    print("*******************************************")
    print("*******************************************")
    if request.method == "POST":
        # Fetching the form data
        # Saving the information in the database
        if request.FILES.get("head_video") :
            fileTitle = request.POST["title"]
            uploadedFile = request.FILES["head_video"]
            document = models.Document(
                title = fileTitle,
                uploadedFile = uploadedFile
            )
            document.save()

            dir_name = os.path.dirname(os.path.abspath(__file__)).split("\\core")[0]
            file_name = urlparse(document.uploadedFile.url).path.replace("/", "\\")
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
                uploaddate = document.dateTimeOfUpload
            )
            
            bools = extractMetadata(videoId)
            return render(request, "Core/success.html", context={"file" : document, "Metadata":bools})
                        
    return render(request, "Core/upload.html") 


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
