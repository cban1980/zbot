#!/usr/bin/env python
#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
html = requests.get('https://open.spotify.com/track/135Lf4Q0CzlMNfOxbEUsLH?si=ca6c1a4981764c71').text
soup = bs(html, 'html5lib')
print(soup.title.string)