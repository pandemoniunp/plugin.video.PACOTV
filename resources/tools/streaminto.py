# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streaminto
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def streaminto(params):
    plugintools.log("[HarryTV-0.3.05].streaminto "+repr(params))

    url = params.get("url")
    
    try:
        if not url.startswith("http://streamin.to/embed-"):
            videoid = plugintools.find_single_match(url,"streamin.to/([a-z0-9A-Z]+)")
            page_url = "http://streamin.to/embed-"+videoid+".html"
    except:
        import traceback
        plugintools.info(traceback.format_exc())
    
    # Leemos el código web
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = plugintools.read(page_url , headers=headers)
    patron_flv = http://streamin.to/t5nqt4wrtktv'file: "([^"]+)"'    
    patron_jpg = 'image: "(http://[^/]+/)'
    #patron_rtmp = 'streamer: "([^"]+)"'

    #media_url = []
    try:
        host = plugintools.find_single_match(data, patron_jpg)
        plugintools.log("[streaminto.py] host="+host)
        flv_url = plugintools.find_single_match(data, patron_flv)
        plugintools.log("[streaminto.py] flv_url="+flv_url)
        flv = host+flv_url.split("=")[1]+"/v.flv"
        plugintools.log("[streaminto.py] flv="+flv)        
    except:
        plugintools.log("[streaminto.py] opcion 2")
        op = plugintools.find_single_match(data,'<input type="hidden" name="op" value="([^"]+)"')
        plugintools.log("[streaminto.py] op="+op)
        usr_login = ""
        id = plugintools.find_single_match(data,'<input type="hidden" name="id" value="([^"]+)"')
        plugintools.log("[streaminto.py] id="+id)
        fname = plugintools.find_single_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
        plugintools.log("[streaminto.py] fname="+fname)
        referer = plugintools.find_single_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
        plugintools.log("[streaminto.py] referer="+referer)
        hashstring = plugintools.find_single_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
        plugintools.log("[streaminto.py] hashstring="+hashstring)
        imhuman = plugintools.find_single_match(data,'<input type="submit" name="imhuman".*?value="([^"]+)"').replace(" ","+")
        plugintools.log("[streaminto.py] imhuman="+imhuman)
        
        import time
        time.sleep(10)
        
        # Lo pide una segunda vez, como si hubieras hecho click en el banner
        #op=download1&usr_login=&id=z3nnqbspjyne&fname=Coriolanus_DVDrip_Castellano_by_ARKONADA.avi&referer=&hash=nmnt74bh4dihf4zzkxfmw3ztykyfxb24&imhuman=Continue+to+Video
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
        headers.append(["Referer",page_url])
        data = plugintools.read( page_url , post=post, headers=headers )
        plugintools.log("data="+data)
    
        # Extrae la URL
        host = plugintools.find_single_match(data, patron_jpg)
        flv = host+plugintools.find_single_match(data, patron_flv).split("=")[1]+"/v.flv"
        plugintools("patron flv= "+flv)
        

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(flv)[-4:]+" [streaminto]",flv])
    
    for video_url in video_urls:
        logger.info("[streaminto.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    encontrados.add("http://streamin.to/embed-theme.html")
    encontrados.add("http://streamin.to/embed-jquery.html")
    encontrados.add("http://streamin.to/embed-s.html")
    encontrados.add("http://streamin.to/embed-images.html")
    encontrados.add("http://streamin.to/embed-faq.html")
    encontrados.add("http://streamin.to/embed-embed.html")
    encontrados.add("http://streamin.to/embed-ri.html")
    encontrados.add("http://streamin.to/embed-d.html")
    encontrados.add("http://streamin.to/embed-css.html")
    encontrados.add("http://streamin.to/embed-js.html")
    encontrados.add("http://streamin.to/embed-player.html")
    encontrados.add("http://streamin.to/embed-cgi.html")
    devuelve = []

    #http://streamin.to/z3nnqbspjyne
    patronvideos  = 'streamin.to/([a-z0-9A-Z]+)'
    plugintools.log("[streaminto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for entry in matches:
        url = "http://streamin.to/embed-"+entry+".html"
        if url not in encontrados:
            plugintools.log("URL= "+url)
        else:
            plugintools.log("URL duplicada"+url)

    #http://streamin.to/embed-z3nnqbspjyne.html
    patronvideos  = 'streamin.to/embed-([a-z0-9A-Z]+)'
    plugintools.log("[streaminto.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[streaminto]"
        url = "http://streamin.to/embed-"+match+".html"
        if url not in encontrados:
            plugintools.log("URL= "+url)
            devuelve.append( [ titulo , url , 'streaminto' ] )
            encontrados.add(url)
        else:
            plugintools.log("URL duplicada="+url)

    return devuelve
