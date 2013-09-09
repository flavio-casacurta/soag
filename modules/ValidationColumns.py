# -*- coding:utf-8
'''
   Created on 27/04/2013
   @author: C&C - HardSoft
'''
from utilities import *

dicInv = {'EQ':'!='
         ,'NE':'=='
         ,'LT':'>='
         ,'LE':'>'
         ,'GT':'<='
         ,'GE':'<'}

def tratarRegras(regra, regras, col, sp, message):
    cd = eval('regra{}(regra, regras, col, sp)'.format(regra))
    cd += "{:{}}session.flash = msgGet(db,'{}')\n".format('', sp + 4, message)
    return cd

#  Preenchimento
def regraPR(regra, regras, col, sp):
    return '{:{}}if  not request.vars.{} and not session.flash:\n'.format('', sp, col.colunas.columnName)

#  Operadores de Comparacao
def regraOC(regra, regras, col, sp):
    cmprdr = regraCol.regrasColunas.argumento1
    return '{:{}}if  request.vars.{} {} {} and not session.flash:\n'.format('', sp, col.colunas.columnName, dicInv[regra], cmprdr)

regraEQ = regraOC    # Igual
regraNE = regraOC    # Diferente
regraLT = regraOC    # Menor Que
regraLE = regraOC    # Menor ou Igual
regraGT = regraOC    # Maior Que
regraGE = regraOC    # Maior ou Igual

def regraVL(regra, regras, col, sp):
    values = ', '.join(["'" + w + "'" for w in words(regras.regrasColunas.argumento1)[1]])
    return '{:{}}if  request.vars.{} not in ({}) and not session.flash:\n'.format('', sp, col.colunas.columnName, values)

def regraRG(regra, regras, col, sp):
    arg1 = regras.regrasColunas.argumento1
    arg2 = regras.regrasColunas.argumento2
    values = map(chr, range(ord(arg1), ord(arg2) + 1))
    return '{:{}}if  request.vars.{} not in {} and not session.flash:\n'.format('', sp, col.colunas.columnName, values)

# Date
def regraDT(regra, regras, col, sp):
    cd  = '{:{}}dt = request.vars.{}\n'.format('', sp, col.colunas.columnName)
    cd += "{:{}}s  = '/' if '/' in request.vars.{} else '-'\n".format('', sp, col.colunas.columnName)
    cd += '{:{}}dts = dt.split(s)\n'.format('', sp)
    cd += '{:{}}try:\n'.format('', sp)
    cd += '{:{}}d = datetime.datetime(int(dts[2]), int(dts[1]), int(dts[0]))\n'.format('', sp + 4)
    cd += '{:{}}except ValueError:\n'.format('', sp)
    return cd
