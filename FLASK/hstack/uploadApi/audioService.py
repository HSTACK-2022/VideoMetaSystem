# audioService.py
#
# video에서 10초 단위의 audio를 추출합니다.
# sttService.py에 의해 호출됩니다.
# 
# uses
# - video2audio(fileURL) : 비디오 파일을 오디오 파일로 추출
# - splitAudio(fileURL) : 오디오 파일을 10초 단위로 쪼개어 저장
# - video2splitedAudio(fileURL) : 비디오 파일을 10초 단위의 오디오 파일로 추출
#
# * video2splitedAudio() 내에서 video2audio(), splitAudio를 호출합니다.
#
# parameters
# - fileURL : 비디오 파일이 저장된 경로
# 
# return
# - audioDirPath : 10초 단위의 오디오들이 저장된 폴더의 경로
# * os.path.join(os.path.dirname(fileURL), 'Audio')와 동일.

import os
import math
import subprocess
from mutagen.wave import WAVE

from .config import OS


#비디오 파일을 10초단위 오디오 파일로 변경
def video2splitedAudio(fileURL):
    fullAudioFile = video2audio(fileURL)
    if (fullAudioFile != None):
        audioDirPath = splitAudio(fullAudioFile, 10)
        return audioDirPath


#비디오 파일을 받아 오디오 파일로 바꾼다.
def video2audio(fileURL):
    if OS == "Windows" : 
        audioName = os.path.basename(fileURL).replace("/", "\\").split('.')[0] + ".wav"
    else : 
        audioName = os.path.basename(fileURL).split('.')[0] + ".wav"
    audioPath = os.path.join(os.path.dirname(fileURL), audioName)
    print(audioPath)

    #Sampling rate:16000 / mono channel 
    result = subprocess.Popen(['ffmpeg', '-y',
        '-i', fileURL, '-vn', '-acodec', 'pcm_s16le', '-ar', '16k', '-ac', '1', '-ab', '128k', audioPath],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    exitcode = result.returncode
    if exitcode != 0:
        print(exitcode, out.decode('utf8'), err.decode('utf8'))
    else:
        print('Completed')

    return audioPath

# Audio를 조각낸다.
def splitAudio(audioFilePath, sec):
    audioLen = WAVE(audioFilePath).info.length              #파일의 전체 길이 알아오기
    audioName = os.path.basename(audioFilePath).split('.')[0]    # 파일의 이름만 가져오기 - test.wav 이면 test만
    audioPath = os.path.join(os.path.dirname(audioFilePath), 'Audio')
    os.makedirs(audioPath, 777, True)

    count = 0
    for i in range(0, math.ceil(audioLen), 10):
        startTime = 0 if (i == 0) else (i + 1)
        newAudioFilePath = os.path.join(audioPath, str(count) + ".wav")

        result = subprocess.Popen(
            ['ffmpeg', '-i', audioFilePath, '-ss', str(startTime), '-t', str(sec),
            '-acodec', 'copy', newAudioFilePath],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        out, err = result.communicate()
        exitcode = result.returncode
        if exitcode != 0:
            print(exitcode, out.decode('utf8'), err.decode('utf8'))
            return None
        else:
            print('%d Completed' %count)

        count+=1

    return audioPath