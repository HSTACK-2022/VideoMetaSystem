import os
import platform
import subprocess

from . import models
from . import getRealPath

# 상수 설정
OS = platform.system()

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
    WORK_DIR = getRealPath.getRealDirPath(videoFilePath)

    if OS == "Windows" : 
        videoName = os.path.basename(videoFilePath).replace("/", "\\")
        audioName = videoName.split('.')[0] + ".wav"
        videoPath = WORK_DIR + videoName 
        audioPath = WORK_DIR.split('Video\\')[0] + "Audio\\" + audioName
    else : 
        videoName = os.path.basename(videoFilePath)
        audioName = videoName.split('.')[0] + ".wav"
        videoPath = WORK_DIR + videoName 
        audioPath = WORK_DIR.split('Video/')[0] + "Audio/" + audioName

    #Sampling rate:16000 / mono channel 
    result = subprocess.Popen(['ffmpeg', '-y',
        '-i', videoPath, '-vn', '-acodec', 'pcm_s16le', '-ar', '16k', '-ac', '1', '-ab', '128k', audioPath],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    exitcode = result.returncode
    if exitcode != 0:
        print(exitcode, out.decode('utf8'), err.decode('utf8'))
    else:
        print('Completed')

    return audioPath