# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import os, pdb
import utilities as utl
from Aplicacao import Aplicacao
from Entidades import Entidades
from Colunas import Colunas
from ColunasEntidades import ColunasEntidades
from ColunasEntidadesReferenciadas import ColunasEntidadesReferenciadas
from PrimaryKeys import PrimaryKeys
from ForeignKeys import ForeignKeys

dicDataTypes={'CHAR':None
             ,'DATE':"'date'"
             ,'DECIMAL':"'decimal'"
             ,'INTEGER':"'integer'"
             ,'TIMESTAMP':"'datetime'"
             ,'VARCHAR':"'text'"}

dicWidgets={'CHAR':1
           ,'DATE':None
           ,'DECIMAL':None
           ,'INTEGER':None
           ,'TIMESTAMP':None
           ,'VARCHAR':1}


class CreateTables:

    def __init__(self, db, sessionId=None, cAppl=None, userName=None):
        self.db               = db
        self.cAppl            = cAppl or 0
        self.aplicacao        = Aplicacao(self.db, self.cAppl)
        self.applId           = self.aplicacao.getApplId()
        self.entidades        = Entidades(self.db, cAppl=self.cAppl)
        self.colunas          = Colunas(db, cAppl=self.cAppl)
        self.colunasEntidades = ColunasEntidades(self.db, self.cAppl)
        self.ColEntRef        = ColunasEntidadesReferenciadas(self.db)
        self.primaryKeys      = PrimaryKeys(self.db)
        self.foreignKeys      = ForeignKeys(self.db)
        self.sessionId        = sessionId or '1'
        self.parametros       = self.db.parametros
        self.parms            = self.db(self.parametros).select()[0]

        App                   = os.path.join( '\\\\'
                                            , '127.0.0.1'
                                            , 'c$'
                                            , 'web2py'
                                            , 'applications'
                                            , self.applId
                                            , 'models')
        self.dbApp            = os.path.join( App
                                            , 'db.py')
        self.settings         = os.path.join( App
                                            , 'settings_local.db')

        Template              = os.path.join( '\\\\'
                                            , '127.0.0.1'
                                            , 'c$'
                                            , 'web2py'
                                            , 'applications'
                                            , self.parms.soag
                                            , 'Template'
                                            , 'web2py')
        self.dbTemplate       = os.path.join( Template
                                            , 'db.py')
        self.settingsTemplate = os.path.join( Template
                                            , 'settings_local.db')


    def createTables(self):

#####################################
#  tem que resolver o db.execute
#####################################

        sql = "DROP DATABASE {}".format(self.applId)
#        db.executesql(sql)

        sql = """
        CREATE DATABASE "{}"
          WITH ENCODING='UTF8'
               OWNER=postgres
               TEMPLATE=template0
               LC_COLLATE='Portuguese, Brazil'
               LC_CTYPE='C'
               CONNECTION LIMIT=-1
               TABLESPACE=pg_default;
        """.format(self.applId)
#        db.executesql(sql)

        settings = open(self.settings, 'w')
        settingsTemplate = open(self.settingsTemplate).readlines()
        settingsTemplate = utl.change({'@applId':self.applId}, settingsTemplate)
        settings.writelines(settingsTemplate)
        settings.close()

        dbApp = open(self.dbApp, 'w')
        dbApp.writelines(open(self.dbTemplate).readlines())

        retEntidade = self.entidades.selectEntidadesBycodigoAplicacao()
        if  not retEntidade[0]:
            return [0,'Ocorreu um erro na chamada de selectEntidadesBycodigoAplicacao.', retEntidade[1]]
        entidades = retEntidade[1]
        dicEntidades = {entidade.id: entidade for entidade in entidades}

        retColunas = self.colunas.selectColunasByCodigoAplicacao()
        colunas = retColunas[1]
        dicColunas = {col.id:col for col in colunas}

        gerados = 0

        for entidade in entidades:
