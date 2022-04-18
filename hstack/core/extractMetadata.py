from core import audioService
from . import models
from . import sttService
from . import opencvService
from . import keywordService


def extractMetadata(videoId):
    #video 기본 정보 추출
    bools = opencvService.extBasicInfo(videoId)
    
    #audio File 추출
    audioFile = audioService.video2audio(videoId)
    if (audioFile) :
        models.Videopath.objects.filter(id=videoId).update(audioaddr = audioFile)
        # 이 앞에 몇명인지 확인하는 코드 필요!
        sex = audioService.detectSex(videoId)
        if (sex) : 
            models.Metadata.objects.filter(id = videoId).update(voicesex = sex)
        models.Videopath.objects.filter(id=videoId).update(audioaddr = audioFile)
        textFile = sttService.doSttService(videoId)
        if (textFile) :
            models.Videopath.objects.filter(id=videoId).update(textaddr = textFile)
            keywords = keywordService.mergeKeyword(videoId, None, None)
            if(keywords) :
                for keyword in keywords :
                    print(keyword)
                    models.Keywords.objects.create(
                        id = models.Videopath.objects.get(id=videoId),
                        keyword = keyword
                    )
                    metadata = models.Keywords.objects.filter(id = videoId)
                topic = keywordService.extractTopic(videoId)
                if(topic):
                    print("*************************************************")
                    print(topic)
                    models.Metadata.objects.filter(id = videoId).update(topic = topic)
                return True

    return False