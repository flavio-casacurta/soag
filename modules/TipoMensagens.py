# -*- coding:utf-8
'''
   Created on 02/09/2011
   @author: C&C - HardSoft
'''
import sys

class TipoMensagens:

   def __init__(self, db):
       self.db          = db
       self.tipos       = self.db.tipoMensagens
       self.dicTipos    = {}

   def getTipos(self):
       try:
           for query in self.db(self.tipos).select():
               self.codigoTipo          = query.id
               self.tipo                = query.tipo
               self.dicTipos[self.tipo] = self.codigoTipo
       except:
           return [0, 'Ocorreu um erro no Select da Tabela TipoMensagens.', sys.exc_info()[1]]
       return self.dicTipos
