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
# Read values from configuration file. 
config = configparser.ConfigParser()
config.read(os.path.expanduser('~/git/zbot/bot.conf'))
# Get connection values
src_ip = config.get('connection', 'source_ip', fallback='0.0.0.0')
src_port = config.getint('connection', 'source_port', fallback=0)
irc_server = config.get('connection', 'irc_server', fallback='irc.dal.net')
# Get values for channels and such when connected.
name = config.get('irc', 'nickname', fallback='zb0t')
rname = config.get('irc', 'rname', fallback='zb0t')
zbot_chans = config.get('irc', 'channels')
#This one wont work on a system with identd running.
uname = config.get('irc', 'username', fallback='zb0t')
# Variables for info and other things
zBotVersion = "1.4"
author = "zphinx"
ircHost = socket.getfqdn()


#Create the bot class.
class zbot(pydle.Client):
    """zbot, a stupid simple IRC bot"""
    async def on_connect(self):
        await self.join(zbot_chans)
        
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    
    async def synable():
        await asyncio.sleep(1800)
        time.sleep(20)
        f = open("synset.txt", "w")
        f.write(str("on"))
        f.close()

    async def on_channel_message(self, target, by, message):
        msg = message
        nick = by
        if msg.lower().startswith('!bofh'):
            boffy = ircfunctions.bofh()
            await self.message(target, "{}: {}".format(nick, boffy)) 
        elif "SaD" in nick:
            file = open("/home/zphinx/zbot/sad.txt", encoding='utf-8', mode='a')
            file.write(message + "\n")
            file.close() 
        elif msg.lower().startswith('!namnsdag'):
            namnsdag = ircfunctions.namnsdag()
            await self.message(target, "{}: {}".format(nick, namnsdag))
        elif msg.lower().startswith('!synonym'):
            with open('synset.txt') as f:
                if 'on' in f.read():
                    arg = msg.split(' ')[1]
                    output = ircfunctions.synonym(arg)
                    await self.message(target, "{}: {}".format(nick, output))
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
            else:
                sadz = ircfunctions.sad()
                await self.message(target, "{}: {}".format(nick, sadz))
        elif msg.lower().startswith('!väder'):
            arg = msg.split(' ', 1)[1:]
            arg2 = ' '.join(arg)
            arg2 = arg2.capitalize()
            vader = ircfunctions.vader(arg2)
            await self.message(target, "{}: {}".format(nick, vader))
        elif by.lower().startswith('Byis'):
            pass
        elif msg.lower().startswith('!sötkatt'):
            katt = ircfunctions.sotkatt()
            await self.message(target, "{}: {}".format(nick, katt))
        elif msg.lower().startswith('!söthund'):
            katt = ircfunctions.sothund()
            await self.message(target, "{}: {}".format(nick, katt))
        elif msg.lower().startswith('!mening'):
            arg = msg.split(' ')[1]
            mening = '(adsbygoogle = window.adsbygoogle || []).push({});'
            while mening ==  '(adsbygoogle = window.adsbygoogle || []).push({});':
                mening = ircfunctions.mening(arg)
            else:
                await self.message(target, "{}: {}".format(nick, mening))
        elif "open.spotify.com" in msg:
            arg = re.search("(?P<url>https?://[^\s]+)", msg).group("url")
            music = ircfunctions.spot(arg)
            music = music.replace('| Spotify', '')
            await self.message(target, "{}'s Spotify länk -> {}".format(nick, music))
        elif msg.lower().startswith('!sv'):
            await self.message(target, 'zbot v{}. Hostad på ({}). '.format(zBotVersion, ircHost))
        elif msg.lower().startswith('!hjälp'):
            await self.message(target, 'Kommandon är !väder, !synonym, !mening, !bofh, !ipkoll, !söthund/!sötkatt och !namnsdag.')
        elif msg.lower().startswith('!ipkoll'):
            arg = msg.split(' ')[1]
            info = ircfunctions.ipkoll(arg)
            await self.message(target, "{}: {}".format(nick, info))
            
client = zbot(name, username=uname, realname=rname)
client.run(irc_server, tls=True, tls_verify=False, source_address=(src_ip, src_port))
client.handle_forever()
