# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import os, pdb
from Aplicacao                     import Aplicacao
from Entidades                     import Entidades
from ColunasEntidades              import ColunasEntidades
from PrimaryKeys                   import PrimaryKeys
from ForeignKeys                   import ForeignKeys

dicDataTypes={'CHAR':''
             ,'DATE':'date'
             ,'DECIMAL':'integer'
             ,'INTEGER':''integer''
             ,'TIMESTAMP':'datetime'
             ,'VARCHAR':'text'}

class CreateTables:

    def __init__(self, db, sessionId=None, cAppl=None, userName=None):
        self.db                            = db
        self.cAppl                         = cAppl or 0
        self.aplicacao                     = Aplicacao(self.db, self.cAppl)
        self.applId                        = self.aplicacao.getApplId()
        self.entidades                     = Entidades(self.db)
        self.colunasEntidades              = ColunasEntidades(self.db, self.cAppl)
        self.primaryKeys                   = PrimaryKeys(self.db)
        self.foreignKeys                   = ForeignKeys(self.db)
        self.sessionId                     = sessionId or '1'
        self.parametros                    = self.db.parametros
        self.parms                         = self.db(self.parametros).select()[0]
        self.log                           = os.path.join( '\\\\'
                                                         , '127.0.0.1'
                                                         , 'c$'
                                                         , self.parms.log
                                                         , "createTable_{}.log".format(self.sessionId))

        log                                = open(self.log, 'w')
        arq.close()
        self.dbApp                         = os.path.join( '\\\\'
                                                         , '127.0.0.1'
                                                         , 'c$'
                                                         , 'web2py'
                                                         , 'applications'
                                                         , self.applId
                                                         , ,'models'
                                                         , 'db.py'

    def createTables(self):
        dbApp       = open(self.dbApp, 'a')
        retEntidade = entidades.selectEntidadesBycodigoAplicacao(self.cAppl)
        if  not retEntidade[0]:
            return [0,'Ocorreu um erro na chamada de selectEntidadesBycodigoAplicacao.', retEntidade[1]]
        entidades   = retEntidade[1]

        for entidade in entidades:
            dbApp.write("db.define_table('{}'\n".format(entidade.nomeFisico))
            retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidade.id)
            if  not retColunasEntidades[0]:
                if  retColunasEntidades[1]:
                    return [0, retColunasEntidades[2]]
                else:
                    return [0, 'Nao existem colunas para esta Entidade']
            colunasEntidade  = retColunasEntidades[1]
            fp = ''
            lc = len(colunasEntidade)
            for n, col in enumerate(colunasEntidade):
                if  n + 1 = lc:
                    fp = ')\n'
                dbApp.write("{:>27}{}'){}\n".format(", Field('", col.colunas.columnName, fp))
            dbApp.write("{0:50}= db['{0}']\n\n".format(entidade.nomeFisico))


       return [1, 'Expecificacoes Geradas = ' + str(gerados)]

