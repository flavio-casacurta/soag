# -*- coding:utf-8
'''
   Created on 04/06/2013
   @author: C&C - HardSoft
'''
from utilities import *
from Aplicacao import Aplicacao

class CreateLoads(object):

    def __init__(self, db, cAppl=None, info=False):
        self.db = db
        self.cAppl = cAppl
        self.info = info
        self.applId = Aplicacao(self.db, self.cAppl).getApplId()
        self.parametros = self.db.parametros
        self.parms = self.db(self.parametros).select()[0]
        self.pathApp = os.path.join('\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', self.applId, 'models')
        self.pathTempl = os.path.join( '\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', self.parms.soag
                                      , 'Template', 'web2py', 'templates')

    def createLoads(self):
        try:
            template = open(os.path.join(self.pathTempl, 'msgLoad.py')).read()
            msgLoad = open(os.path.join(self.pathApp, 'msgLoad.py'), 'w')
            msgLoad.write(change({'@APPLID':self.applId}, template))
            msgLoad.close()
            template = open(os.path.join(self.pathTempl, 'usersLoad.py')).read()
            usrLoad = open(os.path.join(self.pathApp, 'usersLoad.py'), 'w')
            usrLoad.write(change({'@APPLID':self.applId}, template))
            usrLoad.close()
            return True, None
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
