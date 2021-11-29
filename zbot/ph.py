#!/usr/bin/env python
import re
import requests
from bs4  import BeautifulSoup as bs
import sys

def unclutter(text):
    return ''.join(i for i in text if ord(i)<128)

try:
    g = "commentMessage"
    while 'commentMessage' in g:
        pr = requests.get('https://www.pornhub.com/random',  allow_redirects=True).text
        soup = bs(pr, 'html.parser')
        messages = soup.find("div", attrs={'class':'commentMessage'})
        if messages is None: 
            g = "commentMessage"
        else:
            g = messages.text
            g = re.sub("Reply", "", g)
            g = re.sub("\t", "", g)
            g = re.sub("\n", "", g)
            g = unclutter(g)
            g = re.search("[^\d]*", g).group()
    print(g)
except KeyboardInterrupt:
    sys.exit(1)
