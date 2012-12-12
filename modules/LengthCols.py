# -*- coding:utf-8
'''
   Created on 24/08/2012
   @author: C&C - HardSoft
'''
import Datatypes

class LengthCols(object):

    def __init__(self, db):
        self.db         = db
        self.datatype   = Datatypes.Datatypes(self.db).getDatatypes()
        self.dicLength  = {'REAL':4
                          ,'DOUBLE':16
                          ,'DATE':10
                          ,'TIME':8
                          ,'INT':9
                          ,'INTEGER':9
                          ,'SMALLINT':4
                          ,'TIMESTAMP':26}

    def db2DatatypeLength(self, datatype):
        lenCol = 0
        lenDec = 0
        if  datatype.find('(') == -1:
            lenCol = self.dicLength[datatype]
        else:
            if  ',' in datatype:
                lenCol = int(datatype[datatype.index('(')+1:datatype.index(',')])
                lenDec = int(datatype[datatype.index(',')+1:datatype.index(')')])
            else:
                lenCol = int(datatype[datatype.index('(')+1:datatype.index(')')])
            datatype = datatype[:datatype.index('(')]
        return [self.datatype[datatype], lenCol, lenDec]
