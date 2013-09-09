# -*- coding:utf-8
'''
   Created on 17/06/2013
   @author: C&C - HardSoft
'''
import os, time
import cPickle as pickle
fileDump = os.path.join('\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', '@APPLID', 'private', 'usersDump.pickle')
usermtime = time.ctime(os.path.getmtime(fileDump))
cntl=db(db.controle).select()
ousermtime = cntl[0].usermtime if cntl else ''
if  ousermtime != usermtime:
    print 'atualizando usuarios'
    users = pickle.load(open(fileDump, 'rb'))
    for n, user in enumerate(users, 1):
        dbuser = db(db.auth_user.id == n).select()
        if  dbuser:
            dbuser = dbuser[0]
            if  dbuser.username ==  user.username:
                continue
            db(db.auth_user.id == n).update(username   = user.username
                                           ,first_name = user.first_name
                                           ,last_name  = user.last_name
                                           ,email      = user.email
                                           ,password   = user.password)
        else:
            db.auth_user.insert(username   = user.username
                               ,first_name = user.first_name
                               ,last_name  = user.last_name
                               ,email      = user.email
                               ,password   = user.password)
    if  cntl:
        db(db.controle).update(usermtime=usermtime)
    else:
        db.controle.insert(usermtime=usermtime)
    db.commit()
