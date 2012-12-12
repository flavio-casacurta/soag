# -*- coding:utf-8
'''
   Created on 12/09/2011
   @author: C&C - HardSoft
'''
import sys

class ColunasEntidadesReferenciadas:


   def __init__(self, db):
       self.db                            = db
       self.colunasEntidadesReferenciadas = self.db.colunasEntidadesReferenciadas
       self.colunasEntidades              = self.db.colunasEntidades
       self.datatypes                     = self.db.datatypes
       self.colunas                       = self.db.colunas

   def selectColunasEntidadesReferenciadasByCodigoEntidade(self, codigoEntidade):
       try:
           query = self.db((self.colunasEntidadesReferenciadas.codigoEntidade == codigoEntidade)
                         & (self.colunasEntidades.codigoEntidade == self.colunasEntidadesReferenciadas.entidadeReferenciada)
                         & (self.colunasEntidades.codigoColuna   == self.colunasEntidadesReferenciadas.codigoColuna)
                         & (self.colunas.id   == self.colunasEntidadesReferenciadas.codigoColuna)
                         & (self.datatypes.id == self.colunas.codigoDatatype))\
                           .select(orderby=self.colunasEntidadesReferenciadas.id)

       except:
           return [0, 'CE - Ocorreu um erro no Select da Tabela ColunasEntidadesReferenciadas.', sys.exc_info()[1]]
       return [1, query]
