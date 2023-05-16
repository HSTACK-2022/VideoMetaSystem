import os
import platform
import tempfile

from . import models
from pptx import Presentation
from pptx.util import Inches
from fpdf import FPDF


# 상수 설정
OS = platform.system()

def convertPPTtoPDF(pptPath):                                   #필요에 따라 PPT 파일 경로를 매개변수로 받고, PPT를 열어 PDF로 저장한 뒤, PDF 파일 경로를 반환
    pdfPath = os.path.splitext(pptPath)[0] + '.pdf'
    ppt = Presentation(pptPath)
    ppt.save(pdfPath)
    return pdfPath

def getPPTFile(videoId, convert_to_pdf=False):
    pptFile = Presentation()
    videoPathObj = models.Videopath.objects.get(id=videoId)     #DB에서 videoId에 해당하는 객체를 가져옴
    imageFilePath = videoPathObj.imageaddr                      #DB에서 imageAddr 추출
    title = videoPathObj.title

    if OS == "Windows" : 
        imagePath = (imageFilePath + "\\").replace("/", "\\")
    else : 
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
            slide.shapes.add_picture(imagePath + image, 0, 0, pptFile.slide_width, pptFile.slide_height)
    
    if OS == "Windows": 
        pptPathRel = "../../../media/Uploaded/Image/" + imageFilePath.split('Image\\')[1].replace("\\", "/") + "/" + title + '.pptx'
    else: 
        pptPathRel = "../../../media/Uploaded/Image/" + imageFilePath.split('Image/')[1] + "/" + title + ".pptx"

    pptFile.save(imagePath + title + '.pptx')

    if convert_to_pdf:
        pdfPath = convertPPTtoPDF(imagePath + title + '.pptx')
        return pptPathRel, pdfPath

    return pptPathRel
