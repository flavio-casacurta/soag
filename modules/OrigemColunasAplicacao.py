# -*- coding:utf-8
'''
   Created on 14/11/2011
   @author: C&C - HardSoft
'''
import sys

class OrigemColunasAplicacao:

   def __init__(self, db):
       self.db                     = db
       self.origemColunasApoio     = self.db.origemColunasApoio
       self.origemColunasAplicacao = self.db.origemColunasAplicacao

   def selectOrigemColunasAplicacaoByCodigoColuna(self, codigoColuna):
       try:
           query = self.db((self.origemColunasAplicacao.codigoColuna == codigoColuna)
                         & (self.origemColunasApoio.id               == self.origemColunasAplicacao.origem)) \
                           .select()
       except:
           return [0, 'Ocorreu um erro no Select da Tabela Regras.', sys.exc_info()[1]]
       return [1, query]
