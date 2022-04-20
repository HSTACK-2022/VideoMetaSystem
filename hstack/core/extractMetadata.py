# extractMetadata.py
#
# video를 통해 metadata를 추출합니다.
# 
# uses
# - extractMetadata(videoId)
#
# parameters
# - videoId : DB Table들의 key로 쓰이는 video의 고유 id
# 
# return
# - True : 작업이 정상적으로 완료된 경우
# - False : 중간에 오류가 발생한 경우

import threading

from core import keywordService

from . import audioService
from . import opencvService


def extractMetadata(videoId):
    try:
        threads = []

        basic = threading.Thread(target=opencvService.extBasicInfo, args=([videoId]))
        audio = threading.Thread(target=audioService.doAudioService, args=([videoId]))
        video = threading.Thread(target=opencvService.doOpencvService, args=([videoId]))
        
        basic.start()
        audio.start()
        video.start()
        
        threads.append(basic)
        threads.append(audio)
        threads.append(video)

        for thread in threads :
            print(thread)
            thread.join()

        keywordService.doKeywordService(videoId)
        return True

    except:
        print("### extractMetadata() : ERROR!! ###")
        return False