#!/usr/bin/env python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import re
import requests
import random
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    " ".join(map(str, cleantext))
    return cleantext

def swedify(input):
    input = re.sub(r'Ã¤', 'ä', input)
    input = re.sub(r'Ã¶', 'ö', input)
    input = re.sub(r'Ã¥', 'å', input)
    input = re.sub(r'Ã', 'Ä', input)
    input = re.sub(r'Ã', 'Ä', input)
    input = re.sub(r'Ä ', 'Ö', input)
    input = re.sub(r'Â»', '', input)
    return input

html = requests.get('https://exempelmeningar.se/sv/kebab').text
soup = bs(html, 'html5lib')
out = soup.find("div", {'class': 'tabs-container'})
my_list = str(out).split("<hr/>")
mening = random.choice(my_list)
mening = swedify(mening)
print(cleanhtml(mening))