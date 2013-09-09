# -*- coding:cp1252
'''
   Created on 22/07/2013
   @author: C&C - HardSoft
'''

import sys, traceback, time
import sqlalchemy
from utilities import *
from Database import Database
from DicAbrev import DicAbrev

class Sqlalchemy(object):

    def __init__(self, db, cAppl=None, info=False):
        self.db = db
        self.cAppl = cAppl
        self.info = info
        self.database = Database(db, cAppl=self.cAppl)
        self.dicAbrev = DicAbrev(self.db)
        self._entitys = {}
        self._columns = {}
        self._entitysColumns = {}

    def load(self, database=False, picke=''):

        t0 = time.time()

        print ' '
        print 'Loading ...'

        flash = 'Loading ok'
        msgsErrors = ''
        if  database:
            labelErrors = 'Loading Database'
            retorno, returned = self.tryEngine()
            if  not retorno:
                return self.retorno(retorno, 'Error tryEngine', labelErrors, returned)
            engine = returned

            retorno, returned = self.metaSchema(engine)
            if  not retorno:
                return self.retorno(retorno, 'Error metaSchema', labelErrors, returned)
            schm = returned

            self.dicabrev = self.dicAbrev.getDicAbrev()

            retorno, returned = self.__setEntitys__(schm)
            if  not retorno:
                return self.retorno(retorno, 'Error setEntitys', labelErrors, returned)
            self._entitys = returned

            retorno, returned = self.__setColumns__(schm)
            if  not retorno:
                return self.retorno(retorno, 'Error setColumns', labelErrors, returned)
            self._columns = returned

            retorno, returned = self.__setEntitysColumns__(schm)
            if  not retorno:
                return self.retorno(retorno, 'Error setEntitysColumns', labelErrors, returned)
            self._entitysColumns = returned

        elif picke:
            retorno = True
            labelErrors = 'Loading Pickle'
            try:
                self._entitys        = picke['entitys']
                self._columns        = picke['columns']
                self._entitysColumns = picke['entitysColumns']
            except:
                return self.retorno(False, 'Error Loading Pickle', labelErrors, '')
        else:
            retorno = False
            flash = 'Erro nos Parametros do Load'
            labelErrors = 'Parametros Inválidos'
            msgsErrors  = "Informe 'database = True' ou 'picke = nome'!"

        print '        Tempo corrido:', time.time() - t0

        return self.retorno(retorno, flash, labelErrors, msgsErrors)

    def retorno(self, retorno, flash, labelErrors, msgsErrors):
        return {'retorno':retorno
               ,'flash':flash
               ,'labelErrors': labelErrors
               ,'msgsErrors': msgsErrors}


    def tryEngine(self):
        config = self.database.getConfig()
        if  not config:
            if  self.info:
                return False, config[1]
            else:
                return False, False
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
                return False, False
        return True, engine

    def metaSchema(self, engine):
        try:
            schm = sqlalchemy.schema.MetaData(bind=engine)
            schm.reflect()
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, False
        return True, schm

    def __setEntitys__(self, schm):
        _entitys = {}
        dicPre ={'T':u'TB', 'TB':u'Tabela', 'WK':''}
        dicabrev = self.dicabrev

        try:
            # lisTables = [tb for tb in schm.tables.keys() if tb[0] == 't']
            lisTables = [tb for tb in schm.tables.keys()]
            lisTables.sort()

            for tbl in lisTables:
                table = schm.tables[tbl]

                tblUpp = table.description.upper()
                attr=dicPre[tblUpp[:1]] if tblUpp[:1] in dicPre else 'WK'
                attt=tblUpp[1:].replace('_',' ')
                for word in words(attt)[1]:
                    if  word.upper() in dicabrev:
                        attr=attr+dicabrev[word.upper()][0].capitalize()
                    else:
                        attr=attr+word.capitalize()

                nAttr=dicPre[attr[0:2].upper()] + ' '
                strt = 2
                for chr in xrange(3,len(attr)):
                    if  attr[chr].isupper():
                        nAttr = nAttr + attr[strt:chr] + ' '
                        strt  = chr
                nAttr = nAttr + attr[strt:chr+1]

                # atributos
                attrs = {'Do_Not_Generate':False
                        ,'User_Formatted_Physical_Name':tblUpp
                        ,'User_Formatted_Name':' '.join(nAttr.split()[1:])
                        ,'Definition':nAttr
                        ,'Comment':nAttr}
                _entitys[tblUpp]=attrs

        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, False
        return True, _entitys



    def __setColumns__(self, schm):

        _columns = {}
        dicPre ={'C':u'CD', 'D':u'DT', 'R':u'DS', 'E':u'EN', 'H':u'HR', 'M':u'MD',
                 'B':u'MM', 'I':u'NM', 'N':u'NU', 'P':u'PC', 'T':u'PR', 'Q':u'QT',
                 'U':u'UN', 'V':u'VR', 'W':u'WK', 'CD':u'Código ', 'DS':u'Descrição ',
                 'DT':u'Data ', 'EN':u'Endereço ', 'HR':u'Hora ', 'ID':u'Identificador',
                 'NM':u'Nome ', 'NU':u'Número ', 'MD':u'Medida ', 'MM':u'Multimídia ',
                 'PC':u'Percentual ', 'PR':u'Prazo ', 'QT':u'Quantidade ', 'VR':u'Valor ',
                 'UN':u'Unidade ', 'WK':''}

        dicabrev = self.dicabrev

        try:
            lisTables = [tb for tb in schm.tables.keys()]
            lisTables.sort()

            for tbl in lisTables:
                table = schm.tables[tbl]
                for kc in table.columns.keys():
                    col = table.columns.get(kc)
                    colUpp = col.description.upper()
                    if  colUpp not in _columns and col.description != 'id':
                        attr=dicPre[colUpp[:1]] if colUpp[:1] in dicPre else 'WK'
                        attt=colUpp[1:].replace('_',' ')
                        for word in words(attt)[1]:
                            if  word.upper() in dicabrev:
                                attr=attr+dicabrev[word.upper()][0].capitalize()
                            else:
                                attr=attr+word.capitalize()

                        nAttr=dicPre[attr[0:2].upper()]
                        strt = 2
                        for chr in xrange(3,len(attr)):
                            if  attr[chr].isupper():
                                nAttr = nAttr + attr[strt:chr] + ' '
                                strt  = chr
                        nAttr = nAttr + attr[strt:chr+1]

                        # atributos

                        datatype = str(col.type) if '(' in str(col.type) else str(col.type).split()[0]

                        _columns[colUpp]= {'Physical_Name':colUpp
                                          ,'Name':attr
                                          ,'Definition':nAttr
                                          ,'Comment':''
                                          ,'Physical_Data_Type':datatype}
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, False
        return True, _columns


    def __setEntitysColumns__(self, schm):

        _entitysColumns = {}

        try:
            # lisTables = [tb for tb in schm.tables.keys() if tb[0] == 't']
            lisTables = [tb for tb in schm.tables.keys()]
            lisTables.sort()

            for tbl in lisTables:
                table = schm.tables[tbl]
                tblUpp = table.description.upper()
                _entitysColumns[tblUpp]=[]
                for kc in table.columns.keys():
                    col = table.columns.get(kc)
                    colUpp = col.description.upper()
                    fk = []
                    if  col.foreign_keys:
                        fkt, fkc = str(list(col.foreign_keys)[0]).split('(')[1][2:-2].split('.')
                        fkcol = col.description if fkc == 'id' else fkc
                        fk.append([fkcol.upper(), fkt.upper()])

                    datatype = str(col.type) if '(' in str(col.type) else str(col.type).split()[0]
                    _entitysColumns[tblUpp].append({'nomeFisico':col.description.upper()
                                                   ,'null':col.nullable
                                                   ,'pk':col.primary_key
                                                   ,'fk':fk
                                                   ,'dataType':datatype})
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, False
        return True, _entitysColumns

    def getEntidades(self, entidade=''):
        if  entidade:
            try:
                return self._entitys[entidade]
            except:
                return {}
        else:
            ret = []
            for key in self._entitys:
                ret.append(self._entitys[key])
            return ret

    def getColunas(self, coluna=''):
        if  coluna:
            try:
                return self._columns[coluna]
            except:
                return {}
        ret = []
        for key in self._columns:
            ret.append(self._columns[key])
        return ret

    def getEntidadeColunas(self, entidade):
        try:
            return self._entitysColumns[entidade]
        except:
            return []

    def getEntitys(self):
        try:
            return self._entitys
        except:
            return []

    def getColumns(self):
        try:
            return self._columns
        except:
            return []

    def getEntitysColumns(self):
        try:
            return self._entitysColumns
        except:
            return []

# vim: ft=python
