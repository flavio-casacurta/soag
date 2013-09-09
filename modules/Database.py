# -*- coding:utf-8
'''
   Created on 22/07/2013
   @author: C&C - HardSoft
'''
import sys, traceback

class Database(object):

    def __init__(self, db, cAppl=None, info=False):
        self.db = db
        self.cAppl = cAppl
        self.info = info
        self.database = self.db.database
        self.sgdb     = self.db.sgdb

    def getConfig(self):
        try:
            query = self.db((self.database.codigoAplicacao == self.cAppl)
                          & (self.sgdb.id == self.database.sgdbDB)).select().first()
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, 'SGDB nao localido para Aplicacao: {}'.format(self.cAppl)
        return query if query else (False, 'SGDB nao localido para Aplicacao: {}'.format(self.cAppl))

# vim: ft=python
