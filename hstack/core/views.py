import asyncio
import os

from . import models
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from core.extractMetadata import extractMetadata

from unicodedata import category
from django.shortcuts import render
from django.views.generic import ListView , DetailView, CreateView
from .models import Post, Category

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

#video list를 보여준다.
def video_list(request):
    video_list = models.Document.objects.all()
    return render(request, 'Core/video_list.html', {'video_list': video_list})

#video(file) upload
def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        # Saving the information in the database
        if request.FILES.get("uploadedFile") :
            fileTitle = request.POST["fileTitle"]
            uploadedFile = request.FILES["uploadedFile"]
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