# datetime2sec.py
#
# HH:MM:SS 형식의 time string을 받아 sec로 반환합니다.
# 
# uses
# - datetime2sec(time)
#
# parameters
# - time : HH:MM:SS 형태의 문자열
# 
# return
# - sec : 문자열을 초 형태로 바꾼 값


def datetime2sec(time):
    timeStr = (str)(time).split(":")
    hour = (int)(timeStr[0])
    min = (int)(timeStr[1])
    sec = (int)(timeStr[2])
    return hour * 3600 + min * 60 + sec