#!/usr/bin/env python
#-*- coding: utf-8 -*-
import pydle
import re
from bs4 import BeautifulSoup as bs
import sys
import os
import configparser
import ircfunctions
import time
import asyncio
import socket
import logging
# Read values from configuration file. 
config = configparser.ConfigParser()
config.read(os.path.expanduser('~/zbot/bot.conf'))
# Get connection values
src_ip = config.get('connection', 'source_ip', fallback='0.0.0.0')
src_port = config.getint('connection', 'source_port', fallback=0)
irc_server = config.get('connection', 'irc_server', fallback='eu.dal.net')
# Get values for channels and such when connected.
name = config.get('irc', 'nickname', fallback='zb0t')
rname = config.get('irc', 'rname', fallback='zb0t')
zbot_chans = config.get('irc', 'channels')

# This one wont work on a system with identd running.
uname = config.get('irc', 'username', fallback='zb0t')
# Variables for info and other things
zBotVersion = "1.7"
author = "zphinx"
ircHost = socket.getfqdn()
bots = ['DALnet', 'NickServ', 'ChanServ', 'Byis', 'PekingBot', 'Ekdahl']
# Set logging parameters
Log_Format = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "logfile.log",
                    filemode = "a",
                    format = Log_Format, 
                    level = logging.INFO)
logger = logging.getLogger()

###
# Non pydle functions.
### 

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

###
# Pydle class and functions.
###

class zbot(pydle.Client):
    """zbot, a stupid simple IRC bot"""
    async def on_connect(self):
        await self.join(zbot_chans)
        logger.info('Ansluten till {}. Joinade {}'.format(irc_server, zbot_chans))
        
    async def synable():
        await asyncio.sleep(1800)
        time.sleep(20)
        f = open("synset.txt", "w")
        f.write(str("on"))
        f.close()
    
    async def on_ctcp_version(self, by, target, contents):
        version = "zbot {}".format(zBotVersion)
        await self.ctcp_reply(by, 'VERSION', version)
        logger.info('{} skickade CTPCP version.'.format(by))

