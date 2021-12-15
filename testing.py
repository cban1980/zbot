#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup as bs
import re
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext
shit = requests.get('https://www.fittkramp.se/svordom/sv/slumpat-ord/').text
soup = bs(shit, 'html5lib')
maten = soup.findAll("div", class_ = "max75")
maten = str(maten)
my_list = str(maten).split("<em>")
print(cleanhtml(my_list[1].strip("]").lstrip()))