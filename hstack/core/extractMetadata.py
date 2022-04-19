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

from . import audioService
from . import opencvService


def extractMetadata(videoId):
    #video 기본 정보 추출
    bools = opencvService.extBasicInfo(videoId)
    print(bools)
    
    #audio를 활용한 Service 호출
    bools = audioService.doAudioService(videoId)
    print(bools)

    return bools