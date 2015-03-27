# -*- coding: utf-8 -*-
#------------------------------------------------------------
# HarryTV Parser de torrent-tv.ru
# Version 0.1 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.HarryTV-wip/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.HarryTV-wip/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.HarryTV-wip/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.HarryTV-wip/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.HarryTV-wip/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'

# Общие = "General" (cat=5)
# Новостные = "Noticias" (cat=7)
# Развлекательные = "Entretenimiento" (cat=8)
# Детские = "Infantiles" (cat=1)
# Фильмы = "Cine" (cat=3)
# Спорт = "Deportes" (cat=4)
# Познавательные = "Documentales" (cat=6)
# Музыка = "Música" (cat=2)
# Мужские = "Para hombres" (cat=10)
# Региональные = "Regional" (cat=11)
# Религиозные = "religiosos" (cat=12)
# HD каналы = "Canales HD" (hd_channels.php)
# Каналы на модерации = "En moderación" (on_moderation.php)


def torrentvru(params):
    plugintools.log("[HarryTV-0.3.0].Torrent-TV.ru Playlist Sport Channels( "+repr(params))
    plugintools.add_item(action="", title = '[B][I][COLOR gold]Torrent-tv.ru[/B] [COLOR lightgreen]Acestream Sports Playlist[/I][/COLOR]', url = "", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)    

    url = params.get("url")
    plugintools.log("url= "+url)
    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    title = params.get("title")

    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Generalistas[/COLOR] [COLOR lightyellow][I](Общие)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=5", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Noticias[/COLOR] [COLOR lightyellow][I](Новостные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=7", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Entretenimiento[/COLOR] [COLOR lightyellow][I](Развлекательные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=8", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Infantiles[/COLOR] [COLOR lightyellow][I](Детские)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=1", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Cine[/COLOR] [COLOR lightyellow][I](Фильмы)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=3", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Deportes[/COLOR] [COLOR lightyellow][I](Спорт)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=4", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Documentales[/COLOR] [COLOR lightyellow][I](Познавательные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=6", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Música[/COLOR] [COLOR lightyellow][I](Музыка)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=2", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Para hombres[/COLOR] [COLOR lightyellow][I](Мужские)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=10", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Regionales[/COLOR] [COLOR lightyellow][I](Региональные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=11", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Religiosos[/COLOR] [COLOR lightyellow][I](Религиозные)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "cat=12", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]Canales HD[/COLOR] [COLOR lightyellow][I](HD каналы)[/I][/COLOR]', url = "http://torrent-tv.ru/channels.php", extra = "hd_channels.php", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    plugintools.add_item(action="torrentvru_section", title = '[COLOR white]En pruebas[/COLOR] [COLOR lightyellow][I](Каналы на модерации)[/I][/COLOR] [COLOR red](OFF)[/COLOR]', url = "http://torrent-tv.ru/on_moderation.php", extra = "on_moderation.php", thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = True, isPlayable = False)
    


def torrentvru_section(params):    
    url = params.get("url")
    id = params.get("extra")
    data = plugintools.read(url)
    
    match = plugintools.find_single_match(data, id+'(.*?)</ul></li>')
    #plugintools.log("match sports= "+match)
    matches = plugintools.find_multiple_matches(match, '<a href="(.*?)</li>')
    
    for entry in matches:
        #plugintools.log("matches= "+entry)
        entry = entry.split('"')
        url = 'http://www.torrent-tv.ru' + entry[0]
        url = url.strip()
        url = torrentvru_channels(url)
        url_fixed = entry[0].replace("/", "")
        thumbnail = torrentvru_getlogo(url_fixed, data)
        title = entry[1]
        title= title.replace("</a>", "")
        title= title.replace(">", "")
        title = title.strip()
        title_fixed = title.replace(" ", "+")
        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name=' + title_fixed
        #plugintools.log("url= "+url)
        plugintools.add_item(action="torrentvru_channels", title = title, url = url, thumbnail = 'http://1ttv.org/images/logo.png' , fanart = 'http://hdwallpappers.com/images/wallpapers/Allianz-Arena-Stadium-wallpaper.jpg' , folder = False, isPlayable = True)



def torrentvru_channels(url):
    plugintools.log("[HarryTV-0.3.0].Torrent-tv.ru getAcestream: "+url)

    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    match = plugintools.find_single_match(data, 'this.loadPlayer(.*?),{autoplay:')
    match = match.replace('"', "")
    match = match.replace("(", "")
    url = match.strip()
    #plugintools.log("ace= "+url)
    return url


def torrentvru_getlogo(url_fixed, data):
    plugintools.log("[HarryTV-0.3.0].Torrent-tv.ru getLogo: "+url_fixed)

    plugintools.log("data= "+data)
    matches = plugintools.find_multiple_matches(data, '<div style="width: 215px; height: 52px; display: table-cell; vertical-align: middle;"><a href="'+url_fixed+'(.*?)</a></div>')
    for entry in matches:
        plugintools.log("hola")
        plugintools.log("Buscando logo... "+entry)
    
        
        
