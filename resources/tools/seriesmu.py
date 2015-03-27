# -*- coding: utf-8 -*-
#------------------------------------------------------------
# HarryTV Parser de SeriesMu
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


def seriesmu(params):
    plugintools.log("[HarryTV 0.3.0].SeriesMu")
    
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




def seriesmu_capis(params):
    plugintools.log("SeriesMu_capis "+repr(params))
    
    url = params.get("url")
    referer = 'http://www.series.mu/'
    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)
    # ToDo: Card info summary (información de fecha de estreno, temporadas y número de capítulos)
    desc = plugintools.find_single_match(data, '<div class="card media-summary">(.*?)</div>')
    sinopsis = plugintools.find_single_match(desc, '<p>(.*?)</p>')
    cover_match = plugintools.find_single_match(data, '<div class="mini-poster"(.*?)</div>')
    cover = plugintools.find_single_match(cover_match, 'url(.*?);')
    cover = cover.replace("(", "").replace(")", "").strip()
    plugintools.log("cover= "+cover)
    plugintools.log("sinopsis= "+sinopsis)
    plugintools.add_item(action="", title='[COLOR orange][B]The Walking Dead[/B][/COLOR]', url = "", thumbnail = cover , fanart = fanart, folder = True, plot = sinopsis , isPlayable = False)

    match_temporadas = plugintools.find_single_match(data, '<div class="chapters chapters-seasons">(.*?)</ul>')
    match_episodios = plugintools.find_single_match(data, '<ul(.*?)</ul>')
    temps = plugintools.find_multiple_matches(match_temporadas, '<i class=icon-angle-down>(.*?)</li>')
    
    i = 1
    for entry in temps:
        label_temp = 'temp='+str(i)
        plugintools.log("label_temp= "+label_temp)
        match_capis = plugintools.find_multiple_matches(data, '<ul '+label_temp+'>(.*?)</ul>')
        plugintools.add_item(action="seriesmu_capis", title='[COLOR lightyellow]Temporada '+str(i)+'[/COLOR]', url = "", thumbnail = cover , fanart = fanart, folder = True, plot = sinopsis , isPlayable = False)
        j=1
        for matches in match_capis:
            plugintools.log("match_capis= "+matches)
            capis = plugintools.find_multiple_matches(matches, '<li>(.*?)</i>')
            for entri in capis:
                plugintools.log("entri= "+entri)
                title_capi = plugintools.find_single_match(entri, '</span>(.*?)</a>')
                url_capi = plugintools.find_single_match(entri, '<a href=(.*?)><span>')
                url_capi = 'http://series.mu'+url_capi+'/'
                plugintools.log("url_capi= "+url_capi)
                if j <= 9:
                    j = "0"+str(j)
                plugintools.add_item(action="enlacesmu", title=str(i)+'x'+str(j)+' '+title_capi, url = url_capi, thumbnail = cover , fanart = fanart , folder = True, isPlayable = False)
                j = int(j) + 1
        
        i = i + 1


def enlacesmu(params):
    plugintools.log("getlinksmu: "+repr(params))

    url = params.get("url")
    title = params.get("title")
    referer = 'http://www.series.mu/'
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    matches = plugintools.find_single_match(data, '<div class="sections episode-links online shown">(.*?)<div class="sections episode-links download">')
    capis = plugintools.find_multiple_matches(matches, '<div class="link-row">(.*?)</a>')
    for entry in capis:
        plugintools.log("entry= "+entry)
        url_link = plugintools.find_single_match(entry, '<a href=(.*?)target')
        url_link = url_link.replace('"',"").strip()
        url_link = 'http://series.mu'+url_link
        url_final = getlinkmu(url_link)
        if url_final.find("allmyvideos"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Allmyvideos][/I][/COLOR]'
            plugintools.add_item(action="allmyvideos", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif url_final.find("vidspot"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Vidspot][/I][/COLOR]'
            plugintools.add_item(action="allmyvideos", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif url_final.find("streamcloud"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Streamcloud][/I][/COLOR]'
            plugintools.add_item(action="allmyvideos", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif url_final.find("nowvideo"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Nowvideo][/I][/COLOR]'
            plugintools.add_item(action="nowvideo", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)            
        elif url_final.find("played.to"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Played.to][/I][/COLOR]'
            plugintools.add_item(action="playedto", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif url_final.find("vk.com"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Vk][/I][/COLOR]'
            plugintools.add_item(action="vk", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif url_final.find("tumi"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Tumi][/I][/COLOR]'
            plugintools.add_item(action="tumi", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif url_final.find("streamin.to"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][Streamin.to][/I][/COLOR]'
            plugintools.add_item(action="streaminto", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        elif url_final.find("veehd"):
            title_fixed = '[COLOR orange][B]'+title+'[/B][/COLOR] [COLOR lightyellow][I][VeeHD][/I][/COLOR]'
            plugintools.add_item(action="veehd", title = title_fixed, url = url_final , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        
        
     
        
def getlinkmu(url_link):
    plugintools.log("getlinkmu "+url_link)
    referer = 'http://series.mu/'
    data = gethttp_referer_headers(url_link,referer)
    plugintools.log("data= "+data)
    match = plugintools.find_single_match(data, '<h4 class="text_shadow">Video links</h4>(.*?)</div>')
    url_final = plugintools.find_single_match(match, 'value="([^"]+)')
    plugintools.log("URL final= "+url_final)
    return url_final
    
       

def gethttp_referer_headers(url,referer):
    plugintools.log("HarryTV-0.3.0.gethttp_referer_headers ")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);print response_headers
    return body

