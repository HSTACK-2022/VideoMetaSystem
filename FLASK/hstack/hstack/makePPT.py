import os
import platform

from .models import Keyword
from .models import Videopath
from .models import Metadatum
from .models import Timestamp
from pptx import Presentation
from pptx.util import Inches


# 상수 설정
OS = platform.system()


def getPPTFile(videoId):
    pptFile = Presentation()
    videoPathObj = Videopath.query.filter(
        Videopath.id == videoId)  # DB에서 videoId에 해당하는 객체를 가져옴
    imageFilePath = videoPathObj.imageaddr  # DB에서 imageAddr 추출
    title = videoPathObj.title

    if OS == "Windows":
        imagePath = (imageFilePath + "\\").replace("/", "\\")
    else:
        imagePath = (imageFilePath + "\\").replace("\\", "/")

    print(imageFilePath)
    print(imagePath)
    imageList = os.listdir(imageFilePath)
    print(imageList)

    slide_layout = pptFile.slide_layouts[6]

    for image in imageList:
        if image.startswith("L") or image.startswith("P"):
            print("**")
            slide = pptFile.slides.add_slide(slide_layout)
            slide.shapes.add_picture(
                imagePath + image, 0, 0, pptFile.slide_width, pptFile.slide_height)

    if OS == "Windows":
        pptPathRel = "../../../media/Uploaded/Image/" + \
            imageFilePath.split('Image\\')[1].replace(
                "\\", "/") + "/" + title + '.pptx'
    else:
        pptPathRel = "../../../media/Uploaded/Image/" + \
            imageFilePath.split('Image/')[1] + "/" + title + ".pptx"

    pptFile.save(imagePath + title + '.pptx')

    return pptPathRel