###
# on_channel_message event to handle commands. Functions pulled from ircfunctions.py
###

    async def on_channel_message(self, target, by, message):
        msg = message
        nick = by
        # So we dont collect short sentences.
        wordcount = msg.split()
        if len(wordcount) > 6:
            if nick not in bots:
                file = open("/home/zphinx/zbot/chat.txt", encoding='utf-8', mode='a')
                words = ' '.join(msg.split()[1:])
                file.write(words + "\n")
                file.close() 
        elif msg.lower().startswith('!bofh'):
            boffy = ircfunctions.bofh()
            await self.message(target, "{}: {}".format(nick, boffy))
            logger.info('{} anv??nde !bofh'.format(nick)) 
        if msg.lower().startswith('byis:'):
            chat = ircfunctions.chat()
            await self.message(target, "{}: {}".format(nick, chat))
            logger.info('{} samtalade med mig'.format(nick)) 
        elif msg.lower().startswith('!namnsdag'):
            namnsdag = ircfunctions.namnsdag()
            await self.message(target, "{}: {}".format(nick, namnsdag))
            logger.info('{} anv??nde !namnsdag'.format(nick)) 
        elif msg.lower().startswith('!synonym'):
            with open('synset.txt') as f:
                if 'on' in f.read():
                    arg = msg.split(' ')[1]
                    output = ircfunctions.synonym(arg)
                    await self.message(target, "{}: {}".format(nick, output))
                    logger.info('{} anv??nde !synonym f??r ordet {}'.format(nick, arg)) 
                elif 'off' in f.read():
                    pass
        elif "!synset" in msg:
            arg = msg.split(' ')[1]
            f = open("synset.txt", "w")
            f.write(str(arg))
            f.close()
            if 'on' not in arg:
                await zbot.synable()
        elif msg.lower().startswith('byis:'):
            if by.lower().startswith('gerryn'):
                gerr = ircfunctions.gerryn().rstrip()
                await self.message(target, "{}: {}".format(nick, gerr))
                logger.info('gerryn snackade skit med mig') 
            else:
                sadz = ircfunctions.sad()
                await self.message(target, "{}: {}".format(nick, sadz))
                logger.info('{} talade med mig.'.format(nick)) 
        elif msg.lower().startswith('!v??der'):
            arg = msg.split(' ', 1)[1:]
            arg2 = ' '.join(arg)
            arg2 = arg2.capitalize()
            vader = ircfunctions.vader(arg2)
            await self.message(target, "{}: {}".format(nick, vader))
            logger.info('{} anv??nde !v??der f??r staden {}.'.format(nick, arg2)) 
        elif by.lower().startswith('Byis'):
            pass
        elif msg.lower().startswith('!s??tkatt'):
            katt = ircfunctions.sotkatt()
            await self.message(target, "{}: {}".format(nick, katt))
            logger.info('{} anv??nde !s??tkatt'.format(nick)) 
        elif msg.lower().startswith('!nyheter'):
            feed = ircfunctions.nyheter()
            await self.message(target, "{}".format(feed))
            logger.info('{} anv??nde !s??tkatt'.format(nick)) 
        elif msg.lower().startswith('!s??thund'):
            katt = ircfunctions.sothund()
            await self.message(target, "{}: {}".format(nick, katt))
            logger.info('{} anv??nde !s??thund'.format(nick)) 
        elif msg.lower().startswith('!tr'):
            fran = msg.split(' ')[1]
            till = msg.split(' ')[2]
            mening = msg.partition(till)[2]
            oversattning = ircfunctions.tr(fran, till, mening)
            await self.message(target, "{}: {}".format(nick, oversattning))
        elif msg.lower().startswith('!mening'):
            arg = msg.split(' ')[1]
            mening = '(adsbygoogle = window.adsbygoogle || []).push({});'
            while mening ==  '(adsbygoogle = window.adsbygoogle || []).push({});':
                mening = ircfunctions.mening(arg)
            else:
                await self.message(target, "{}: {}".format(nick, mening))
                logger.info('{} anv??nde !mening for ordet {}.'.format(nick, mening)) 
        elif "open.spotify.com" in msg:
            arg = re.search("(?P<url>https?://[^\s]+)", msg).group("url")
            music = ircfunctions.spot(arg)
            music = music.replace('| Spotify', '')
            await self.message(target, "{}'s Spotify l??nk -> {}".format(nick, music))
            logger.info('{} l??nkade {} p?? spotify.'.format(nick, music)) 
        elif msg.lower().startswith('!sv'):
            await self.message(target, 'zbot v{}. Hostad p?? ({}). '.format(zBotVersion, ircHost))
            logger.info('{} anv??nde !sv'.format(nick)) 
        elif msg.lower().startswith('!hj??lp'):
            await self.message(target, 'Kommandon ??r !v??der <stad>, !tv <kanal>, !synonym <ord>, !mening <ord>, !bofh, !nyheter, !ipkoll <host>, !s??thund/!s??tkatt, !tr (??vers??ttning) <fr??n> <till> <mening>,!namnsdag och !lk f??r en lyckokaka.')
            logger.info('{} anv??nde !hj??lp'.format(nick)) 
        elif msg.lower().startswith('!help'):
            await self.message(target, 'Commands are !v??der <city>, !tv <channel>, !synonym <word>, !mening <word>, !bofh, !nyheter, !ipkoll <host>, !s??thund/!s??tkatt, !tr (translation) <from> <to> <sentence>,!namnsdag and !lk for a swedish fortune cookie.')
            logger.info('{} anv??nde !hj??lp'.format(nick)) 
        elif msg.lower().startswith('!ipkoll'):
            arg = msg.split(' ')[1]
            info = ircfunctions.ipkoll(arg)
            await self.message(target, "{}: {}".format(nick, info))
            logger.info('{} anv??nde !ipkoll p?? {}'.format(nick, arg))
        elif msg.lower().startswith('!lk'):
            lk = ircfunctions.lk()
            await self.message(target, "{}'s lyckokaka: {}".format(nick, lk))
        elif msg.lower().startswith('!tv'):
            kanaler = ["al-jazeera", "animal-planet", "atg-live", "axess-tv",
               "barnkanalen", "bbc-brit", "bbc-earth", "bbc-world-news",
               "bloomberg", "boomerang", "c-more-first", "c-more-first-hd",
               "c-more-fotboll", "c-more-golf", "c-more-hits", "c-more-hockey",
               "c-more-live", "c-more-live-2","c-more-live-3", "c-more-live-4",
               "c-more-live-5", "c-more-series", "c-more-sf", "c-more-stars",
               "cartoon-network", "cbs-reality", "cnbc", "cnn", "curiositystream", 
               "di-tv", "discovery-channel", "dr1", "dr2", "e", "euronews", 
               "eurosport", "eurosport-hd", "extreme-sports", "fashion-tv", 
               "fight-sports", "fuel-tv", "godare", "h2", "history-channel",
               "history-channel-hd", "horse-and-country", "kanal-10", "kanal-4",
               "kanal-5", "kanal-9", "kunskapskanalen", "mezzo", "mezzo-live-hd",
               "motorvision-tv", "mtv", "mtv-80s", "mtv-90s", "mtv-dance", "mtv-hits",
               "mtv-live-hd", "national-geo-wild", "national-geografic-hd",
               "national-geographic", "nautical-channel", "nick-jr", "nick-toons",
               "nickelodeon", "nrk-1", "nrk-2", "nrk-3", "outdoor-channel",
               "outtv", "paramount-network", "rt-news", "sjuan", "sky-news",
               "sportkanalen", "svt1", "svt1-hd", "svt2", "svt2-hd", "svt24",
               "tlc", "travel", "tv-finland", "tv-norge", "tv10", "tv12",
               "tv2-danmark", "tv3-norge", "tv4", "tv4-fakta", "tv4-film",
               "tv4-guld", "tv4-hd", "tv6", "tv8", "vh-1", "viasat-explore",
               "viasat-film-action", "viasat-film-family", "viasat-film-hits",
               "viasat-film-premier", "viasat-film-premier-hd", "viasat-fotboll",
               "viasat-golf", "viasat-history", "viasat-hockey", "viasat-motor",
               "viasat-nature", "viasat-series", "viasat-sport-extra",
               "viasat-premium", "viasat-ultra-hd", "yle-tv1", "yle-tv2", "tv3"]
            arg = msg.split(' ')[1]
            if arg == 'lista':
                await self.notice(nick, ", ".join(kanaler))
            elif not arg in kanaler:
                await self.message(target, "{}: Ej s??kbar/existerande kanal, skriv !tv lista f??r en (stor!) lista i notice".format(nick))
            else:
                tvnu = ircfunctions.tv(arg)
                await self.message(target, "{}: {}".format(nick, tvnu))
                logger.info('{} anv??nde !tv f??r kanalen {}.'.format(nick, arg, tvnu)) 

###
# Initialization of pydle object.
###
        
client = zbot(name, username=uname, realname=rname)
client.run(irc_server, tls=True, tls_verify=False, source_address=(src_ip, src_port))
client.handle_forever()
