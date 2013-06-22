#!/usr/bin/python3.2
# -*-coding:Utf-8 -*

import httplib
from xmpp import *
import time,os
import json

# définition des constantes
CLE_API = 'blablabla'
JID_EHBOT = 'ehbot@eliteheberg.fr'
PASSWORD_EHBOT = 'toto'

# Connection au JID de ehbot
BOT=(JID_EHBOT, PASSWORD_EHBOT)
CONF=('eliteheberg@muc.eliteheberg.fr','')
LOGDIR='./'
PROXY={}

id = 0

def LOG(stanza,nick,text):
    ts=stanza.getTimestamp()
    if not ts:
        ts=stanza.setTimestamp()
        ts=stanza.getTimestamp()
    tp=time.mktime(time.strptime(ts,'%Y%m%dT%H:%M:%S'))+3600*3
    if time.localtime()[-1]: tp+=3600
    tp=time.localtime(tp)
    fold=stanza.getFrom().getStripped().replace('@','%')+'_'+time.strftime("%Y.%m",tp)
    day=time.strftime("%d",tp)
    tm=time.strftime("%H:%M:%S",tp)
    try: os.mkdir(LOGDIR+fold)
    except: pass
    fName='%s%s/%s.%s.html'%(LOGDIR,fold,fold,day)
    try: open(fName)
    except:
        open(fName,'w').write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xml:lang="ru-RU" lang="ru-RU" xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="content-type" />
        <title>%s logs for %s.%s.</title>
    </head>
    <body>
<table border="1"><tr><th>time</th><th>who</th><th>text</th></tr>
"""%(CONF[0],fold,day))
    text='<pre>%s</pre>'%text
    open(fName,'a').write((u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(tm,nick,text)).encode('utf-8'))
    print (u"<tr><td>%s</td><td>%s</td><td>%s</td></tr>\n"%(tm,nick,text)).encode('koi8-r','replace')
#    print time.localtime(tp),nick,text

def messageCB(sess,mess):
    nick=mess.getFrom().getResource()
    text=mess.getBody()
    LOG(mess,nick,text)

roster=[]
def presenceCB(sess,pres):
    nick=pres.getFrom().getResource()
    text=''
    if pres.getType()=='unavailable':
        if nick in roster:
            text=nick+unicode(' ÐÏËÉÎÕÌ ËÏÎÆÅÒÅÎÃÉÀ','koi8-r')
            roster.remove(nick)
    else:
        if nick not in roster:
            text=nick+unicode(' ÐÒÉÛ£Ì × ËÏÎÆÅÒÅÎÃÉÀ','koi8-r')
            roster.append(nick)


cl=Client(JID(BOT[0]).getDomain(),debug=[])
cl.connect(proxy=PROXY)
cl.RegisterHandler('message',"Disponible")
cl.RegisterHandler('presence',presenceCB)
cl.auth(JID(BOT[0]).getNode(),BOT[1])
p=Presence(to='%s/ehbot'%CONF[0])
p.setTag('x',namespace=NS_MUC).setTagData('password',CONF[1])
p.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})
cl.send(p)

i = 1

while i == 1:
    httpServ = httplib.HTTPConnection('http://www.eliteheberg.fr', 80)
    httpServ.connect()
    
    # Vérifier id repository
    httpServ.request('GET', '/projects/2/repository/commits?private_token=' + CLE_API)
    response = httpServ.getresponse()
    if response.status == httplibOk:
        data = response.read()

    #envoi du message
    if id_ancien == data['id']:
        if data:
            message = '[' + data['name'] + data['id'] + '] ' + data['message'] + ' par ' + data['author']['name']
        else:
            message  = 'Impossible de se connecter au serveur GIT.'
        cl.send(Message('eliteheberg@muc.eliteheberg.fr', message, typ='groupchat'))
    
    httpServ.close()
    
    # on attend 30 minutes avant de faire une autre vérification
    time.sleep(120)
    id_ancien = data['id']
