# -*- coding:utf-8
'''
   Created on 27/04/2013
   @author: C&C - HardSoft
'''
from utilities import *

dicOC = {'EQ':('==', 'arg'    , 'arg')
        ,'NE':('!=', 'None'   , 'None')
        ,'LT':('<' , 'None'   , 'arg+-0.1')
        ,'LE':('<=', 'None'   , 'arg')
        ,'GT':('>' , 'arg+0.1', 'None')
        ,'GE':('>=', 'arg'    , 'None')}

dicNat={'CHAR':('', '')
       ,'DECIMAL':('float(', ')')
       ,'NUMERIC':('float(', ')')
       ,'INTEGER':('int(', ')')
       ,'VARCHAR':('', '')}

def tratarRegras(regra, regras, col, requires, eq, al, message):

    ret = eval('regra{}(regra, regras, col, requires, eq, al, message)'.format(regra))
    return ret

#  Operadores de Comparacao
def regraOC(regra, regras, col, requires, eq, al, message):
    cmprdr = regras.regrasColunas.argumento1
    natureza = col.datatypes.descricao
    if  natureza == 'DECIMAL':
        if  col.colunas.decimais == 0:
            natureza = 'INTEGER'
            iap = dicNat[natureza][0]
            ifp = dicNat[natureza][1]
            return "{:50}{} {}IS_EXPR('{}value{} {} {}',error_message=msgGet(db,'{}'))\n".format(requires
                                                                                                , eq
                                                                                                , al
                                                                                                , iap
                                                                                                , ifp
                                                                                                , dicOC[regra][0]
                                                                                                , cmprdr
                                                                                                , message)
        else:
            arg=cmprdr
            arg1 = eval(dicOC[regra][1])
            arg2 = eval(dicOC[regra][2])
            return "{:50}{} {}IS_DECIMAL_IN_RANGE({},{},error_message=msgGet(db,'{}'),dot=',')\n".format(requires
                                                                                                        , eq
                                                                                                        , al
                                                                                                        , arg1
                                                                                                        , arg2
                                                                                                        , message)

regraEQ = regraOC    # Igual
regraNE = regraOC    # Diferente
regraLT = regraOC    # Menor Que
regraLE = regraOC    # Menor ou Igual
regraGT = regraOC    # Maior Que
regraGE = regraOC    # Maior ou Igual

# Lista de Valores
def regraVL(regra, regras, col, requires, eq, al, message):
    values = ', '.join(["'" + w + "'" for w in words(regras.regrasColunas.argumento1)[1]])
    return "{:50}{} {}IS_IN_SET([{}],error_message=msgGet(db,'{}'))\n".format(requires
                                                                             , eq
                                                                             , al
                                                                             , values
                                                                             , message)

# Range
def regraRG(regra, regras, col, requires, eq, al, message):
    natureza = col.datatypes.descricao
    if  natureza == 'DECIMAL':
        if  col.colunas.decimais == 0:
            natureza = 'INTEGER'
    ret = ''
    if  natureza in dicNat.keys():
        ret = eval('range{}(regra, regras, col, requires, eq, al, message)'.format(natureza))
    return ret

# Range CHAR
def rangeCHAR(regra, regras, col, requires, eq, al, message):
    arg1 = regras.regrasColunas.argumento1
    arg2 = regras.regrasColunas.argumento2
    sets = map(chr, range(ord(arg1), ord(arg2) + 1))
    return '{:50}{} {}IS_EXPR("value in {}",error_message=msgGet(db,"{}"))\n'.format(requires
                                                                                    , eq
                                                                                    , al
                                                                                    , sets
                                                                                    , message)
rangeVARCHAR = rangeCHAR

# Range INTEGER
def rangeINTEGER(regra, regras, col, requires, eq, al, message):
    arg1 = regras.regrasColunas.argumento1
    arg2 = regras.regrasColunas.argumento2
    return "{:50}{} {}IS_INT_IN_RANGE({},{},error_message=msgGet(db,'{}'))\n".format(requires
                                                                                    , eq
                                                                                    , al
                                                                                    , int(arg1)
                                                                                    , int(arg2) + 1
                                                                                    , message)

# Range DECIMAL
def rangeDECIMAL(regra, regras, col, requires, eq, al, message):
    arg1 = float(regras.regrasColunas.argumento1.replace(',','.'))
    arg2 = float(regras.regrasColunas.argumento2.replace(',','.'))
    return "{:50}{} {}IS_DECIMAL_IN_RANGE({},{},error_message=msgGet(db,'{}'),dot=',')\n".format(requires
                                                                                                , eq
                                                                                                , al
                                                                                                , arg1
                                                                                                , arg2
                                                                                                , message)

# Range DATE
def rangeDATE(regra, regras, col, requires, eq, al, message):
    return ''

# Range TIME
def rangeTIME(regra, regras, col, requires, eq, al, message):
    return ''

# Range TIMESTAMP
def rangeTIMESTAMP(regra, regras, col, requires, eq, al, message):
    return ''

# Date
def regraDT(regra, regras, col, requires, eq, al, message):
    return ''

def regraTM(regra, regras, col, requires, eq, al, message):
    return ''

def regraTS(regra, regras, col, requires, eq, al, message):
    return ''

