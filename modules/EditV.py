# -*- coding:utf-8
'''
   Created on 02/09/2011
   @author: C&C - HardSoft
'''
import os

def editV(db, dicEditV):
    db         = db
    parametros = db.parametros
    parms      = db(parametros).select()[0]
    fn         = os.path.join( '\\\\'
                             , '127.0.0.1'
                             , 'c$'
                             , parms.log
                             , 'editV.tmp')
    arq        = open(fn, 'w')
    for k, v in dicEditV.items():
        lista = k, v
        linha = lista[0] + ' ' + lista[1] + '\n'
        arq.write(linha)
    arq.close()
