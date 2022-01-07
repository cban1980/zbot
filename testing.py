#!/usr/bin/env python3
import re
import requests
from bs4 import BeautifulSoup as bs
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    " ".join(map(str, cleantext))
    return cleantext

url = requests.get('https://www.allatvkanaler.se/tabla/cnn/idag').text
soup = bs(url, 'html.parser')
data = soup.find('p',attrs={'class':'cur lead'})
if data is None:
    print("Inget för tillfället..")
else:
    cur = data.find('b',attrs={'class':'fvs'})
    #print(cur)
    #print(cleanhtml(str(cur)))
    time = cleanhtml(str(data))
    show = cleanhtml(str(cur)) 
    print("{} började: {}".format(show, time.split()[0]))
