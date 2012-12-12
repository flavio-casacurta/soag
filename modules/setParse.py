# -*- coding:utf-8
'''
   Created on 02/09/2011
   @author: C&C - HardSoft
'''
import os

def setParse(db, arg):
    db          = db
    parametros  = db.parametros
    parms       = db(parametros).select()[0]
    fn          = os.path.join( '\\\\'
                              , '127.0.0.1'
                              , 'c$'
                              , parms.log
                              , arg +'.tmp')
    arq         = open(fn, 'w')
    arq.write(arg)
    arq.close()
