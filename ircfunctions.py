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
import feedparser
from googletrans import Translator
ab_rss = "https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = cleantext.replace("&lt;", "<")
    cleantext = cleantext.replace("&gt;", ">")
    cleantext = cleantext.replace("&amp;", "&")
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

def tr(fran, till, mening):
    """Translation function."""
    translator = Translator()
    translation = translator.translate(mening, src=fran, dest=till)
    return translation.text

def chat():
    """return random markovify string when spoken to."""
    with open("/home/zphinx/zbot/chat.txt", "r", encoding="utf-8") as f:
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
    svarlista = svarlista[1].strip("]")
    return cleanhtml(svarlista)

def lk():
    "En lyckokaka."
    html = requests.get('http://www.fortunecookiemessage.com/').text
    soup = bs(html, 'html5lib')
    svar = soup.findAll("div", class_ = "quote")
    svar = cleanhtml(str(svar))
    translator = Translator()
    translation = translator.translate(svar, src="en", dest="sv")
    return translation.text.strip("[]")

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

def ipkoll(arg):
    """IP geolocation med https://ip-api.com/"""
    lander = {"AF":"Afghanistan",
"AX":"Åland",
"AL":"Albanien",
"DZ":"Algeriet",
"AS":"Amerikanska Samoa",
"AD":"Andorra",
"AO":"Angola",
"AI":"Anguilla",
"AQ":"Antarktis",
"AG":"Antigua och Barbuda",
"AR":"Argentina",
"AM":"Armenien",
"AW":"Aruba",
"AU":"Australien",
"AT":"Österrike",
"AZ":"Azerbajdzjan",
"BS":"Bahamas",
"BH":"Bahrain",
"BD":"Bangladesh",
"BB":"Barbados",
"BY":"Vitryssland",
"BE":"Belgien",
"BZ":"Belize",
"BJ":"Benin",
"BM":"Bermuda",
"BT":"Bhutan",
"BO":"Bolivia, plurinationell stat",
"BQ":"Bonaire, Sint Eustatius och Saba",
"BA":"Bosnien och Hercegovina",
"BW":"Botswana",
"BV":"Bouvet Island",
"BR":"Brasilien",
"IO":"Brittiska territoriet i Indiska oceanen",
"BN":"Brunei Darussalam",
"BG":"Bulgarien",
"BF":"Burkina Faso",
"BI":"Burundi",
"KH":"Kambodja",
"CM":"Kamerun",
"CA":"Kanada",
"CV":"Kap Verde",
"KY":"Caymanöarna",
"CF":"Centralafrikanska republiken",
"TD":"Tchad",
"CL":"Chile",
"CN":"Kina",
"CX":"Julön",
"CC":"Cocos (Keeling) Islands",
"CO":"Colombia",
"KM":"Komorerna",
"CG":"Kongo",
"CD":"Kongo, Demokratiska republiken",
"CK":"Cooköarna",
"CR":"Costa Rica",
"CI":"Elfenbenskusten",
"HR":"Kroatien",
"CU":"Kuba",
"CW":"Curaçao",
"CY":"Cypern",
"CZ":"Tjeckien",
"DK":"Danmark",
"DJ":"Djibouti",
"DM":"Dominica",
"DO":"Dominikanska republiken",
"EC":"Ecuador",
"EG":"Egypten",
"SV":"El Salvador",
"GQ":"Ekvatorialguinea",
"ER":"Eritrea",
"EE":"Estland",
"ET":"Etiopien",
"FK":"Falklandsöarna (Malvinas)",
"FO":"Färöarna",
"FJ":"Fiji",
"FI":"Finland",
"FR":"Frankrike",
"GF":"Franska Guyana",
"PF":"Franska Polynesien",
"TF":"Franska sydterritorier",
"GA":"Gabon",
"GM":"Gambia",
"GE":"Georgien",
"DE":"Tyskland",
"GH":"Ghana",
"GI":"Gibraltar",
"GR":"Grekland",
"GL":"Grönland",
"GD":"Grenada",
"GP":"Guadeloupe",
"GU":"Guam",
"GT":"Guatemala",
"GG":"Guernsey",
"GN":"Guinea",
"GW":"Guinea-Bissau",
"GY":"Guyana",
"HT":"Haiti",
"HM":"Heard Island och McDonald Islands",
"VA":"Heliga stolen (Vatikanstaten)",
"HN":"Honduras",
"HK":"Hong Kong",
"HU":"Ungern",
"IS":"Island",
"IN": "Indien",
"ID":"Indonesien",
"IR":"Iran, Islamiska republiken",
"IQ":"Irak",
"IE":"Irland",
"IM":"Isle of Man",
"IL":"Israel",
"IT":"Italien",
"JM":"Jamaica",
"JP":"Japan",
"JE":"Jersey",
"JO":"Jordan",
"KZ":"Kazakstan",
"KE":"Kenya",
"KI":"Kiribati",
"KP":"Korea, Demokratiska folkrepubliken",
"KR":"Korea, Republiken",
"KW":"Kuwait",
"KG":"Kirgizistan",
"LA":"Laos demokratiska republik",
"LV":"Lettland",
"LB":"Libanon",
"LS":"Lesotho",
"LR":"Liberia",
"LY":"Libyen",
"LI":"Liechtenstein",
"LT":"Litauen",
"LU":"Luxemburg",
"MO":"Macao",
"MK":"Makedonien, Republiken",
"MG":"Madagaskar",
"MW":"Malawi",
"MY":"Malaysia",
"MV":"Maldiverna",
"ML":"Mali",
"MT":"Malta",
"MH":"Marshallöarna",
"MQ":"Martinique",
"MR":"Mauretanien",
"MU":"Mauritius",
"YT":"Mayotte",
"MX":"Mexiko",
"FM":"Mikronesien, federerade stater av",
"MD":"Moldavien, Republiken",
"MC":"Monaco",
"MN":"Mongolien",
"ME":"Montenegro",
"MS":"Montserrat",
"MA":"Marocko",
"MZ":"Moçambique",
"MM":"Myanmar",
"NA":"Namibia",
"NR":"Nauru",
"NP":"Nepal",
"NL":"Nederländerna",
"NC":"Nya Kaledonien",
"NZ":"Nya Zeeland",
"NI":"Nicaragua",
"NE":"Niger",
"NG":"Nigeria",
"NU":"Niue",
"NF":"Norfolkön",
"MP":"Norra Marianaöarna",
"NO":"Norge",
"OM":"Oman",
"PK":"Pakistan",
"PW":"Palau",
"PS":"Palestinska territoriet, ockuperat",
"PA":"Panama",
"PG":"Papua Nya Guinea",
"PY":"Paraguay",
"PE":"Peru",
"PH":"Filippinerna",
"PN":"Pitcairn",
"PL":"Polen",
"PT":"Portugal",
"PR":"Puerto Rico",
"QA":"Qatar",
"RE":"Reunion",
"RO":"Rumänien",
"RU":"Rysska federationen",
"RW":"Rwanda",
"BL":"Saint Barthélemy",
"SH":"Sankt Helena, Ascension och Tristan da Cunha",
"KN":"Saint Kitts och Nevis",
"LC":"Saint Lucia",
"MF":"Saint Martin (fransk del)",
"PM":"Saint Pierre och Miquelon",
"VC":"Saint Vincent och Grenadinerna",
"WS":"Samoa",
"SM":"San Marino",
"ST":"Sao Tomé och Principe",
"SA":"Saudiarabien",
"SN":"Senegal",
"RS":"Serbien",
"SC":"Seychellerna",
"SL":"Sierra Leone",
"SG":"Singapore",
"SX":"Sint Maarten (nederländsk del)",
"SK":"Slovakien",
"SI":"Slovenien",
"SB":"Salomonöarna",
"SO":"Somalia",
"ZA":"Sydafrika",
"GS":"Sydgeorgien och södra Sandwichöarna",
"ES":"Spanien",
"LK":"Sri Lanka",
"SD":"Sudan",
"SR":"Surinam",
"SS":"Sydsudan",
"SJ":"Svalbard och Jan Mayen",
"SZ":"Swaziland",
"SE":"Sverige",
"CH":"Schweiz",
"SY":"Syrien",
"TW":"Taiwan, provinsen Kina",
"TJ":"Tadzjikistan",
"TZ":"Tanzania, Förenade republiken",
"TH":"Thailand",
"TL":"Östtimor",
"TG":"Togo",
"TK":"Tokelau",
"TO":"Tonga",
"TT":"Trinidad och Tobago",
"TN":"Tunisien",
"TR":"Turkiet",
"TM":"Turkmenistan",
"TC":"Turks- och Caicosöarna",
"TV":"Tuvalu",
"UG":"Uganda",
"UA":"Ukraina",
"AE":"Förenade Arabemiraten",
"GB":"Storbritannien",
"US":"USA",
"UM":"USA:s mindre avlägsna öar",
"UY":"Uruguay",
"UZ":"Uzbekistan",
"VU":"Vanuatu",
"VE":"Venezuela, Bolivariska republiken",
"VN":"Viet Nam",
"VG":"Jungfruöarna, brittiska",
"VI":"Jungfruöarna, USA",
"WF": "Wallis och Futuna",
"EH": "Västsahara",
"YE": "Jemen",
"ZM": "Zambia",
"ZW": "Zimbabwe"} 
    htmldata = requests.get('http://ip-api.com/json/{}'.format(arg))
    resp = htmldata.json()
    landskod = resp['countryCode']
    stad = resp['city']
    isp = resp['isp']
    land = lander[landskod]
    info = ("Land: {}. Stad: {}. Ägare: {}".format(land, stad, isp))
    return info

