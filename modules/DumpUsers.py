# -*- coding:utf-8
'''
   Created on 27/04/2013
   @author: C&C - HardSoft
'''
from utilities import *
from Aplicacao import Aplicacao

class DumpUsers(object):

    def __init__(self, db, cAppl=0, info=False):
        self.db = db
        self.cAppl = cAppl
        self.aplicacao = Aplicacao(self.db, self.cAppl).getApplId()
        parms = db(db.parametros.id==1).select()[0]
        self.userAplicacao = self.db.userAplicacao
        self.checkListPrototipo = self.db.checkListPrototipo
        self.fileDump = os.path.join('\\\\', '127.0.0.1', 'c$', parms.web2py, 'applications'
                                           , self.aplicacao, 'private', 'usersDump.pickle')

    def dumpUsers(self):
        try:
            users = self.db(self.userAplicacao.codigoAplicacao == self.cAppl).select()
            pic(users, self.fileDump)
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        return self.atualizaCheckListPrototipo()

    def atualizaCheckListPrototipo(self):
        try:
            self.db(self.checkListPrototipo.codigoAplicacao == self.cAppl).update(users = True)
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        self.db.commit()
        return True, None
