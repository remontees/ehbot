#!/usr/bin/python2
# -*-coding:Utf-8 -*

import httplib2
from xmpp import *
import time,os
import json
import HTMLParser

# définition des constantes
CLE_API = ''
JID_EHBOT = ''
PASSWORD_EHBOT = ''

PROJECT = ''
PROJECT_TITLE = ''
PROJECT_OWNER = ''

PROJECT2 = ''
PROJECT2_TITLE = ''
PROJECT2_OWNER = ''

MUC_SEND = ''
URL_SERVER = ''


# Connection au JID de ehbot
BOT=(JID_EHBOT, PASSWORD_EHBOT)
CONF=(MUC_SEND,'')
LOGDIR='./'
PROXY={}

id = 0

roster=[]

cl=Client(JID(BOT[0]).getDomain(),debug=[])
cl.connect(proxy=PROXY)
cl.RegisterHandler('message',"Disponible")
#cl.RegisterHandler('presence',presenceCB)
cl.auth(JID(BOT[0]).getNode(),BOT[1])
p=Presence(to='%s/ehbot'%CONF[0])
p.setTag('x',namespace=NS_MUC).setTagData('password',CONF[1])
p.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})
cl.send(p)

nb_tours = 0
last_commit = None

# Instanciation du parser HTML
html_parser = HTMLParser.HTMLParser()

while nb_tours >= 0:
    httpServ = httplib2.Http(disable_ssl_certificate_validation=True)
    response, content = httpServ.request(URL_SERVER + '/api/v3/projects/' + PROJECT + '/repository/commits?private_token=' + CLE_API, "GET")
    response2, content2 = httpServ.request(URL_SERVER + '/api/v3/projects/' + PROJECT2 + '/repository/commits?private_token=' + CLE_API, "GET")
    if response.status == 200:
        data = json.loads(content)
        data2 = json.loads(content2)

        for ligne in data:
            if (ligne == data[0] and last_commit != ligne['id']):
                if nb_tours == 0:
                    message = 'Dernier commit'
                else:
                    message = 'Nouveau commit'
                
                message += ' de ' + ligne['author_name'] + ' : ' + html_parser.unescape(ligne['title']) + ' - ' + URL_SERVER + '/' + PROJECT_OWNER + '/' + PROJECT_TITLE + '/commit/' + ligne['id']
                    
                cl.send(Message('MUC_SEND', message, typ='groupchat'))
                last_commit = ligne['id']

            else:
                break
        
        for ligne2 in data2:
            if (ligne2 == data2[0] and last_commit2 != ligne2['id']):
                if nb_tours == 0:
                    message2 = 'Dernier commit'
                else:
                    message2 = 'Nouveau commit'
                
                message2 += ' de ' + ligne2['author_name'] + ' : ' + html_parser.unescape(ligne2['title']) + ' - ' + URL_SERVER + '/' + PROJECT2_OWNER + '/' + PROJECT2_TITLE + '/commit/' + ligne2['id']
                    
                cl.send(Message('MUC_SEND', message2, typ='groupchat'))
                last_commit2 = ligne2['id']

            else:
                break
                
        nb_tours = nb_tours + 1
        time.sleep(60)
