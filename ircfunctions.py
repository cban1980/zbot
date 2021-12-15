#!/usr/bin/env python3
import requests
import markovify
from bs4 import BeautifulSoup as bs
import wikipedia
import os
import random
import re
import json
import cfscrape

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
    input = re.sub(r'Â«', '', input)
    input = re.sub(r'â', '', input)
    input = re.sub(r'â ¦', '', input)
    input = re.sub(r'â   ', '', input)
    
    return input

def namnsdag():
    namn = requests.get("https://www.dagensnamn.nu").text
    soup = bs(namn, 'html.parser')
    dagens = soup.find('h1').getText()
    return dagens


def sad():
    """markovify things sad say"""
    with open("/home/zphinx/zbot/sad.txt", "r", encoding="utf-8") as f:
        text = f.read()
        model = markovify.NewlineText(text, well_formed=False)
        chain = model.make_sentence(tries=100, state_size=120)
        f.close()
        return chain


def bofh():
    """Return random bofh quote"""
    url_data = requests.get('http://pages.cs.wisc.edu/~ballard/bofh/excuses').text
    soup = bs(url_data, 'html.parser')
    for line in soup:
        soppa = line.splitlines()
        soppa = random.choice(soppa)
    return soppa

def gerryn():
    "Snuskiga svar till gerryn."
    # Väldigt ful funktion, går säkert att fixa snyggare med bättre bs4 parse.
    html = requests.get('https://www.fittkramp.se/svordom/sv/slumpat-ord/').text
    soup = bs(html, 'html5lib')
    svar = soup.findAll("div", class_ = "max75")
    svar = str(svar)
    svarlista = str(svar).split("<em>")
    return cleanhtml(svarlista[1].strip("]").rstrip('\n'))
    
def mening(arg="None"):
    if arg == "None":
        return ("Var god ange ett ord...")
    else:
        html = requests.get("https://exempelmeningar.se/sv/{}".format(arg)).text
        soup = bs(html, 'html5lib')
        out = soup.find("div", {'class': 'tabs-container'})
        my_list = str(out).split("<hr/>")
        mening = random.choice(my_list)
        mening = swedify(mening)
        if mening == "None":
            return "Kunde ej hitta exempelmening för ordet {}! ".format(arg)
        else:
            return cleanhtml(mening).strip().lstrip()
        
def synonym(arg="None"):
    if arg == "None":
        return ("Kunde ej finna ord..")
    else:
        scraper = cfscrape.create_scraper()
        html = scraper.get("https://www.synonymer.se/sv-syn/{}".format(arg)).text
        soup = bs(html, 'html5lib')
        out = soup.find("div", {'class': 'body'})
        out = re.sub(r'[\ \n]{2,}', ' ', str(out))
        out = cleanhtml(out)
        out = re.sub(r'(\s*\|\s*)',' | ',out)
        out = " ".join(out.split())
        if "Nytt ord" in out:
            return("Kunde ej finna denna synonym.")
        else:
            split_string = out.split("Användarna", 1)
            return split_string[0]

def spot(arg):
    html = requests.get('{}'.format(arg)).text
    soup = bs(html, 'html5lib')
    return soup.title.string

def vader(arg):
    if arg:
        url = requests.get("http://wttr.in/{}?format=j1&lang=sv".format(arg)).text
        data = json.loads(url)
        besk = data['current_condition'][0]['lang_sv'][0]['value']
        feel = data['current_condition'][0]['FeelsLikeC']
        celcius = data['current_condition'][0]['temp_C']
        fukt = data['current_condition'][0]['humidity']
        precip = data['current_condition'][0]['precipMM']
        info = ("{} -> {}. Temp: {}C / Luftfuktighet: {}% / Nederbörd: {}MM".format(arg, besk, celcius, feel, fukt, precip))
        return info
    else:
        return ("Var god ange stad..")


def sotkatt():
    htmldata = requests.get('https://api.thecatapi.com/v1/images/search')
    katten = htmldata.json()
    bild = katten[0]['url']
    return bild


def sothund():
    htmldata = requests.get('https://dog.ceo/api/breeds/image/random')
    hunden = htmldata.json()
    bild = hunden['message']
    return bild