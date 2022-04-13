from django.shortcuts import render, redirect

from core import audioService
from . import models
from . import sttService
from . import keywordService

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

            # DB에 Video 저장
            models.Videopath.objects.create(
                title = fileTitle,
                videoaddr = document.uploadedFile.url
            )

            # DB Check
            videoId = models.Videopath.objects.get(videoaddr=document.uploadedFile.url).id

            # AudioFile 추출
            audioFile = audioService.video2audio(videoId)
            if (audioFile) :
                models.Videopath.objects.filter(id=videoId).update(audioaddr = audioFile)
                textFile = sttService.doSttService(videoId)
                if (textFile) :
                    models.Videopath.objects.filter(id=videoId).update(textaddr = textFile)
                    keywords = keywordService.getKeyword(videoId, None, None)
                    if(keywords) :
                        models.Metadata.objects.create(
                            id = models.Videopath.objects.get(id=videoId),
                            keyword = keywords
                        )
                        metadata = models.Metadata.objects.get(id = videoId)
                        return render(request, "Core/success.html", context={"file" : document, "Metadata":metadata})
            return render(request, "Core/success.html", context={"file" : document})    

        # True if empty  
        else :
            return render(request, "Core/upload.html") 

    else :
        return render(request, "Core/upload.html") 