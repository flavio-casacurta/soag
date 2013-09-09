# -*- coding:utf-8
'''
   Created on 17/06/2013
   @author: C&C - HardSoft
'''

import os, time
import cPickle as pickle
fileDump = os.path.join('\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', '@APPLID', 'private', 'msgDump.pickle')
msgmtime = time.ctime(os.path.getmtime(fileDump))
cntl=db(db.controle).select()
omsgmtime = cntl[0].msgmtime if cntl else ''
if  omsgmtime != msgmtime:
    print 'atualizando mensagens'
    msgs = pickle.load(open(fileDump, 'rb'))
    for n, k in enumerate(sorted(msgs.keys()), 1):
        if  db(db.mensagens.id == n).select():
            db(db.mensagens.id == n).update(codigoMensagem = k, descricao = msgs[k])
        else:
            db.mensagens.insert(codigoMensagem = k, descricao = msgs[k])
    if  cntl:
        db(db.controle).update(msgmtime=msgmtime)
    else:
        db.controle.insert(msgmtime=msgmtime)
    db.commit()
