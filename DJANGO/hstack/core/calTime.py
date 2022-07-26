# calTime.py
#
# int 형식의 sec를 받아 HH:MM:SS 형식으로 변환합니다.

def calSec2Time(sec):
    hour = sec // 3600
    sec -= hour * 3600
    min = sec // 60
    sec -= min  * 60
    dateStr = str('%d:%d:%d' %(hour, min, sec))
    
    
    return dateStr