import os, sys
import numpy as np

from datetime import datetime
import time

###########################################################################################

ENCODING = "UTF-8"
DELIM_KEY = "\t"

FILE_EXT = "."

###########################################################################################

''' CAT_LIST = ["01.news_r", "02.briefing", "03.his_cul", "04.paper", "05.minute",
            "06.edit", "07.public", "08.speech", "09.literature", "10.narration"]

INPUT_FIELDS = ["doc_type", "publisher", "publisher_year", "passage"]
LABEL_FIELDS = ["summary1"]

USAGE_RATE = 0.01 '''

###########################################################################################

'''
    로그를 파일에도 작성할 거면, 아래 함수에서 추가
'''
def logging(msg: str) :
    print(msg)

###########################################################################################

def check_option(option1: int, option2: int) :
    if option1 == option2 :
        return True
    elif (option1 & option2) != 0 :
        return True
    else :
        return False

def rm_option(option1: int, option2: int) :
    return (option1 | option2) ^ option2

###########################################################################################

def get_time_ms() :
    return int(round(time.time_ns() / 1000000))

def get_datetime_now(expression: str="%Y-%m-%d %H:%M:%S") :
    date_now = datetime.now()
    return date_now.strftime(expression)