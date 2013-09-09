# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import os
import sqlalchemy
from utilities import *
from ValidationColumnsDb import *
from Aplicacao import Aplicacao
from Entidades import Entidades
from Colunas import Colunas
from ColunasEntidades import ColunasEntidades
from ColunasEntidadesReferenciadas import ColunasEntidadesReferenciadas
from PrimaryKeys import PrimaryKeys
from ForeignKeys import ForeignKeys
from OrigemColunasAplicacao import OrigemColunasAplicacao
from RegrasColunas import RegrasColunas
from Mensagens import Mensagens
from Database import Database

dicDataTypes={'CHAR':None
             ,'DATE':"'date'"
             ,'DECIMAL':"'decimal'"
             ,'NUMERIC':"'decimal'"
             ,'INTEGER':"'integer'"
             ,'TIMESTAMP':"'datetime'"
             ,'VARCHAR':"'text'"}

dicWidgets={'CHAR':1
           ,'DATE':None
           ,'DECIMAL':1
           ,'NUMERIC':1
           ,'INTEGER':None
           ,'TIMESTAMP':None
           ,'VARCHAR':1}

dicNatureza={'CHAR':(None, None)
            ,'DATE':('IS_DATE', 'DT')
            ,'DECIMAL':('IS_DECIMAL_IN_RANGE', 'NU')
            ,'NUMERIC':('IS_DECIMAL_IN_RANGE', 'NU')
            ,'INTEGER':('IS_INT_IN_RANGE', 'NU')
            ,'TIME':('IS_TIME', 'TM')
            ,'TIMESTAMP':('IS_DATETIME', 'TS')
            ,'VARCHAR':(None, None)}

modeloDB = {0:'Soag'
           ,1:'legacy'}


