
from importlib_metadata import metadata
from . import models
import os
import platform
from django.db.models import Count

# 상수 설정
OS = platform.system()

def rankAlgo():
    preWeight = models.Timestamp.objects.values('subtitle').annotate(Count('subtitle'))
    print("gggg")
    #print(preWeight)