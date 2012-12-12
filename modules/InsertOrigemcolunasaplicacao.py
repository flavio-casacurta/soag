# -*- coding:utf-8
'''
   Created on 12/09/2011
   @author: C&C - HardSoft
'''

import sys

class InsertOrigemcolunasaplicacao:

   def __init__(self, db):
       self.db                     = db
       self.origemColunasAplicacao = self.db.origemColunasAplicacao

   def insertOrigemColunasAplicacao(self):

       gravados = 0
       t = ((1,105,1,9)
           ,(1,142,2,5)
           ,(1,143,1,5)
           ,(1,144,1,5)
           ,(1,145,2,5)
           ,(1,146,1,5)
           ,(1,160,2,8)
           ,(1,161,1,8)
           ,(1,162,1,8)
           ,(1,163,1,8)
           ,(1,164,1,8)
           ,(1,165,1,8)
           ,(1,166,1,8)
           ,(1,167,2,8)
           ,(1,168,1,8)
           ,(1,169,1,8)
           ,(1,170,1,8)
           ,(1,171,1,8))

       for t1 in t:
           try:
               self.origemColunasAplicacao.insert(codigoAplicacao = t1[0]
                                                 ,codigoColuna    = t1[1]
                                                 ,codigoRegra     = t1[2]
                                                 ,origem          = t1[3])
               gravados += 1
           except:
               return [0,"CE - Ocorreu um erro no Insert da Tabela OrigemColunasAplicacao.", sys.exc_info()[1]]
       self.db.commit()

       return [1,('Origem das Colunas >>>'
              + '\n' + ' Gravados = ' + str(gravados)
              + '\n')]
