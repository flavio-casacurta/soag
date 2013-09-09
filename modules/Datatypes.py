# -*- coding:utf-8
'''
   Created on 21/10/2011
   @author: C&C - HardSoft
'''
import sys

class Datatypes:

   def __init__(self, db):
       self.db            = db
       self.datatypes     = self.db.datatypes

   def getDatatypes(self):
       dicDatatypes  = {}
       try:
           for query in self.db(self.datatypes).select():
               dicDatatypes[query.descricao] = query.id
       except:
           return [0, 'Ocorreu um erro no Select da Tabela Datatypes.', sys.exc_info()[1]]
       return dicDatatypes

   def getDatatypesNumerics(self):
       lisDatatypes  = []
       try:
           for query in self.db(self.datatypes.picture_cobol==9).select():
               lisDatatypes.append(query.descricao)
       except:
           return [0, 'Ocorreu um erro no Select da Tabela Datatypes.', sys.exc_info()[1]]
       return lisDatatypes

# vim: ft=python
