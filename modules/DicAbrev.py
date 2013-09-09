# -*- coding:utf-8
'''
   Created on 20/04/2012
   @author: C&C - HardSoft
'''
import sys

class DicAbrev(object):

   def __init__(self, db):
       self.db         = db
       self.DicAbrev   = self.db.dicAbrev
       self.dicAbrev   = {}

   def getDicAbrev(self):
       try:
           for query in self.db(self.DicAbrev).select():
               self.dicAbrev[query.mnemonico] = [query.termo, query.descricao]
       except:
           return [0, 'Ocorreu um erro no Select da Tabela DicAbrev.', sys.exc_info()[1]]
       return self.dicAbrev

# vim: ft=python
