# -*- coding:utf-8
'''
   Created on 13/09/2011
   @author: C&C - HardSoft
'''
import sys, string
from Aplicacao   import Aplicacao
from Regras      import Regras
from Entidades   import Entidades
from PrimaryKeys import PrimaryKeys
from CheckList   import CheckList

class Programas:

   def __init__(self, db, cAppl=None):
       self.db          = db
       self.cAppl       = cAppl or 0
       self.applId      = Aplicacao(self.db, self.cAppl).getApplId()
       self.programas   = self.db.programas
       self.char        = string.digits + string.ascii_uppercase
       self.gravados    = 0
       self.regra       = Regras(self.db).getRegras(1)
       self.entidades   = Entidades(self.db, cAppl=self.cAppl)
       self.primaryKeys = PrimaryKeys(self.db)
       self.bookSaida   = {'I':0, 'A':'0', 'E':0, 'C':1, 'L':1}
       returnCode       = self.maxPrograma()
       if returnCode[0] and returnCode[1]:
           mp           = returnCode[1]
           self.c1      = self.char.index(mp[0])
           self.c2      = self.char.index(mp[1])
       else:
           self.c1      = 0
           self.c2      = -1
       self.checkList   = CheckList(self.db, cAppl=self.cAppl)

   def nomearProgramas(self):
       returnCode = self.entidades.selectEntidadesProgramasBycodigoAplicacao()
       if not returnCode[0]:
           return [0, "Não existem Entidades para esta Aplicação", returnCode[1]]
       for codigoEntidade, listaProgramas in returnCode[1]:
           if listaProgramas[0]:
               bookSaidaI = 0
               if not self.primaryKeys.primaryKeyInformada(codigoEntidade):
                   bookSaidaI = 1
               self.insertProgramas(codigoEntidade
                                   , 1
                                   , self.regra['I'][0]
                                   , self.novoNomePrograma()
                                   , bookSaidaI
                                   )
           if listaProgramas[1]:
               self.insertProgramas(codigoEntidade
                                   , 1
                                   , self.regra['A'][0]
                                   , self.novoNomePrograma()
                                   , self.bookSaida['A']
                                   )
           if listaProgramas[2]:
               self.insertProgramas(codigoEntidade
                                   , 1
                                   , self.regra['E'][0]
                                   , self.novoNomePrograma()
                                   , self.bookSaida['E']
                                   )
           if listaProgramas[3]:
               self.insertProgramas(codigoEntidade
                                   , 1
                                   , self.regra['C'][0]
                                   , self.novoNomePrograma()
                                   , self.bookSaida['C']
                                   )
           if listaProgramas[4]:
               self.insertProgramas(codigoEntidade
                                   , 1
                                   , self.regra['L'][0]
                                   , self.novoNomePrograma()
                                   , self.bookSaida['L']
                                   )

       ckListPGM =  self.checkList.updateCheckListProgramas()
       if not ckListPGM[0]:
           return ckListPGM

       self.db.commit()
       return [1,'Programas Nomeados >>>'                  \
              + '\n' + ' Gravados = ' + str(self.gravados) \
              + '\n']

   def nomearPrograma(self, entidadeId, codigoTipo, regra):
       returnCode     = self.insertProgramas( entidadeId
                                            , codigoTipo
                                            , self.regra[regra][0]
                                            , self.novoNomePrograma()
                                            , self.bookSaida[regra])
       if returnCode[0]:
           self.db.commit()
           return [1, str(self.gravados) + " Programa Nomeado"]
       else:
           return [0, returnCode[1], returnCode[2]]

   def insertProgramas(self, codigoEntidade, codigoTipo, codigoRegra, nomePrograma, bookSaida):
       try:
           self.programas.insert(codigoAplicacao = int(self.cAppl)
                                ,codigoEntidade  = codigoEntidade
                                ,codigoTipo      = codigoTipo
                                ,codigoRegra     = codigoRegra
                                ,nomePrograma    = nomePrograma
                                ,bookSaida       = bookSaida)
           self.gravados += 1
           return [1]
       except:
           return [0,"Ocorreu um erro no Insert da Tabela Programas.", sys.exc_info()[1]]

   def maxPrograma(self):
       try:
           query=self.db(self.programas.codigoAplicacao == int(self.cAppl)).select(self.programas.nomePrograma.max())
       except:
           return [0,"Ocorreu um erro no select da Tabela Programas.", sys.exc_info()[1]]
       if query:
           maxPrograma = query[0]._extra['MAX(programas.nomePrograma)']
       else:
           return [0, 0]
       return [1, maxPrograma]

   def novoNomePrograma(self):
       self.c2 += 1
       if self.c2 > 35:
           self.c1 += 1
           self.c2  = 0
       return self.char[self.c1] + self.char[self.c2]

   def selectProgramasByEntidadeRegra(self, codigoEntidade, regra):
       try:
           query=self.db((self.programas.codigoEntidade == int(codigoEntidade))
                       & (self.programas.codigoRegra    == self.regra[regra][0])).select()
       except:
           return [0,'Ocorreu um erro no Select da Tabela Programas.', sys.exc_info()[1]]
       if not query:
           return [0, 0]
       return [1, query]
