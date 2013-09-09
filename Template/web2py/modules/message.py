# -*- coding:utf-8
'''
   Created on 27/04/2013
   @author: C&C - HardSoft
'''
def msgGet(db, codigoMensagem):
    try:
        return '{} - {}'.format(codigoMensagem, db(db.mensagens.codigoMensagem==codigoMensagem).select()[0].descricao)
    except:
        return codigoMensagem
