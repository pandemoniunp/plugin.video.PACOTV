# -*- coding: utf-8 -*-
#------------------------------------------------------------
# HarryTV Parser de AnimeFLV.com
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



def animeflv(params):
    plugintools.log("[HarryTV 0.3.0].AnimeFLV")

    thumbnail = 'http://www.animeflv.com/temas/v1/css/img/logo_naranja.png'
    fanart = 'http://muryou-anime-wallpaper.net/wallpapers/tokimeki-memorial-only-love-170-wide800.jpg'
    cabecera(thumbnail, fanart)
    
    
    url = params.get("url")
    referer = 'http://www.animeflv.com/'
        
    data = gethttp_referer_headers(url, referer)
    #plugintools.log("data= "+data)
    
    # Paginación: Obtenemos número de páginas de resultados
    paginas = plugintools.find_single_match(data, '<div class="pagin">(.*?)</div>')
    actual = plugintools.find_single_match(paginas, '<span class="actual">(.*?)</span>')
    sig = plugintools.find_single_match(paginas, '<div class="pagin">(.*?)</div>')
    plugintools.log("Página siguiente: "+sig)
    num_pags = plugintools.find_multiple_matches(paginas, '<a href="([^"]+)')
    i = 1
    for entry in num_pags:
        pag_url = 'http://www.animeflv.com/animes/'+entry
        plugintools.log("num_pags= "+pag_url)
        i = i + 1

    plugintools.add_item(action="paginator", title='[COLOR lightyellow][I]Avanzar página [/COLOR][COLOR orange][B]('+actual+'/'+str(i)+')[/I][/B][/COLOR]', url = pag_url, extra = str(i), thumbnail = thumbnail , fanart = fanart, folder = True, isPlayable = False)

    lista_series(data, thumbnail, fanart)


def paginator(params):
    plugintools.log("Paginator: "+repr(params))

    url = params.get("url")
    thumbnail = params.get("thumbnail")
    num_total = params.get("extra")
    fanart = 'http://muryou-anime-wallpaper.net/wallpapers/tokimeki-memorial-only-love-170-wide800.jpg'
    referer = 'http://www.animeflv.com/'
        
    data = gethttp_referer_headers(url, referer)
    #plugintools.log("data= "+data)

    # Paginación de series
    paginas = plugintools.find_single_match(data, '<div class="pagin">(.*?)</div>')
    actual = plugintools.find_single_match(paginas, '<span class="actual">(.*?)</span>')
    plugintools.log("Pág. actual: "+actual)
    sig = plugintools.find_single_match(paginas, '<div class="pagin">(.*?)</div>')
    plugintools.log("Pág. siguiente: "+sig)
    num_pags = params.get("extra")
    plugintools.log("Núm. págs.= "+num_pags)
    sig = int(actual)+1
    page_next = 'http://www.animeflv.com/animes/?p='+str(sig)
    cabecera(thumbnail, fanart)
    if int(sig) <= int(num_total):
        plugintools.add_item(action="paginator", title='[COLOR lightyellow][I]Avanzar página [/COLOR][COLOR orange][B]('+actual+'/'+str(num_total)+')[/I][/B][/COLOR]', url = page_next, extra = num_total, thumbnail = thumbnail , fanart = fanart, folder = True, isPlayable = False)
    else:
        plugintools.add_item(action="", title='[COLOR lightyellow][I]Última página [/COLOR][COLOR orange][B]('+actual+'/'+str(num_total)+')[/I][/B][/COLOR]', url = page_next, extra = num_total, thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)

    data = gethttp_referer_headers(url, referer)
    lista_series(data, thumbnail, fanart)
    

