#!/usr/bin/python2
# -*-coding:Utf-8 -*

import httplib2
from xmpp import *
import time,os
import json
import HTMLParser

# définition des constantes
CLE_API = 'npB5qGysrKQsY5vRp9Vn'
JID_EHBOT = 'ehbot@eliteheberg.fr'
PASSWORD_EHBOT = 'toto'

PROJECT = '5'
PROJECT_TITLE = 'ehbot'
PROJECT_OWNER = 'remontees'

# Connection au JID de ehbot
BOT=(JID_EHBOT, PASSWORD_EHBOT)
CONF=('eliteheberg@muc.eliteheberg.fr','')
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
    response, content = httpServ.request('https://git.eliteheberg.fr/api/v3/projects/' + PROJECT + '/repository/commits?private_token=' + CLE_API, "GET")
    if response.status == 200:
        data = json.loads(content)
        increment = 0
        for ligne in data:
            if (increment == 0 and last_commit != ligne['id']):
                if nb_tours == 0:
                    message = 'Dernier commit'
                else:
                    message = 'Nouveau commit'
                
                message += ' de ' + ligne['author_name'] + ' : ' + html_parser.unescape(ligne['title']) + ' - https://git.eliteheberg.fr/' + PROJECT_OWNER + '/' + PROJECT_TITLE + '/commit/' + ligne['id']
                    
                cl.send(Message('eliteheberg@muc.eliteheberg.fr', message, typ='groupchat'))
                last_commit = ligne['id']
                increment = increment + 1
            else:
                break
        
        nb_tours = nb_tours + 1
        time.sleep(60)
