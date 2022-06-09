#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
 
now = datetime.now()
 
def fetch_all_shows(channel: str):
    response = requests.get(f"https://www.allatvkanaler.se/tabla/{channel}/idag")
    soup = bs(response.text, 'html.parser')
    entries = soup.find_all('div', attrs={'class': 'sdr'})
    for entry in entries:
        items = entry.find('p').children
        start_str = next(items).strip()
        start = datetime.strptime(start_str, '%H:%M')
        title = next(items).text
        yield title, start
 
def fetch_current_show(channel: str, now: datetime):
    shows = fetch_all_shows(channel)
    i = 0
    for title, start in shows:
        if now >= start:
            try:
                next_title, next_start = next(shows)
                next_start_str = next_start.strftime('%H:%M')
            except StopIteration:
                next_start_str = None
            start_str = start.strftime('%H:%M')
            return title, start_str, next_start_str
 
title, start, end = fetch_current_show('svt1', now)
print(f"{title}. {start} ~> {end}")