#            pdb.set_trace()
            dbApp.write("\ndb.define_table('{}'\n".format(entidade.nomeFisico))
            retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidade.id)
            if  not retColunasEntidades[0]:
                if  retColunasEntidades[1]:
                    return [0, retColunasEntidades[2]]
                else:
                    return [0, 'Nao existem colunas para esta Entidade']
            gerados += 1
            colunasEntidade = retColunasEntidades[1]
            retPrimaryKeys = self.primaryKeys.selectPrimaryKeysByCodigoEntidade(entidade.id)
            if not retPrimaryKeys:
                return [0, retPrimaryKeys[1]]
            primaryKeys = retPrimaryKeys
            dicForeignKeys = self.foreignKeys.selectForeignKeysByCodigoEntidade(entidade.id)
            retColEntRef = self.ColEntRef.selectColunasEntidadesReferenciadasByCodigoEntidade(entidade.id)
            colEntRef = retColEntRef[1]
            lc = len(colunasEntidade)
            for n, col in enumerate(colunasEntidade):
                foreignKey = ''
                if  col.colunas.id in dicForeignKeys:
                    foreignKey = ', {}'.format(dicEntidades[dicForeignKeys[col.colunas.id][0]].nomeFisico)

                dttp = dicDataTypes[col.datatypes.descricao]
                if  dttp == "'decimal'":
                    dttp = ", 'decimal({},{})'".format(col.colunas.tamanhoColuna
                                                      ,col.colunas.decimais)
                elif not dttp:
                    dttp = ", length={}".format(col.colunas.tamanhoColuna)
                else:
                    dttp = ', {}'.format(dttp)
                fpar = ')\n' if  n + 1 == lc else ''
                dbApp.write("{:>24}{}'{}{}){}\n".format(", Field('", col.colunas.columnName, foreignKey, dttp, fpar))
            dbApp.write("{0:50}= db['{0}']\n\n".format(entidade.nomeFisico))
            dbApp.write('{:50}= False\n'.format('{}.id.writable'.format(entidade.nomeFisico)))
            for col in colunasEntidade:
                entCol = '{}.{}'.format(entidade.nomeFisico, col.colunas.columnName)
                if (col.colunas.id in primaryKeys and
                    primaryKeys[col.colunas.id] == 3):
                    dbApp.write('{:50}= False\n'.format('{}.writable'.format(entCol)))
                else:
                    dbApp.write("{:50}= '{}'\n".format('{}.label'.format(entCol)
                                                    ,col.colunas.label))
                    dbApp.write('{:50}= True\n'.format('{}.writable'.format(entCol)))

                    requires = '{}.requires'.format(entCol)
                    if  col.colunas.id in dicForeignKeys:
                        entRef = dicEntidades[dicForeignKeys[col.colunas.id][0]].nomeFisico
                        colName = dicColunas[dicForeignKeys[col.colunas.id][1]].columnName
                        colRef = colName
                        for cer in colEntRef:
                            if  (cer.colunasEntidadesReferenciadas.entidadeReferenciada ==
                                 dicForeignKeys[col.colunas.id][0]):
                                colRef = dicColunas[cer.colunasEntidadesReferenciadas.codigoColuna].columnName
                                break
                        dbApp.write('{:50}= IS_IN_DB(db, {}.{},\n'.format(requires, entRef, colName))
                        dbApp.write("{:>52}'%({})s', zero='-- Selecione --')\n".format('',colRef))

                    elif  col.colunasEntidades.ehNotNull:
                        dbApp.write('{:50}= IS_NOT_EMPTY()\n'.format(requires))
                    if  dicWidgets[col.datatypes.descricao]:
                        dbApp.write('if  widgets:\n')
                        dbApp.write('    {:46}= widgets.text\n'.format('{}.widget'.format(entCol)))

        dbApp.close()
        return [1, 'Entidades Geradas = ' + str(gerados)]

