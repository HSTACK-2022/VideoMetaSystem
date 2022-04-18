import os
import platform

# 상수 설정
OS = platform.system()

#상대경로를 절대경로로 변환하는 함수
def getRealDirPath(path):
    if OS == "Windows" : 
        BASE_DIR = os.getcwd().replace("/", "\\")
        FILE_DIR = os.path.dirname(path).replace("/", "\\")
        path = BASE_DIR + FILE_DIR + "\\"
    else :
        BASE_DIR = os.getcwd()
        FILE_DIR = os.path.dirname(path)
        path = BASE_DIR + FILE_DIR + "/"
    return path