class CreateDB:

    def __init__(self, db, cAppl=None, createDataBase=False, info=False):
        self.db = db
        self.cAppl = cAppl
        self.createDataBase = createDataBase
        self.info = info
        self.aplicacao = Aplicacao(self.db, self.cAppl)
        self.applId = self.aplicacao.getApplId()
        self.modeloDb = self.aplicacao.getModeloDb()
        self.entidades = Entidades(self.db, cAppl=self.cAppl)
        self.colunas = Colunas(db, cAppl=self.cAppl)
        self.colunasEntidades = ColunasEntidades(self.db, self.cAppl)
        self.ColEntRef = ColunasEntidadesReferenciadas(self.db)
        self.primaryKeys = PrimaryKeys(self.db)
        self.foreignKeys = ForeignKeys(self.db)
        self.OrigemColunasAplicacao = OrigemColunasAplicacao(self.db)
        self.regrasColunas = RegrasColunas(self.db)
        self.mensagens = Mensagens(self.db, cAppl=self.cAppl)
        self.parametros = self.db.parametros
        self.parms = self.db(self.parametros).select()[0]
        self.checkListPrototipo = self.db.checkListPrototipo
        self.database = Database(db, cAppl=self.cAppl)
        self.databaseCreated = False

        App = os.path.join( '\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', self.applId)

        self.dbApp = os.path.join(App, 'models', 'db.py')

        self.settings = os.path.join(App, 'models', 'settings_local.db')

        self.databases = os.path.join(App, 'databases')

        Template = os.path.join( '\\\\', '127.0.0.1', 'c$', 'web2py', 'applications'
                               , self.parms.soag, 'Template', 'web2py', 'models')

        self.dbTemplate = os.path.join( Template, 'db.py')

        self.settingsTemplate = os.path.join( Template, 'settings_local.db')

    def createDB(self):

        try:
            if  self.createDataBase:
                if  modeloDB[self.modeloDb] == 'Soag':
                    command = 'dropdb --username=postgres -w {}'.format(self.applId)
                    try:
                        os.system(command)
                    except:
                        pass

                    command = 'createdb --username=postgres -w {}'.format(self.applId)
                    os.system(command)
                else:
                    retorno, returned = self.tryEngine()
                    if  not retorno:
                        return retorno, returned
                    engine = returned

                    retorno, returned = self.metaSchema(engine)
                    if  not retorno:
                        return retorno, returned
                    schm = returned

                    for tbl in [u'controle'
                               ,u'mensagens'
                               ,u'auth_cas'
                               ,u'auth_event'
                               ,u'auth_permission'
                               ,u'auth_membership'
                               ,u'auth_group'
                               ,u'auth_user']:
                        try:
                            table = schm.tables[tbl]
                            table.drop(engine)
                        except:
                            pass

            settings = open(self.settings, 'w')
            settingsTemplate = open(self.settingsTemplate).readlines()
            settingsTemplate = change({'@applId':self.applId}, settingsTemplate)
            settings.writelines(settingsTemplate)
            settings.close()

            if  self.createDataBase:
                try:
                    shutil.rmtree(self.databases)
                except:
                    pass
                os.mkdir(self.databases)
                self.databaseCreated = True

            dbApp = open(self.dbApp, 'w')
            dbApp.writelines(open(self.dbTemplate).readlines())

            retEntidade = self.entidades.selectEntidadesBycodigoAplicacao()
            if  not retEntidade[0]:
                return False, retEntidade[1]
            entidades = retEntidade[1]
            dicEntidades = {entidade.id: entidade for entidade in entidades}

            retColunas = self.colunas.selectColunasByCodigoAplicacao()
            colunas = retColunas[1]
            dicColunas = {col.id:col for col in colunas}

            gerados = 0
            lisWrite = [] # Lista com a ordem de gravação das entidades
            dicWrite = {} # Dicionario com as linhas de gravação por entidade
            dicRefer = {} # Dicionario com as entidades referenciadas

            for entidade in entidades:
                lookups = ''
                lisAppWrite = []
                lisAppWrite.append("\ndb.define_table('{}'\n".format(entidade.nomeFisico))
                retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidade.id)
                if  not retColunasEntidades[0]:
                    if  retColunasEntidades[1]:
                        return False, retColunasEntidades[2]
                    else:
                        return False, None
                gerados += 1
                colunasEntidade = retColunasEntidades[1]
                retPrimaryKeys = self.primaryKeys.selectPrimaryKeysByCodigoEntidade(entidade.id)
                if not retPrimaryKeys:
                    return [0, retPrimaryKeys[1]]
                primaryKeys = retPrimaryKeys
                dicFKs = self.foreignKeys.selectForeignKeysByCodigoEntidade(entidade.id)
                dicRefer[entidade.id]=list(set([dicFKs[k][0] for k in dicFKs if dicFKs[k][0] != entidade.id]))
                retColEntRef = self.ColEntRef.selectColunasEntidadesReferenciadasByCodigoEntidade(entidade.id)
                colEntRef = retColEntRef[1]
                lc = len(colunasEntidade)
                for n, col in enumerate(colunasEntidade):
                    foreignKey = ''
                    if  (col.colunas.id in dicFKs and
                         dicFKs[col.colunas.id][0] != entidade.id):
                        foreignKey = ', {}'.format(dicEntidades[dicFKs[col.colunas.id][0]].nomeFisico)

                    dttp = dicDataTypes[col.datatypes.descricao]
                    if  dttp == "'decimal'":
                        dttp = ", 'decimal({},{})'".format(col.colunas.tamanhoColuna
                                                          ,col.colunas.decimais)
                    elif not dttp:
                        dttp = ", length={}".format(col.colunas.tamanhoColuna)
                    else:
                        dttp = ', {}'.format(dttp)
                    if  modeloDB[self.modeloDb] == 'Soag':
                        fpar = ')\n' if  n + 1 == lc else ''
                    else:
                        fpar = ''
                    lisAppWrite.append("{:>24}{}'{}{}){}\n".format(", Field('", col.colunas.columnName
                                                                  , foreignKey, dttp, fpar))

                if  modeloDB[self.modeloDb] == 'legacy':
                    lisAppWrite.append('{:15}{}\n'.format('',', primarykey=[{}]'.format(
                                 ', '.join(["'"+dicColunas[c].columnName+"'" for c in primaryKeys.keys()]))))
                    lisAppWrite.append('{:15}{}\n'.format('', ', migrate=False)'))

                lisAppWrite.append("{0:50}= db['{0}']\n\n".format(entidade.nomeFisico))
                if  modeloDB[self.modeloDb] == 'Soag':
                    lisAppWrite.append('{:50}= False\n'.format('{}.id.writable'.format(entidade.nomeFisico)))
                for col in colunasEntidade:
                    entCol = '{}.{}'.format(entidade.nomeFisico, col.colunas.columnName)
                    origem = self.origemColuna(col)
    ###### Label
                    lisAppWrite.append("{:50}= '{}'\n".format('{}.label'.format(entCol)
                                                        ,col.colunas.label))
                    if (col.colunas.id in primaryKeys and primaryKeys[col.colunas.id] == 3):
                        lisAppWrite.append('{:50}= True\n'.format('{}.readonly'.format(entCol)))
                        lisAppWrite.append('if  widgets:\n')
                        lisAppWrite.append('    {:46}= widgets.text\n'.format('{}.widget'.format(entCol)))
                    elif origem:
                        lisAppWrite.append('{:50}= True\n'.format('{}.readonly'.format(entCol)))
                        lisAppWrite.append('if  widgets:\n')
                        lisAppWrite.append('    {:46}= widgets.text\n'.format('{}.widget'.format(entCol)))
                    else:
                        lisAppWrite.append('{:50}= True\n'.format('{}.writable'.format(entCol)))
                        isindb = False
                        requires = '{}.requires'.format(entCol)
                        if  (col.colunas.id in dicFKs and
                             dicFKs[col.colunas.id][0] != entidade.id):
                            isindb = True
                            entRef = dicEntidades[dicFKs[col.colunas.id][0]].nomeFisico
                            entRefId = dicEntidades[dicFKs[col.colunas.id][0]].id
                            colName = dicColunas[dicFKs[col.colunas.id][1]].columnName
                            colRef = colName
                            for cer in colEntRef:
                                if  (cer.colunasEntidadesReferenciadas.entidadeReferenciada ==
                                     dicFKs[col.colunas.id][0]):
                                    if cer.colunasEntidadesReferenciadas.consultaSaida:
                                       colRef = dicColunas[cer.colunasEntidadesReferenciadas.codigoColuna].columnName
                                    if cer.colunasEntidadesReferenciadas.listaSaida:
                                       lookups = self.montaLookups(lookups
                                                                  ,entidade.nomeFisico
                                                                  ,col.colunas.columnName
                                                                  ,entRef
                                                                  ,dicColunas[cer.colunasEntidadesReferenciadas.codigoColuna].columnName)
                                    break
                            lisAppWrite.append('{:50}= IS_IN_DB(db, {}.{}\n'.format(requires, entRef, colName))
                            lisAppWrite.append("{:>52},'%({})s', zero='-- Selecione --'\n".format('',colRef))
                            message = self.montaMensagem(entRefId, 'E', 'E', 'C')
                            lisAppWrite.append("{:>52},error_message=msgGet(db,'{}'))\n".format('',message))
                        else:
                            lisRegras =[]
                            al = '['
                            eq = '='
                            retRegras = self.regrasColunas.selectRegrasColunasByColumnId(col.colunas.id)
                            if  not retRegras[0] and retRegras[1]:
                                if  self.info:
                                    return False, traceback.format_exc(sys.exc_info)
                                else:
                                    return False, None
                            regras = retRegras[1]

                            if  col.colunasEntidades.ehNotNull:
                                message = self.montaMensagem(col.colunas.id, 'C', 'E', 'PR', nova=1)
                                lisRegras.append("{:50}{} {}IS_NOT_EMPTY(error_message=msgGet(db,'{}'))\n".format(
                                                                                       requires, eq, al, message))
                                requires=''
                                al = ','
                                eq = ' '

                            natureza = col.datatypes.descricao
                            if  natureza in 'DECIMAL NUMERIC' and col.colunas.decimais == 0:
                                natureza = 'INTEGER'

                            if  dicNatureza[natureza][0]:
                                message = self.montaMensagem(col.colunas.id, 'C', 'E', dicNatureza[natureza][1], nova=1)
                                lisRegras.append("{:50}{} {}{}(error_message=msgGet(db,'{}'))\n".format(
                                                                   requires, eq, al, dicNatureza[natureza][0], message))
                                requires=''
                                al = ','
                                eq = ' '

                            if  regras:
                                regras = regras[0]
                                regra = regras.regras.regra
                                message = self.montaMensagem(col.colunas.id, 'C', 'E', regra, nova=1)
                                lisRegras.append(tratarRegras(regra, regras, col, requires, eq, al, message))

                            lr = len(lisRegras)
                            for n, l in enumerate(lisRegras):
                                if  n + 1 == lr:
                                    l = l[:-1] + ']\n'
                                lisAppWrite.append(l)

                        if  dicWidgets[col.datatypes.descricao] and not isindb:
                            lisAppWrite.append('if  widgets:\n')
                            lisAppWrite.append('    {:46}= widgets.text\n'.format('{}.widget'.format(entCol)))

                if  lookups:
                    lisAppWrite.append(lookups[:-1] + '}\n')
                dicWrite[entidade.id]=lisAppWrite

            while len(dicRefer) > 0:
                lisKeys = sorted(dicRefer.keys()) # Lista com as keys do dicRefer para deleção dos vazios
                                                  # Cada key deletada do dicRefer entra na lisWrite
                for k in lisKeys:
                    if  not dicRefer[k]:
                        lisWrite.append(k)
                        del dicRefer[k]
                for ent in lisWrite:
                    for k in dicRefer.keys():
                        if  ent in dicRefer[k]:
                            dicRefer[k].remove(ent)

            for ent in lisWrite:
                dbApp.writelines(dicWrite[ent])

            dbApp.close()
            clp = self.atualizaCheckListPrototipo()
            if  not clp:
                return clp
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        return True, 'Entidades Geradas = ' + str(gerados)

    def origemColuna(self, col):
        origem = self.OrigemColunasAplicacao.selectOrigemColunasAplicacaoByCodigoColuna(col.colunas.id)
        if  origem[0] and origem[1]:
            return True
        else:
            return False

    def montaMensagem(self, codigoEntCol, origemMsg, tipoMsg, regra, nova=None):
        retMessage = self.mensagens.getMensagem(codigoEntCol, origemMsg, tipoMsg, regra, nova)
        if  retMessage[0]:
            return '{}{:04}'.format(self.applId, retMessage[1])
        else:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None

    def montaLookups(self, lookups, entidade, coluna, entRef, colRef):
        if  lookups:
            lkp = ''
            eqs = ' '
            ach = ','
        else:
            lkp = '{}.lookups'.format(entidade)
            eqs = '='
            ach = '{'
        lookups += "{:50}{} {}'{}': ['{}', ['{}'] ,False]\n".format(lkp, eqs, ach, coluna, entRef, colRef)
        return lookups

    def atualizaCheckListPrototipo(self):
        try:
            if self.databaseCreated:
               self.db(self.checkListPrototipo.codigoAplicacao == self.cAppl).update(model = True
                                                                                    ,database = True)
            else:
               self.db(self.checkListPrototipo.codigoAplicacao == self.cAppl).update(model = True)
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        self.db.commit()
        return True, None

    def tryEngine(self):
        config = self.database.getConfig()
        sgdbDB = config.sgdb.sgdb
        userDB = config.database.userDB
        passDB = config.database.passDB
        hostDB = config.database.hostDB
        portDB = config.database.portDB
        nameDB = config.database.nameDB

        if  sgdbDB == 'DB2':
            import ibm_db_sa
        try:
            engine = eval("{}.{}('{}://{}:{}@{}:{}/{}')".format( 'sqlalchemy'
                                                               , 'create_engine'
                                                               , sgdbDB
                                                               , userDB
                                                               , passDB
                                                               , hostDB
                                                               , portDB
                                                               , nameDB))
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        return True, engine

    def metaSchema(self, engine):
        try:
            schm = sqlalchemy.schema.MetaData(bind=engine)
            schm.reflect()
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        return True, schm

