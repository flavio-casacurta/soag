# -*- coding:utf-8
'''
   Created on 25/09/2011
   @author: C&C - HardSoft
'''

class Empresa:

   def __init__(self, db, empresaId=None):

       self.db        = db
       self.empresaId = empresaId or 0
       self.empresa   = self.db.empresa

       try:
           self.query               = self.db(self.empresa.id==self.empresaId).select()
           self.nome                = self.query[0].nome
           self.descricao           = self.query[0].descricao
           self.ativo               = self.query[0].ativo
       except:
           self.nome                = ''
           self.descricao           = ''
           self.ativo               = 0


   def getNome(self):
       return self.nome

   def getDescricao(self):
       return self.descricao

   def getAtivo(self):
       return self.ativo
