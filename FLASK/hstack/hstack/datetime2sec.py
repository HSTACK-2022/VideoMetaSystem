def datetime2sec(time):
    timeStr = (str)(time).split(":")
    hour = (int)(timeStr[0])
    min = (int)(timeStr[1])
    sec = (int)(timeStr[2])
    return hour * 3600 + min * 60 + sec
    
