# -*- coding:utf-8
'''
   Created on 02/09/2011
   @author: C&C - HardSoft
'''
import sys

class OrigemMensagens:

   def __init__(self, db):
       self.db          = db
       self.origens     = self.db.origemMensagens
       self.dicOrigem   = {}

   def getOrigens(self):
       try:
           for query in self.db(self.origens).select():
               self.codigoOrigem           = query.id
               self.origem                 = query.origem
               self.dicOrigem[self.origem] = self.codigoOrigem
       except:
           return [0, 'Ocorreu um erro no Select da Tabela OrigemMensagens.', sys.exc_info()[1]]
       return self.dicOrigem
