import asyncio
import os

from . import models
from urllib.parse import urlparse
from django.shortcuts import render, redirect
from core.extractMetadata import extractMetadata

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