def tv(arg):
        url = requests.get('https://www.allatvkanaler.se/tabla/{}/idag'.format(arg)).text
        soup = bs(url, 'html.parser')
        data = soup.find('p',attrs={'class':'is-clearfix cur lead'})      
        if data is None:
            return ("Inget för tillfället... ")
        else:
            info = data.find_next_sibling('p')
            cur = data.find('b',attrs={'class':'fvs'})
            time = cleanhtml(str(data))
            show = cleanhtml(str(cur)) 
            info = cleanhtml(str(info))
            return "{}. {} ~> {}".format(show, time.split()[0],info)




def nyheter():
    ab_rss = "https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/"
    exp_rss = "https://feeds.expressen.se/nyheter/"
    dn_rss = "https://www.dn.se/rss/"
    ab_feed = feedparser.parse(ab_rss)
    exp_feed = feedparser.parse(exp_rss)
    dn_feed = feedparser.parse(dn_rss)
    abtitel = ab_feed.entries[0].title
    ablank = ab_feed.entries[0].link
    exptitle = exp_feed.entries[0].title
    explank = exp_feed.entries[0].link
    dntitle = dn_feed.entries[0].title
    dnlank = dn_feed.entries[0].link
    return """📰 Aftonbladet: {} ~> <🔗{}>
📰 Expressen: {} ~> <🔗{}>
📰 Dagens Nyheter: {} ~> <🔗{}>""".format(abtitel, ablank, exptitle, explank, dntitle, dnlank)
