import os
import platform

from pptx import Presentation
from pptx.util import Inches
from .config import OS


# 화면에 띄우기 위한 PPT 이미지 얻기
def getPPTImage(fileURL):
    pptImage = set()
    imagePath = os.path.join(os.path.dirname(fileURL), 'Image')
    imageList = os.listdir(imagePath)
    print(imageList)

    for image in imageList:
        if image.startswith("L") or image.startswith("P"):
            imageSrc = os.path.join(imagePath, image)
            pptImage.add(imageSrc)
    
    return pptImage


# PPT 파일 얻기
def getPPTFile(fileURL, title):
    pptFile = Presentation()
    imagePath = os.path.join(os.path.dirname(fileURL), 'Image')

    imageList = os.listdir(imagePath)
    print(imagePath)
    print(imageList)

    slide_layout = pptFile.slide_layouts[6]

    for image in imageList:
        if image.startswith("L") or image.startswith("P"):
            print("**")
            path = os.path.join(imagePath, image)
            slide = pptFile.slides.add_slide(slide_layout)
            slide.shapes.add_picture(path, 0, 0, pptFile.slide_width, pptFile.slide_height)
    

    pptPathRel = os.path.join(os.path.dirname(fileURL), title + '.pptx')
    pptFile.save(pptPathRel)