import os
import platform

from .models import TotalSearch
from .models import TitleSearch
from .models import KeywordSearch
from .models import PresenterSearch

# 전체 검색 _ DB에서 가장 많이 검색된 단어들 출력
def total_search():
    #totalList = TotalSearch.query.filter_by(cnt=1).all()
    totalList= "dddd"
    print(totalList)
    return totalList

# 제목 검색

# 키워드 검색

# 발표자 검색

# 세부 검색 페이지 _ 미완임.
# https://www.delftstack.com/ko/howto/python/python-find-string-in-file/#file-readlines%25EB%25A9%2594%25EC%2584%259C%25EB%2593%259C%25EB%25A5%25BC-%25EC%2582%25AC%25EC%259A%25A9%25ED%2595%2598%25EC%2597%25AC-python%25EC%259D%2598-%25ED%258C%258C%25EC%259D%25BC%25EC%2597%2590%25EC%2584%259C-%25EB%25AC%25B8%25EC%259E%2590%25EC%2597%25B4-%25EC%25B0%25BE%25EA%25B8%25B0
# file = open("temp.txt", "w")
# file.write("blabla is nothing.")
# file.close()

# def check_string():
#     with open('temp.txt') as temp_f:
#         datafile = temp_f.readlines()
#     for line in datafile:
#         if 'blabla' in line:
#             return True # The string is found
#     return False  # The string does not exist in the file

# if check_string():
#     print('True')
# else:
#     print('False')