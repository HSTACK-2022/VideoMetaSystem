from asyncio.windows_events import NULL
import threading
import sttService


audioPath = None
filePath = None
audioPath_0 = []
audioPath_1 = []
audioPath_2 = []
audioPath_3 = []
audioPath_4 = []
audioPathVector = []
result_0 = []
result_1 = []
result_2 = []
result_3 = []
result_4 = []
resultVector = []
threads = []

def pcm2text(audioPath, filePath) : 

    return True


def sttAsync(endNum):
    for i in range(0, endNum):
        if i%5 == 0:
            audioPath_0.append(audioPath+str(i)+".pcm")
        elif i%5 == 1:
            audioPath_1.append(audioPath+str(i)+".pcm")
        elif i%5 == 2:
            audioPath_2.append(audioPath+str(i)+".pcm")
        elif i%5 == 3:
            audioPath_3.append(audioPath+str(i)+".pcm")
        elif i%5 == 4:
            audioPath_4.append(audioPath+str(i)+".pcm")
    audioPathVector.append(audioPath_0)
    audioPathVector.append(audioPath_1)
    audioPathVector.append(audioPath_2)
    audioPathVector.append(audioPath_3)
    audioPathVector.append(audioPath_4)
    resultVector.append(result_0)
    resultVector.append(result_1)
    resultVector.append(result_2)
    resultVector.append(result_3)
    resultVector.append(result_4)

    for i in range(0, 5):
        th = threading.Thread(target=threadWork, args=([i]))
        th.start()
        threads.append(th)

    for thread in threads:
        thread.join()

    resultFileWrite(endNum)

def threadWork(num):
    threadAudioPath = audioPathVector[num]
    threadResult = resultVector[num]

    for i in range(0,len(threadAudioPath)):
        print(str(num) + ">>" + str(len(threadAudioPath)) + ">>" + str(threadAudioPath[i]))
        threadResult.append(sttService.audio2text(threadAudioPath[i],num)) # num -> keyNum
        # result of Pcm2Text = 
            # new Pcm2Text().pcm2text(String.valueOf(audioPath.get(i)),keys[number]
        print("@@@@" + str(resultVector))

def resultFileWrite(endNum):
    for j in range(int(endNum/5)+1):
        for i in range (0,5):
            if i==0 and j==0:
                #sttService.content2file(str((5 * j) + i) + "\n" + resultVector[i][j], filePath, True)
                sttService.content2file(resultVector[i][j], filePath, True)
                continue
            elif(j>len(resultVector[i])-1):
                continue
            #sttService.content2file(str((5 * j) + i) + "\n" + resultVector[i][j], filePath, False)
            sttService.content2file(resultVector[i][j], filePath, False)


# if __name__ == '__main__':
#     sttAsync(6)