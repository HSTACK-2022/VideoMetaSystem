# calTime.py
#
# int 형식의 sec를 받아 HH:MM:SS 형식으로 변환합니다.
# 
# uses
# - calSec2Time(sec)
#
# parameters
# - sec : 변환하고자 하는 시간 (초단위)
# 
# return
# - dataStr : HH:MM:SS 형태로 변환된 문자열

def calSec2Time(sec):
    hour = sec // 3600
    sec -= hour * 3600
    min = sec // 60
    sec -= min  * 60
    dateStr = str('%d:%d:%d' %(hour, min, sec))
    
    
    return dateStr