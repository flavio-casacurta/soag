# -*- coding:utf-8
'''
   Created on 04/06/2013
   @author: C&C - HardSoft
'''
import pdb
from utilities import *
from Aplicacao import Aplicacao
from Entidades import Entidades

class CreateMenu(object):

    def __init__(self, db, cAppl=0, info=False):
        self.db = db
        self.cAppl = cAppl
        self.info = info
        self.aplicacao = Aplicacao(self.db, self.cAppl)
        self.applId = self.aplicacao.getApplId()
        self.entidades = Entidades(self.db, cAppl=self.cAppl)
        self.menu = self.db.menu
        self.parametros = self.db.parametros
        self.parms = self.db(self.parametros).select()[0]
        self.checkListPrototipo = self.db.checkListPrototipo

        self.menuApp    = os.path.join( '\\\\'
                                      , '127.0.0.1'
                                      , 'c$'
                                      , 'web2py'
                                      , 'applications'
                                      , self.applId
                                      , 'models'
                                      , 'menu2.py')

        self.Template   = os.path.join( '\\\\'
                                      , '127.0.0.1'
                                      , 'c$'
                                      , 'web2py'
                                      , 'applications'
                                      , self.parms.soag
                                      , 'Template'
                                      , 'web2py'
                                      , 'templates'
                                      , 'menu2.py')


    def createMenu(self):

        retEntidade = self.entidades.selectEntidadesBycodigoAplicacao()
        if  not retEntidade[0]:
            return [0,'Ocorreu um erro na chamada de selectEntidadesBycodigoAplicacao.', retEntidade[1]]
        entidades = retEntidade[1]
        dicEnt = {e.id:e.nomeFisico for e in entidades}

        try:
            query=self.db(self.menu.codigoAplicacao == self.cAppl).select(orderby=self.menu.id)
            dicParent = {q.id:q.descricao for q in query if q.url==0}
            lmenu = ''
            for q in query:
                if  q.parent == 1:
                    lmenu += "{:4}response.dtree.menu('{}')\n\n".format('', q.descricao)
                elif q.url == 0:
                    lmenu += "{:4}response.dtree.menu('{}', parent='{}')\n\n".format('', q.descricao
                                                                                       , dicParent[q.parent])
                else:
                    lmenu += "{:4}response.dtree.aplicacao('{}', '{}',\n".format('', dicParent[q.parent]
                                                                              , q.descricao)
                    url = ''.join(Capitalize(dicEnt[q.url].replace('_',' ')).split())
                    lmenu += "{:{}}URL(request.application, '{}', 'index'))\n\n".format('', 42 - len(url), url)

            template = open(self.Template).read()
            menu = open(self.menuApp, 'w')
            menu.write(change({'@menus\n':lmenu}, template))
            menu.close()
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        return self.atualizaCheckListPrototipo()

    def atualizaCheckListPrototipo(self):
        try:
            self.db(self.checkListPrototipo.codigoAplicacao == self.cAppl).update(menus = True)
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        self.db.commit()
        return True, None
