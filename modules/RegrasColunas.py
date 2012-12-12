# -*- coding:utf-8
'''
   Created on 02/09/2011
   @author: C&C - HardSoft
'''
import sys

class RegrasColunas:

   def __init__(self, db, cAppl=None):
       self.db            = db
       self.cAppl         = cAppl or 0
       self.regras        = self.db.regras
       self.regrasColunas = self.db.regrasColunas

   def insertRegrasColunas(self, codigoColuna, codigoRegra, argumento1=None, argumento2=None):
       try:
           self.regrasColunas.insert(codigoAplicacao = int(self.cAppl)
                                    ,codigoColuna    = codigoColuna
                                    ,codigoRegra     = codigoRegra
                                    ,argumento1      = argumento1
                                    ,argumento2      = argumento2)
           self.db.commit()
           return [1, 1]
       except:
           return [0,"CE - Ocorreu um erro no Insert da Tabela regrasColunas.", sys.exc_info()[1]]

   def selectRegrasColunasByColumnId(self, codigoColuna):
       try:
           query = self.db((self.regrasColunas.codigoColuna == codigoColuna)
                         & (self.regras.id                  == self.regrasColunas.codigoRegra)) \
                          .select(orderby=self.regrasColunas.codigoRegra)
       except:
           return [0, 'E1 - Ocorreu um erro no Select da Tabela regrasColunas.', sys.exc_info()[1]]

       return [1, query]

   def selectRegrasColunasByColumnIdCodigoRegra(self, codigoColuna, codigoRegra):
       try:
           query = self.db((self.regrasColunas.id          == codigoColuna) \
                         & (self.regrasColunas.codigoRegra == codigoRegra)).select()
       except:
           return [0, 'E2 - Ocorreu um erro no Select da Tabela regrasColunas.', sys.exc_info()[1]]

       return [1, query]
