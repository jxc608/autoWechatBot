#coding=utf-8
import re

def is_number(num):
    regex = re.compile(r"^(-?\d+)(\.\d*)?$")
    if re.match(regex,num):
        return True
    else:
        return False

def getSortedDict(dict):
    keys = dict.keys()
    keys.sort()
    return [dict[key] for key in keys]
