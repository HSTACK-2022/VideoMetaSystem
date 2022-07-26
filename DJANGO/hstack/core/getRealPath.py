# getRealPath.py
#
# 주어진 path를 절대경로로 반환합니다.
# - Windows인 경우 "\\"
# - 그 외의 경우 "/"
# 
# uses
# - getRealDirPath(path)
#
# parameters
# - path : 절대경로로 변환하고자 하는 경로
# 
# return
# - path : 변경된 경로

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