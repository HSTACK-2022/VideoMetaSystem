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

from core import indexingService, keywordService

from . import audioService
from . import opencvService


def extractMetadata(videoId):
    try:
        threads = []

        # Step1) 기본 Metadata 추출 : index, keyword 제외
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
        
        threads.clear()

        # Step2) keyword, index 추출
        # 둘다 konlpy 기반의 Service이므로 동시에 못돌림
        keywordService.doKeywordService(videoId)
        indexingService.doIndexingService(videoId)

        return True

    except Exception as e:
        print(e)
        print("### extractMetadata() : ERROR!! ###")
        return False