# audioService.py
#
# video에서 audio를 추출하고, 이를 이용한 metadata를 얻어냅니다.
# - audio에서 성별 정보 얻기
# - audio에서 다수가 말하는지의 여부 추출
# - audio를 통해 script, keyword, topic 추출 (sttService.py 참고)
# 
# uses
# - doAudioService(videoId)
#
# parameters
# - videoId : DB Table들의 key로 쓰이는 video의 고유 id
# 
# return
# - True : 작업이 정상적으로 완료된 경우
# - False : 중간에 오류가 발생한 경우

import os
import platform
import threading
import subprocess

from sqlalchemy import true

from . import models
from . import getRealPath
from . import sttService
from . import keywordService

# 상수 설정
OS = platform.system()

# audioService
def doAudioService(videoId):
    threads = []
    audioFile = video2audio(videoId)
    if (audioFile) :
        models.Videopath.objects.filter(id=videoId).update(audioaddr = audioFile)
        vt = threading.Thread(target=voiceThread, args=([videoId]))
        st = threading.Thread(target=scriptThread, args=([videoId]))
        vt.start()
        st.start()
        threads.append(vt)
        threads.append(st)

        for thread in threads:
            thread.join()
        
        return True

    return False

# 남여를 구별하는 Thread용 함수
def voiceThread(videoId):
    male_prop = float(detectSex(videoId))
    models.Metadata.objects.filter(id = videoId).update(
        voicemanrate = male_prop,
        voicewomanrate = 1 - male_prop
    )

# sttService를 돌리는 Thread용 함수
def scriptThread(videoId):
    textFile = sttService.doSttService(videoId)
    if (textFile) :
        models.Videopath.objects.filter(id=videoId).update(textaddr = textFile)
        return True    
    return False

# 통 오디오 파일을 받아오는 함수
def getFullAudioFile(videoId):
    videoPathObj = models.Videopath.objects.get(id=videoId)     #DB에서 videoId에 해당하는 객체를 가져옴
    if videoPathObj:
        return videoPathObj.audioaddr     
    else :
        return None

#비디오 파일을 받아 오디오 파일로 바꾼다.
def video2audio(videoId):
    videoPathObj = models.Videopath.objects.get(id=videoId)     #DB에서 videoId에 해당하는 객체를 가져옴
    videoFilePath = videoPathObj.videoaddr              #DB에서 videoAddr 추출

    if OS == "Windows" : 
        videoName = os.path.basename(videoFilePath).replace("/", "\\")
        audioName = videoName.split('.')[0] + ".wav"
        videoPath = videoFilePath + videoName 
        audioPath = videoFilePath.split('Video\\')[0] + "Audio\\" + audioName
    else : 
        videoName = os.path.basename(videoFilePath)
        audioName = videoName.split('.')[0] + ".wav"
        videoPath = videoFilePath + videoName 
        audioPath = videoFilePath.split('Video/')[0] + "Audio/" + audioName

    #Sampling rate:16000 / mono channel 
    result = subprocess.Popen(['ffmpeg', '-y',
        '-i', videoFilePath, '-vn', '-acodec', 'pcm_s16le', '-ar', '16k', '-ac', '1', '-ab', '128k', audioPath],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    exitcode = result.returncode
    if exitcode != 0:
        print(exitcode, out.decode('utf8'), err.decode('utf8'))
    else:
        print('Completed')

    return audioPath

# AudioFile로 남/여를 구분한다.
def detectSex(videoId):
    audio = getFullAudioFile(videoId)
    modelPath = os.path.join(os.getcwd(), "tensorflow\\AudioDetect\\test.py")
    
    #>python tensorflow\AudioDetect\test.py -f fff.mp3
    result = subprocess.check_output(['python', modelPath, '-f', audio], universal_newlines=True)
    male_prop = result.split("*****")[1]

    return male_prop