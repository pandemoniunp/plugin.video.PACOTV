# -*- coding: utf-8 -*-
#------------------------------------------------------------
# HarryTV Parser de Vipracing.org
# Version 0.1 (02.11.2014)
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
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import re,urllib,urllib2,sys
import plugintools,ioncube
from resources.tools.directwatch import *


icon = art + 'icon.png'
fanart = 'fanart.jpg'



def vipracing(params):
    plugintools.log("[HarryTV 0.3.0].Vipracing")

    thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg'
    fanart = 'http://wallpup.com/wp-content/uploads/2013/03/Soccer-Wallpaper.jpg'

    plugintools.add_item(action="", title= '[COLOR orange][B] V I P R A C I N G [/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    

    
    try:
        # Vamos a intentar obtener la programación de VipRacing
        vipr_schedule()
    except:
        # Si no conseguimos acceder a la programación, listamos canales disponibles
        plugintools.log("No existe la programación")
        vipr_channels(params)
        
        

def vipr_channels(params):

    thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg'
    fanart = 'http://wallpup.com/wp-content/uploads/2013/03/Soccer-Wallpaper.jpg'

    
    # var channels = JSON.parse('{"0":{"id":"1","name":"Opci\u00f3n 1","shortcut":"opcion-1","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"1":{"id":"3","name":"CBS Sports","shortcut":"espn","group":"0","new":"0","group_id":null,"group_name":null,"parent":null},"2":{"id":"8","name":"Opci\u00f3n 2","shortcut":"opcion-2","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"3":{"id":"9","name":"Opci\u00f3n 3","shortcut":"opcion-3","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"4":{"id":"10","name":"Opci\u00f3n 4","shortcut":"opcion-4","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"5":{"id":"26","name":"ESPN USA","shortcut":"espnusa","group":"0","new":"0","group_id":null,"group_name":null,"parent":null},"6":{"id":"40","name":"Opcion 5","shortcut":"opcion-5","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"7":{"id":"41","name":"Opcion 6","shortcut":"opcion-6","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"8":{"id":"42","name":"Opcion 8","shortcut":"opcion-8","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"9":{"id":"44","name":"Opcion-11","shortcut":"opcion-11","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"10":{"id":"45","name":"Opcion-12","shortcut":"opcion-12","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"11":{"id":"46","name":"Opcion-13","shortcut":"opcion-13","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"},"12":{"id":"50","name":"Roja 1","shortcut":"roja-1","group":"2","new":"0","group_id":"2","group_name":"Roja Directa","parent":"0"},"13":{"id":"51","name":"Roja 2","shortcut":"roja-2","group":"2","new":"0","group_id":"2","group_name":"Roja Directa","parent":"0"},"14":{"id":"52","name":"Roja 3","shortcut":"roja-3","group":"2","new":"0","group_id":"2","group_name":"Roja Directa","parent":"0"},"15":{"id":"54","name":"Roja 5","shortcut":"roja-5","group":"2","new":"0","group_id":"2","group_name":"Roja Directa","parent":"0"},"16":{"id":"55","name":"Roja 6","shortcut":"roja-6","group":"2","new":"0","group_id":"2","group_name":"Roja Directa","parent":"0"},"17":{"id":"58","name":"Opcion 7","shortcut":"opcion-7","group":"1","new":"0","group_id":"1","group_name":"Opciones","parent":"0"}}'),
    url = params.get("url")
    referer = 'http://www.vipracing.org'
    data = gethttp_referer_headers(url,referer)
    match = plugintools.find_single_match(data, 'var channels = (.*?)}}')
    plugintools.log("match= "+match)
    option = plugintools.find_multiple_matches(match, '"name":"([^"]+)')
    shortcut = plugintools.find_multiple_matches(match, '"shortcut":"([^"]+)')
    names = []
    shortcuts = []
    for entry in option:
        entry = entry.replace("\u00f3n","on")
        plugintools.log("Opción: "+entry)
        names.append(entry)
        url_channel = canal_vipracing(entry)
        plugintools.log("url_channel= "+url_channel)
        
    for entry in shortcut:
        plugintools.log("Nombre: "+entry)
        shortcuts.append(entry)

    i = 0
    while i < len(names):
        
        url = 'http://www.vipracing.org/channel/'+shortcuts[i]
        plugintools.log("url= "+url)
        plugintools.add_item(action="geturl_vipracing", title=names[i], url = url , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
        i = i + 1
        
    

def gethttp_referer_headers(url,referer):
    plugintools.log("HarryTV-0.3.0.gethttp_referer_headers ")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return body


def server_rtmp(url_vipracing):
    plugintools.log("[HarryTV-0.3.0].server_rtmp " + url_vipracing)
    
    if url_vipracing.find("iguide.to") >= 0:
        server = 'iguide'
        return server

    elif url_vipracing.find("direct2watch.com") >= 0:
        server = 'direct2watch'
        return server

    elif url_vipracing.find("freetvcast.pw") >= 0:
        server = 'freetvcast'
        return server    

    elif url_vipracing.find("9stream") >= 0:
        server = '9stream'
        return server

    elif url_vipracing.find("freebroadcast") >= 0:
        server = 'freebroadcast'
        return server 

    elif url_vipracing.find("goodgame.ru") >= 0:
        server = 'goodgame.ru'
        return server 

    elif url_vipracing.find("hdcast") >= 0:
        server = 'hdcast'
        return server  

    elif url_vipracing.find("sharecast") >= 0:
        server = 'sharecast'
        return server 

    elif url_vipracing.find("cast247") >= 0:
        server = 'cast247'
        return server 

    elif url_vipracing.find("castalba") >= 0:
        server = 'castalba'
        return server       

    elif url_vipracing.find("vaughnlive") >= 0:
        server = 'vaughnlive'
        return server 

    elif url_vipracing.find("gameso.tv") >= 0:
        server = 'gameso.tv'
        return server   

    elif url_vipracing.find("totalplay") >= 0:
        server = 'totalplay'
        return server     

    elif url_vipracing.find("shidurlive") >= 0:
        server = 'shidurlive'
        return server        
    
    elif url_vipracing.find("everyon") >= 0:
        server = 'everyon'
        return server  

    elif url_vipracing.find("iviplanet") >= 0:
        server = 'iviplanet'
        return server    

    elif url_vipracing.find("cxnlive") >= 0:
        server = 'cxnlive'
        return server      

    elif url_vipracing.find("ucaster") >= 0:
        server = 'ucaster'
        return server  

    elif url_vipracing.find("mediapro") >= 0:
        server = 'mediapro'
        return server  

    elif url_vipracing.find("veemi") >= 0:
        server = 'veemi'
        return server  

    elif url_vipracing.find("yukons") >= 0:
        server = 'yukons'
        return server      

    elif url_vipracing.find("janjua") >= 0:
        server = 'janjua'
        return server 

    elif url_vipracing.find("mips") >= 0:
        server = 'mips'
        return server 

    elif url_vipracing.find("zecast") >= 0:
        server = 'zecast'
        return server 

    elif url_vipracing.find("vertvdirecto") >= 0:
        server = 'vertvdirecto'
        return server 

    elif url_vipracing.find("9stream") >= 0:
        server = '9stream'
        return server 

    elif url_vipracing.find("filotv") >= 0:
        server = 'filotv'
        return server 

    elif url_vipracing.find("dinozap") >= 0:
        server = 'dinozap'
        return server    

    elif url_vipracing.find("ezcast") >= 0:
        server = 'ezcast'
        return server 

    elif url_vipracing.find("flashstreaming") >= 0:
        server = 'flashstreaming'
        return server 

    elif url_vipracing.find("shidurlive") >= 0:
        server = 'shidurlive'
        return server 

    elif url_vipracing.find("multistream") >= 0:
        server = 'multistream'
        return server 

    elif url_vipracing.find("playfooty") >= 0:
        server = 'playfooty'
        return server 

    elif url_vipracing.find("flashtv") >= 0:
        server = 'flashtv'
        return server 

    elif url_vipracing.find("04stream") >= 0:
        server = '04stream'
        return server 

    elif url_vipracing.find("vercosas") >= 0:
        server = 'vercosas'
        return server 

    elif url_vipracing.find("dcast") >= 0:
        server = 'dcast'
        return server 

    elif url_vipracing.find("playfooty") >= 0:
        server = 'playfooty'
        return server 

    elif url_vipracing.find("pvtserverz") >= 0:
        server = 'pvtserverz'
        return server 
    
    else:
        server = 'undefined'
        return server 
        

def canal_vipracing(canal):
    plugintools.log("[HarryTV-0.3.0].canal_vipracing "+canal)

    try:
        if canal.startswith("Opcion 1") == True:
            url = 'http://www.vipracing.tv/channel/opcion-1'
        elif canal.startswith("Opcion 2") == True:
            url = 'http://www.vipracing.tv/channel/opcion-2'
        elif canal.startswith("Opcion 3") == True:
            url = 'http://www.vipracing.tv/channel/opcion-3'
        elif canal.startswith("Opcion 4") == True:
            url = 'http://www.vipracing.tv/channel/opcion-4'
        elif canal.startswith("Opcion 5") == True:
            url = 'http://www.vipracing.tv/channel/opcion-5'
        elif canal.startswith("Opcion 6") == True:
            url = 'http://www.vipracing.tv/channel/opcion-6'
        elif canal.startswith("Opcion 7") == True:
            url = 'http://www.vipracing.tv/channel/opcion-7'
        elif canal.startswith("Opcion 8") == True:
            url = 'http://www.vipracing.tv/channel/opcion-8'
        elif canal.startswith("Opcion 9") == True:
            url = 'http://www.vipracing.tv/channel/opcion-9'
        elif canal.startswith("Opcion 10") == True:
            url = 'http://www.vipracing.tv/channel/opcion-10'
        elif canal.startswith("Opcion 11") == True:
            url = 'http://www.vipracing.tv/channel/opcion-11'
        elif canal.startswith("Opcion 12") == True:
            url = 'http://www.vipracing.tv/channel/opcion-12'
        else:
            url = "Nada"
            print "No se ha encontrado canal"

        if url:
            return url
    
    except:
        plugintools.log("Eror al parsear Vipracing")

    


def geturl_vipracing(params):
    plugintools.log("[HarryTV-0.3.0].GetURL_VipRacing "+repr(params))

    url=params.get("url")
    referer = 'http://vipracing.org/channel/opcion-1'  

    body = gethttp_referer_headers(url,referer)
    plugintools.log("body= "+body)
    if body.find("direct2watch.com/embed/") >= 0:
        url = plugintools.find_single_match(body, 'http://www.direct2watch.com/embed/(.*?)\"')
        print url
        url_prueba = plugintools.find_single_match(body, 'src=http://www.(.*?)\"')
        print url_prueba
        #rtmp://50.7.69.170:1935/direct2watch/_definst_/?xs=_we_dmh4OTZ5Y2ttcGF4cHE1fDE0MTcwMTQ3Njl8ODcuMjIwLjIxMC4yNTV8NTQ3NWRmZTEwZmZkY3xlMWNmYTU3ZmQ3MmZkY2YxMGYxYWNiNzU0ZGYzYjI5YzI0YWE3OWEw playpath=vhx96yckmpaxpq5 swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf live=1 pageUrl=http://www.direct2watch.com/embedplayer.php?width=653&height=410&channel=10&autoplay=true
        url = 'rtmp://watch1.direct2watch.com:1935/direct2watch/ swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf live=1 pageUrl=http://www.direct2watch.com/embedplayer.php?channel=' + url
        url = url.strip()
        plugintools.log("U R L = "+url)
        params["url"]=url
        directwatch(params)
        #plugintools.add_item(action="directwatch", title = '[COLOR green][direct2watch][/COLOR]', url=url, thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg', fanart = 'http://2.bp.blogspot.com/-AsAGdW3oDAU/UYofQDyna2I/AAAAAAAAO6s/VPWX-ck0oCk/s1600/Champions+League+Pictures+8.jpg' , folder = False, isPlayable=True)
        
    elif body.find("iguide") >= 0:
        url = plugintools.find_single_match(body, 'http://www.iguide.to/embed/(.*?)\"')
        url = 'http://www.iguide.to/embed/'+url
        pageurl = params.get("url")
        #ejem = gethttp_referer_headers(pageurl, entry)
        url = 'rtmp://50.7.69.234/iguide swfUrl=http://cdn1.iguide.to/player/secure_player_iguide_embed_token.swf pageUrl='+url+ ' token=#ed%h0#w18623jsda6523lDGDdmo'
        plugintools.log("U R L = "+url)
        server = server_rtmp(url)
        plugintools.add_item(action="play", title = "Canal "+str(i) +' [COLOR green][' + server + '][/COLOR]', url=url, thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg', fanart = 'http://2.bp.blogspot.com/-AsAGdW3oDAU/UYofQDyna2I/AAAAAAAAO6s/VPWX-ck0oCk/s1600/Champions+League+Pictures+8.jpg' , folder = False, isPlayable=True)
        i = i + 1
    elif body.find("gameso.tv") >= 0:
        params["url"]=url
        server = server_rtmp(url)
        playpath = plugintools.find_single_match(url, 'id=(.*)\&width')
        url = 'rtmp://go.gameso.tv/fasts playpath=' + playpath + ' swfUrl=http://www.gameso.tv/player/player_embed.swf pageUrl=' +url+ ' token=#ed%h0#w18723jdsahjkDHFbydmo'
        plugintools.log("U R L = "+url)
        plugintools.add_item(action="play", title = "[COLOR lightyellow]Canal "+str(i) +'[/COLOR][COLOR green] [' + server + '][/COLOR]', url=url, thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg', fanart = 'http://2.bp.blogspot.com/-AsAGdW3oDAU/UYofQDyna2I/AAAAAAAAO6s/VPWX-ck0oCk/s1600/Champions+League+Pictures+8.jpg' , folder = False, isPlayable=True)
        i = i + 1
    else:
        server = server_rtmp(url)
        plugintools.add_item(action="play" , title = "[COLOR lightyellow]Canal "+str(i) + '[/COLOR][COLOR green] [' + server + '][/COLOR]', url=url, thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg', fanart = 'http://2.bp.blogspot.com/-AsAGdW3oDAU/UYofQDyna2I/AAAAAAAAO6s/VPWX-ck0oCk/s1600/Champions+League+Pictures+8.jpg' , folder = False, isPlayable=True)
        i = i + 1


def menu2_vipracing(params):
    plugintools.log("[HarryTV-0.3.0].menu2_vipracing "+repr(params))
    
    menu2 = plugintools.find_single_match(body, '<map name="Map2" id="Map2">(.*?)</map>')
    plugintools.log("menu2= "+menu2)
    matches = plugintools.find_multiple_matches(menu2, 'href=\"(.*?)\"')    
    
    for entry in matches:
        referer='http://vipracing.tv/'
        plugintools.log("Canal: "+entry)
        
        try:
            # <script type="text/javascript" src="http://www.gameso.tv/embed.php?id=max22a2&width=653&height=410&autoplay=true"></script>
            canal = gethttp_referer_headers(entry,referer)
            url = plugintools.find_single_match(canal, 'http://www.direct2watch.com/embed/(.*?)\"')
            url = url.strip()
            ch = plugintools.find_single_match(url,'(.*?)\&')
            width = plugintools.find_single_match(url,'width=(.*?)\&')
            height = plugintools.find_single_match(url,'height=(.*?)\&')
            url_vipracing = 'rtmp://watch1.direct2watch.com:1935/direct2watch/ pageUrl=http://www.direct2watch.com/embedplayer.php?width='+width+'&height='+height+'&channel='+ch+'&autoplay=true swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf referer=' + entry
            plugintools.log("URL direct2watch: "+url_vipracing)
            server = server_rtmp(url_vipracing)
            plugintools.add_item(action="launch_rtmp", title = "[COLOR lightyellow]Canal "+str(i)+'[/COLOR][COLOR green] [' + server + '][/COLOR]', url=url_vipracing, thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg' , fanart = 'http://2.bp.blogspot.com/-AsAGdW3oDAU/UYofQDyna2I/AAAAAAAAO6s/VPWX-ck0oCk/s1600/Champions+League+Pictures+8.jpg' , folder = False, isPlayable=True)
            i = i + 1
            if url == "":
                url = plugintools.find_single_match(canal, 'src=\"http://www.gameso.tv/(.*?[^"]+)')
                plugintools.log("Somago encontrado: "+url)
                ch = plugintools.find_single_match(url,'(.*?)\&')
                width = plugintools.find_single_match(url,'width=(.*?)\&')
                height = plugintools.find_single_match(url,'height=(.*?)\&')                
                url_vipracing = 'rtmp://go.gameso.tv/fasts playpath='+playpath+' swfUrl=http://www.gameso.tv/player/player_embed.swf pageUrl='+url+' token=#ed%h0#w18723jdsahjkDHFbydmo'
                plugintools.log("URL somago: "+url_vipracing)
                server = server_rtmp(url_vipracing)
                plugintools.add_item(action="launch_rtmp", title = "[COLOR lightyellow]Canal "+str(i) +'[/COLOR][COLOR green] [' + server + '][/COLOR]', url=url_vipracing, thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg' , fanart = 'http://2.bp.blogspot.com/-AsAGdW3oDAU/UYofQDyna2I/AAAAAAAAO6s/VPWX-ck0oCk/s1600/Champions+League+Pictures+8.jpg' , folder = False, isPlayable=True)
                i = i + 1                
        except:
            pass

def vipr_schedule():

    url = 'http://vipracing.net/programacion/programacion.html'
    referer = 'http://www.vipracing.org'

    prog = gethttp_referer_headers(url,referer)
    plugintools.log("programación?= "+prog)

    # Obtenemos lista de canales y su clave
    canales_dict = {}
    canales = plugintools.find_single_match(prog, 'stm_bp(.*?)stm_ep')
    plugintools.log("programación?= "+canales)
    matches = plugintools.find_multiple_matches(canales, 'stm_aix\(\"(.*?)\);')
    for entry in matches:
        #plugintools.log("entry= "+entry)
        entry = entry.replace('"]', "")
        entry = entry.split(',')
        try:
            code_channel = entry[0].replace('"', "")
            name_channel = entry[3].replace('"', "")
            #plugintools.log("num_channel= "+code_channel)
            #plugintools.log("name_channel= "+name_channel)
            canales_dict[code_channel]=name_channel
            print canales_dict
        except:
            pass

    # Obtenemos fechas de la programación
    # stm_aix("p0i7","p0i6",[0,"LUNES","","",-1,-1,0,"","_self","","","arrow011.gif","icon_65.gif",0,15,0,"","",0,0]);
    date = plugintools.find_multiple_matches(prog, '\"p0i7\",\"p0i6\"(.*?)\);')
    for entry in date:
        plugintools.log("date= "+entry)        
        entry = entry.replace("0", "")
        entry = entry.replace("[", "")
        entry = entry.replace("]", "")
        entry = entry.replace('""', "")
        entry = entry.replace(",,", "")
        entry = entry.split('"')
        print entry[0]
        print entry[1]
        date = entry[1]
        plugintools.add_item(action="", title = '[COLOR red]'+date+'[/COLOR]' , url="" , thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg' , fanart = 'http://wallpup.com/wp-content/uploads/2013/03/Soccer-Wallpaper.jpg', folder = False, isPlayable = False )

        num_items = len(entry)
        i = 0
        while i < num_items :
            if entry[i].isupper() == True:
                date = entry[i]
                print date
                i = i + 1
                continue
            else:
                i = i + 1
                continue


    # Listamos eventos por día...
    eventos_dia = plugintools.find_single_match(prog, 'stm_ep(.*?)stm_em')
    eventos_dia = eventos_dia.split("stm_ep();")
    num_items = len(eventos_dia)

    i = 0
    while i < num_items:
        evento = eventos_dia[i]
        plugintools.log("EVENTO= "+evento)
        evento = evento.replace(".gif","")
        evento = evento.split('"')
        j = 0
        
        while j < len(evento):
            item_evento = evento[j].strip()
            if item_evento.find(":") >=0:
                evento_final = item_evento
                evento_final = evento_final.replace("\'", "'")
                plugintools.log("EVENTO= "+evento_final)
                j = j + 1
                while j < len(evento):
                    item_evento = evento[j]
                    item_evento = item_evento.strip()
                    if item_evento in canales_dict :
                        canal = canales_dict[item_evento]
                        plugintools.log("CANAL= "+canal)
                        # Función para buscar la URL del canal
                        url = canal_vipracing(canal)
                        plugintools.log("URL= "+url)
                        plugintools.add_item(action="geturl_vipracing", title = '[COLOR lightyellow]'+evento_final+' [/COLOR][COLOR orange][I]['+canal+'][/I][/COLOR]' , plot=canal , url=url , thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg' , fanart = 'http://wallpup.com/wp-content/uploads/2013/03/Soccer-Wallpaper.jpg', folder = False, isPlayable = True )
                        j = j + 1
                        continue
                    
                    else:
                        j = j + 1
                        continue

            elif item_evento.find(".") >=0:
                evento_final = item_evento
                evento_final = evento_final.replace("\'", "'")
                plugintools.log("EVENTO= "+evento_final)
                j = j + 1
                while j < len(evento):
                    item_evento = evento[j]
                    item_evento = item_evento.strip()
                    if item_evento in canales_dict :
                        canal = canales_dict[item_evento]
                        plugintools.log("CANAL= "+canal)
                        # Función para buscar la URL del canal
                        url = canal_vipracing(canal)
                        if url:
                            plugintools.log("URL= "+url)
                            plugintools.add_item(action="geturl_vipracing", title = '[COLOR lightyellow]'+evento_final+' [/COLOR][COLOR orange][I]['+canal+'][/I][/COLOR]' , plot=canal , url=url , thumbnail = 'http://oi58.tinypic.com/307qkj6.jpg' , fanart = 'http://wallpup.com/wp-content/uploads/2013/03/Soccer-Wallpaper.jpg', folder = False, isPlayable = True )
                            j = j + 1
                            continue
                        else:
                            j = j + 1
                            continue
                    else:
                        j = j + 1
                        continue                    
            else:
                j = j + 1
                continue
            
        i = i + 1

    
    
