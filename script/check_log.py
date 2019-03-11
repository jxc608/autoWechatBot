#encoding=utf-8
import re

def out_limit(filepath, rule):
    f = open(filepath, 'r', encoding='utf8')
    lines = f.readlines()
    for line in lines:
        mt = re.search(rule, line)
        if mt:
            print(mt.group(1))
    f.close()

if __name__ == '__main__':
    filepath = r'D:\temp\2019-03-05_err.log'
    rule = 'Wechat Limit: wid: (.*)__,__'
    out_limit(filepath, rule)
