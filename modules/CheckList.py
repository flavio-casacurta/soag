# -*- coding:utf-8
'''
   Created on 12/09/2011
   @author: C&C - HardSoft
'''
import sys

class CheckList:

   def __init__(self, db, cAppl=None):
       self.db        = db
       self.cAppl     = cAppl or 0
       self.checkList = self.db.checkList

   def updateCheckListColunasEntidades(self):
       try:
           self.db(self.checkList.codigoAplicacao == self.cAppl)    \
                       .update(colunasEntidades   = 1)
       except:
           return [0, 'CE - Ocorreu um erro no Update da Tabela checkList.', sys.exc_info()[1]]
       self.db.commit()
       return [1, 1]

   def updateCheckListMensagensEntidades(self):
       try:
           self.db(self.checkList.codigoAplicacao  == self.cAppl)   \
                       .update(mensagensEntidades   = 1)
       except:
           return [0, 'MSG - Ocorreu um erro no Update da Tabela checkList.', sys.exc_info()[1]]
       self.db.commit()
       return [1, 1]

   def updateCheckListProgramas(self):
       try:
           self.db(self.checkList.codigoAplicacao  == self.cAppl)   \
                       .update(programas   = 1)
       except:
           return [0, 'PGM - Ocorreu um erro no Update da Tabela checkList.', sys.exc_info()[1]]
       self.db.commit()
       return [1, 1]
