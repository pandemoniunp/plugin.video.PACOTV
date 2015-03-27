# -*- coding: utf-8 -*-
#------------------------------------------------------------
# HarryTV Parser de SeriesYonkis.sx
# Version 0.1 (02.11.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools

thumbnail = 'http://oi58.tinypic.com/1jwwo6.jpg'
fanart = 'http://st-listas.20minutos.es/images/2012-06/335200/list_640px.jpg?1368294762'
referer = 'http://www.seriesflv.com/'


def seriesyonkis(params):
    plugintools.log("[HarryTV 0.3.0].SeriesYonkis")
    
    url = 'http://www.seriesyonkis.sx/lista-de-series'
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url, referer)
    #plugintools.log("data= "+data)
    match_series = plugintools.find_single_match(data, '<div class="covers-box">(.*?)</ul>')
    #plugintools.log("listado= "+match_series)
    plugintools.add_item(action="", title = "[COLOR orange][B]Lista de series[/B][/COLOR]", url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)
    letra_activa = plugintools.find_single_match(match_series, '<li class="active">(.*?)</li>')
    url = plugintools.find_single_match(letra_activa, '<a href="([^"]+)')
    plugintools.log("url= "+url)
    title = url.replace("/lista-de-series/", "")
    plugintools.add_item(action="", title = title, url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)

    letras = plugintools.find_multiple_matches(match_series, '<li>(.*?)</a></li>')
    for entry in letras:
        url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        plugintools.log("url= "+url)
        title = url.replace("/lista-de-series/", "")
        plugintools.log("title= "+title)
        plugintools.add_item(action="lista_letra", title = title, url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)



def lista_letra(params):
    plugintools.log("[HarryTV 0.3.0].SeriesYonkis.Lista_letra")

    url = params.get("url")
    url = 'http://www.seriesyonkis.sx/'+url
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url, referer)
    #plugintools.log("data= "+data)
    match_series = plugintools.find_single_match(data, '<div class="covers-box">(.*?)<div id="sidebar-section">')
    plugintools.log("listado= "+match_series)

    # Paginador de series por letra (botón "siguiente")
    paginador_next(data)

    # Listado de series
    lista_series(match_series)



# Listado de series
def lista_series(match_series):
    serie = plugintools.find_multiple_matches(match_series, '<li>(.*?)</a></li>')
    for entry in serie:
        url = plugintools.find_single_match(entry, 'href="([^"]+)')
        url = 'http://www.seriesyonkis.sx'+url
        plugintools.log("url= "+url)
        title_serie = plugintools.find_single_match(entry, 'title="([^"]+)').strip()
        plugintools.log("title_serie= "+title_serie)
        if title_serie != "":
            plugintools.log("url_serie= "+url)
            plugintools.add_item(action="serie_capis", title = title_serie, url = url, thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)    
        

