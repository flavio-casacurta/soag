# -*- coding:utf-8
'''
   Created on 02/09/2011
   @author: C&C - HardSoft
'''
import sys

class Regras:

   def __init__(self, db):
       self.db         = db
       self.regras     = self.db.regras
       self.dicRegras  = {}

   def getRegras(self, tipoPrograma):
       try:
           for query in self.db(self.regras.tipoPrograma == int(tipoPrograma)).select():
               self.dicRegras[query.regra] = [query.id, query.argumento1, query.argumento2]
       except:
           return [0, 'Ocorreu um erro no Select da Tabela Regras.', sys.exc_info()[1]]
       return self.dicRegras
