# -*- coding:utf-8
'''
   Created on 04/06/2013
   @author: C&C - HardSoft
'''
import shutil
from utilities import *
from Aplicacao import Aplicacao

class CreateLayout(object):

    def __init__(self, db, cAppl=None, info=False):
        self.db         = db
        self.cAppl      = cAppl
        self.info = info
        self.aplicacao  = Aplicacao(self.db, self.cAppl)
        self.applId     = self.aplicacao.getApplId()
        self.applName   = self.aplicacao.getApplName()
        self.nomeLogo   = self.aplicacao.getNomeLogo()
        self.applLogo   = self.aplicacao.getApplLogo()
        self.parametros = self.db.parametros
        self.parms      = self.db(self.parametros).select()[0]

        self.logoAppOrigem = os.path.join( '\\\\'
                                         , '127.0.0.1'
                                         , 'c$'
                                         , 'web2py'
                                         , 'applications'
                                         , self.parms.soag
                                         , 'uploads') + os.sep

        self.logoAppDestino = os.path.join( '\\\\'
                                          , '127.0.0.1'
                                          , 'c$'
                                          , 'web2py'
                                          , 'applications'
                                          , self.applId
                                          , 'static'
                                          , 'images') + os.sep

        self.layoutApp    = os.path.join( '\\\\'
                                      , '127.0.0.1'
                                      , 'c$'
                                      , 'web2py'
                                      , 'applications'
                                      , self.applId
                                      , 'views'
                                      , 'layout.html')

        self.Template   = os.path.join( '\\\\'
                                      , '127.0.0.1'
                                      , 'c$'
                                      , 'web2py'
                                      , 'applications'
                                      , self.parms.soag
                                      , 'Template'
                                      , 'web2py'
                                      , 'templates'
                                      , 'layout.html')

    def createLayout(self):
        try:
            if  self.nomeLogo:
                applLogoOrigem = self.logoAppOrigem + self.applLogo
                ipp = iterInv(self.applLogo)
                pp = 0
                for n, p in enumerate(ipp):
                    if  p == '.':
                        pp = n
                        break
                logo = self.nomeLogo + '.' + self.applLogo[-pp:]
                applLogoDestino = self.logoAppDestino + logo
                shutil.copyfile(applLogoOrigem, applLogoDestino)
            else:
                logo = 'SeuLogo.png'

            layout = open(self.layoutApp, 'w')
            dic = {'@SISTEMA':'{} - {}'.format(self.applId, self.applName)
                  ,'@LOGO':logo}
            layout.write(change(dic, open(self.Template).read()))
            layout.close()
            return True, None
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