# Paginador de series por letra
def paginador_next(data):    
    match_paginas = plugintools.find_single_match(data, 'class="paginator">(.*?)<div id="sidebar-section">')
    plugintools.log("match_paginas= "+match_paginas)
    pag_actual = plugintools.find_single_match(match_paginas, '<strong>(.*?)</strong>')
    plugintools.log("pag_actual = "+str(pag_actual))
    num_pags = plugintools.find_multiple_matches(match_paginas, '<a(.*?)</a>')
    i = 0
    for entry in num_pags:
        i = i + 1
    plugintools.log("Núm. páginas= "+str(i))
    next = int(pag_actual) + 1
    plugintools.add_item(action="", title= '[COLOR lightyellow][I]Siguiente (Pág. '+str(next)+')[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False)    




def serie_capis(params):
    plugintools.log("serie_capis "+repr(params))
    url = params.get("url")
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url,referer)
    #Carátula
    cover = plugintools.find_single_match(data, '<img src="([^"]+)')
    match_temporadas = plugintools.find_single_match(data, '<div id="section-content">(.*?)</ul>')
    temps = plugintools.find_multiple_matches(match_temporadas, '<h3 class="season"(.*?)</li>')
    for entry in temps:
        capis = plugintools.find_multiple_matches(entry, '<td class="episode-title">(.*?)</td>')
        for entri in capis:
            url_cap = plugintools.find_single_match(entri, '<a href="([^"]+)')
            url_cap = 'http://www.seriesyonkis.sx'+url_cap
            plugintools.log("url_cap= "+url_cap)
            num_cap = plugintools.find_single_match(entri, '<strong>(.*?)</strong>')
            num_cap = num_cap.strip()
            plugintools.log("num_cap= "+num_cap)
            title_cap = plugintools.find_single_match(entri, '</strong>(.*?)</a>')
            title_cap = title_cap.strip()
            plugintools.log("title_cap= "+title_cap)
            title_capi = '[COLOR orange][B]'+num_cap+'[/B][COLOR white]'+title_cap+'[/COLOR]'.strip()
            title_fixed = num_cap + title_cap
            title_fixed = title_fixed.strip()
            plugintools.add_item(action="enlaces_capi", title=title_capi, url = url_cap, thumbnail = cover , fanart = fanart, folder = True, plot = title_fixed , isPlayable = False)




def enlaces_capi(params):
    plugintools.log("enlaces_capi "+repr(params))

    url = params.get("url")
    title_fixed = params.get("plot")
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)
    matches = plugintools.find_single_match(data, '<h2 class="header-subtitle veronline">(.*?)</table>')
    match_veronline = plugintools.find_single_match(matches, '<tbody>(.*?)</tbody>')
    match_links = plugintools.find_multiple_matches(match_veronline, '<tr>(.*?)</tr>')
    for entry in match_links:
        plugintools.log("entry= "+entry)
        title_url = plugintools.find_single_match(entry, 'title="([^"]+)')
        page_url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        page_url = 'http://www.seriesyonkis.sx/'+page_url
        url_final = getlink(page_url)
        if url_final.find("tumi") >= 0:
            desc = '[Tumi]'
            plugintools.add_item(action="tumi", title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR]' , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        elif url_final.find("streamin.to") >= 0:
            desc = '[Streamin.to]'
            plugintools.add_item(action="streaminto", title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR]' , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        elif url_final.find("vidspot") >= 0:
            desc = '[Vidspot]'
            plugintools.add_item(action="vidspot", title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR]' , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        elif url_final.find("allmyvideos") >= 0:
            desc = '[allmyvideos]'
            plugintools.add_item(action="allmyvideos", title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR]' , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        elif url_final.find("streamcloud") >= 0:
            desc = '[Streamcloud]'
            plugintools.add_item(action="streamcloud", title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR]' , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        elif url_final.find("nowvideo.sx") >= 0:
            desc = '[Nowvideo]'
            plugintools.add_item(action="nowvideo", title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR]' , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        elif url_final.find("veehd") >= 0:
            desc = '[VeeHD]'
            plugintools.add_item(action="veehd", title = title_fixed + ' [COLOR orange][I]'+desc+'[/I][/COLOR]' , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        
        #server_url = plugintools.find_single_match(entry, 'alt="([^"]+)')
        #plugintools.add_item(action="", title = title_fixed , url = url_final , thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)

        
        
def getlink(page_url):
    plugintools.log("getlink "+page_url)
    referer = 'http://www.seriesyonkis.sx/'
    data = gethttp_referer_headers(page_url,referer)
    match = plugintools.find_single_match(data, '<table class="episodes full-width">(.*?)</table>')
    url_final = plugintools.find_single_match(match, '<a href="([^"]+)')
    plugintools.log("URL final= "+url_final)
    return url_final
    
       

def gethttp_referer_headers(url,referer):
    plugintools.log("HarryTV-0.3.0.gethttp_referer_headers ")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body