# Esta función muestra la cabecera de "AnimeFLV" en el addon
def cabecera(thumbnail, fanart):
    thumbnail = 'http://www.animeflv.com/temas/v1/css/img/logo_naranja.png'
    fanart = 'http://muryou-anime-wallpaper.net/wallpapers/tokimeki-memorial-only-love-170-wide800.jpg'
    plugintools.add_item(action="", title= '[COLOR orange][B] A N I M E [/B][/COLOR][COLOR royalblue]F L V[/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    return thumbnail, fanart
    


def gethttp_referer_headers(url,referer):
    plugintools.log("HarryTV-0.3.0.gethttp_referer_headers ")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return body


def lista_series(data, thumbnail, fanart):
    anime = plugintools.find_multiple_matches(data, '<div class="aboxy_lista">(.*?)</div>')
    for entry in anime:
        plugintools.log("anime= "+entry)
        url_anime = plugintools.find_single_match(entry, '<a href="([^"]+)')
        url_anime = 'http://www.animeflv.com'+url_anime
        print 'url_anime',url_anime
        title_anime = plugintools.find_single_match(entry, 'title="([^"]+)')
        print 'title_anime',title_anime
        thumb_anime = plugintools.find_single_match(entry, 'data-original="([^"]+)')
        print 'thumb_anime',thumb_anime
        plugintools.add_item(action="animecaps", title=title_anime, url=url_anime, thumbnail = thumb_anime, fanart = fanart, folder = True, isPlayable = False)


def animecaps(params):
    plugintools.log("animecaps: "+repr(params))
    url = params.get("url")
    thumbnail = 'http://www.animeflv.com/temas/v1/css/img/logo_naranja.png'
    fanart = 'http://muryou-anime-wallpaper.net/wallpapers/tokimeki-memorial-only-love-170-wide800.jpg'
    #http://www.animeflv.com/ver/yamada-kun-to-7-nin-no-majo-1.html
    #http://www.animeflv.com/ova/yamada-kun-to-7-nin-no-majo.html
    url = url.replace(".html", "")
    url = url.replace("/ova/", "/ver/")
    url = url.replace("/anime/", "/ver/")
    url = url + '-1.html'
    #plugintools.log("URL capitulos: "+url)
    referer = 'http://www.animeflv.com/'
    data = gethttp_referer_headers(url, referer)
    getserver(data)
    opvid = plugintools.find_single_match(data, '<ul class="opvid">(.*)</ul>')
    #plugintools.log("opvid= "+opvid)
    option = plugintools.find_multiple_matches(data, '<li(.*?)</li>')
    lang_audio = ""
    lang_subs = ""
    
    for entry in option:
        #plugintools.log("entry= "+entry)
        if entry.find("Audio") >= 0:
            audio = plugintools.find_single_match(entry, '<img src="([^"]+)')
            if audio.endswith("JP.png") == True:
                thumb_audio = 'http://animeflv.com'+audio
                lang_audio = "Japonés"
                
        if entry.find("Subs") >= 0:
            subs = plugintools.find_single_match(entry, '<img src="([^"]+)')
            if subs.endswith("ES.png") == True:
                thumb_subs = 'http://animeflv.com'+subs
                lang_subs = "Castellano"
                
    if lang_audio != "":
        if lang_subs != "":
            plugintools.add_item(action="", title='[COLOR lightyellow][B]'+params.get("title")+'[/B][/COLOR]', thumbnail = thumb_audio, fanart = fanart, folder=False, isPlayable=False)
            plugintools.add_item(action="", title='[COLOR white][B]Audio: [/B][/COLOR][COLOR lightgreen]'+lang_audio+' [/COLOR][COLOR white][B]Subs: [/B][/COLOR][COLOR lightgreen]'+lang_subs+'[/COLOR]', thumbnail = thumbnail, fanart = fanart, folder=False, isPlayable=False)
    
    i = 1 
    for entry in option:
        #plugintools.log("entry= "+entry)
        server = plugintools.find_single_match(entry, 'title="([^"]+)')
        #plugintools.log("server= "+server)
        if server != "":
            title = '[COLOR white]Opción [B]'+str(i)+'[/B]: [I][COLOR orange]'+server+'[/COLOR][/I]'            
            plugintools.add_item(action="", title=title, url="", thumbnail = params.get("thumbnail") , fanart = fanart , folder=False, isPlayable=False)
            i = i + 1
        

    #<ul class="opvid"><li id="vid_363438" data-id="363438" data-audio="JP" title="Hyperion" class="ttip">Opción 1</li><li id="vid_363524" data-id="363524" data-audio="JP" title="Dailymotion" class="ttip">Opción 2</li><li id="vid_363521" data-id="363521" data-audio="JP" title="Zippyshare" class="ttip">Opción 3</li><li id="vid_363523" data-id="363523" data-audio="JP" title="Videobam" class="ttip">Opción 4</li><li id="vid_363532" data-id="363532" data-audio="JP" title="Nowvideo" class="ttip">Opción 5</li><li id="vid_363559" data-id="363559" data-audio="JP" title="Vkontakte" class="ttip">Opción 6</li><li id="vid_363531" data-id="363531" data-audio="JP" title="Novamov" class="ttip">Opción 7</li><li id="vid_363522" data-id="363522" data-audio="JP" title="Videoweed" class="ttip">Opción 8</li><li id="vid_363527" data-id="363527" data-audio="JP" title="Mp4upload" class="ttip">Opción 9</li><li id="vid_363529" data-id="363529" data-audio="JP" title="Netu" class="ttip">Opción 10</li></ul>
    

def getserver(data):
    plugintools.log("Getserver. "+data)

    match_vars = plugintools.find_single_match(data, 'var videos = {(.*?)}')
    plugintools.log("match_vars = "+match_vars)
    nowvid = plugintools.find_single_match(match_vars, 'nowvideo(.*?)">"]')
    plugintools.log("nowvid= "+nowvid)
    
    #var videos = {"365660":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","hyperion","<embed allowfullscreen=\"true\" src=\"\/archivos\/player.swf\" bgcolor=\"#000\" type=\"application\/x-shockwave-flash\" wmode=\"transparent\" pluginspage=\"http:\/\/www.macromedia.com\/go\/getflashplayer\" flashvars=\"file=\/video\/hyperion.php?key=ra7q1J7Z0rPCwI7A2L7ar6eb3pq%252Br72rzA%253D%253D&provider=video&abouttext=AnimeFLV Player&controlbar=bottom&stretching=exactfit&screencolor=000&plugins=backstroke-1,timeslidertooltipplugin-1\" height=\"463\" width=\"773\">"],"365661":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","dailymotion","<iframe frameborder=\"0\" width=\"773\" height=\"463\" src=\"\/\/www.dailymotion.com\/embed\/video\/x2d7bgo\" allowfullscreen><\/iframe>"],"365748":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","videobam","<iframe title=\"VideoBam video player\" type=\"text\/html\" frameborder=\"0\" scrolling=\"no\" width=\"773\" height=\"463\" src=\"http:\/\/videobam.com\/widget\/ZpcXc\/custom\/773\" allowFullScreen><\/iframe>"],"365665":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","nowvideo","<iframe width=\"773\" height=\"463\" frameborder=\"0\" src=\"http:\/\/embed.nowvideo.eu\/embed.php?v=121920b013bf1&width=773&height=463\" scrolling=\"no\"><\/iframe>"],"365667":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","vkontakte","<iframe src=\"http:\/\/vk.com\/video_ext.php?oid=273679768&id=170699525&hash=bc4823a209afee22&hd=2\" width=\"773\" height=\"463\" frameborder=\"0\"><\/iframe>"],"365666":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","novamov","<iframe style=\"overflow: hidden; border: 0; width: 773px; height: 463px\" src=\"http:\/\/embed.novamov.com\/embed.php?width=773&height=463&v=89b952584b5ce&px=1\" scrolling=\"no\"><\/iframe>"],"365662":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","videoweed","<iframe width=\"773\" height=\"463\" frameborder=\"0\" src=\"http:\/\/embed.videoweed.es\/embed.php?v=ee4e6517b1443&width=773&height=463\" scrolling=\"no\"><\/iframe>"],"365663":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","mp4upload","<iframe frameborder=\"0\" width=\"773\" height=\"463\" src=\"http:\/\/www.mp4upload.com\/embed-1805_1.mp4.html\" scrolling=\"no\" marginheight=\"0\" marginwidth=\"0\" allowfullscreen><\/iframe>"],"365664":["JP","ES","0","N\/D",null,"Desconocido",null,null,"24\/12\/2014","netu","<iframe src=\"http:\/\/hqq.tv\/player\/embed_player.php?vid=MYW7UN3YMKHA&autoplay=no\" height=\"463\" width=\"773\" allowfullscreen frameborder=\"0\" scrolling=\"no\"><\/iframe>"]};
