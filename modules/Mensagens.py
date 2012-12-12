# -*- coding:utf-8
'''
   Created on 13/09/2011
   @author: C&C - HardSoft
'''
import sys
from OrigemMensagens    import OrigemMensagens
from TipoMensagens      import TipoMensagens
from Regras             import Regras
from Entidades          import Entidades
from PrimaryKeys        import PrimaryKeys
from MensagensPadrao    import MensagensPadrao
from CheckList          import CheckList

class Mensagens:

   def __init__(self, db, cAppl=None):
       self.db              = db
       self.cAppl           = int(cAppl) or 0
       self.mensagens       = self.db.mensagensEntCol
       self.gravados        = 0
       self.origem          = OrigemMensagens(self.db).getOrigens()
       self.tipo            = TipoMensagens(self.db).getTipos()
       self.regra           = Regras(self.db).getRegras(1)
       self.primaryKeys     = PrimaryKeys(self.db)
       self.codigoMsgPadrao = MensagensPadrao(self.db, cAppl=self.cAppl).selectMensagensPadraoBycodigoAplicacao()
       self.checkList       = CheckList(self.db, cAppl=self.cAppl)

   def criaMensagensEntidades(self):
       entidades  = Entidades(self.db, cAppl=self.cAppl)
       returnCode = entidades.selectEntidadesProgramasBycodigoAplicacao()
       if not returnCode[0]:
           return [0, "Não existem Entidades para esta Aplicação"]
       for codigoEntidade, listaProgramas in returnCode[1]:
#          servico inclusao
           if listaProgramas[0]:
               if self.primaryKeys.primaryKeyInformada(codigoEntidade):
                   self.insertMensagensEntidades(codigoEntidade, 'E', 'E', 'I')

               self.insertMensagensEntidades(codigoEntidade, 'E', 'S', 'I')
#          servico alteracao
           if listaProgramas[1]:
               self.insertMensagensEntidades(codigoEntidade, 'E', 'S', 'A')
#          servico exclusao
           if listaProgramas[2]:
               self.insertMensagensEntidades(codigoEntidade, 'E', 'S', 'E')
#          servico consulta
           if listaProgramas[3]:
               self.insertMensagensEntidades(codigoEntidade, 'E', 'E', 'C')
               self.insertMensagensEntidades(codigoEntidade, 'E', 'S', 'C')
#          servico lista
           if listaProgramas[4]:
               self.insertMensagensEntidades(codigoEntidade, 'E', 'E', 'L')
               self.insertMensagensEntidades(codigoEntidade, 'E', 'S', 'L')

       ckListMSG = self.checkList.updateCheckListMensagensEntidades()
       if not ckListMSG[0]:
           return ckListMSG

       self.db.commit()
       return [1,'Mensagens das Entidades >>>'          \
              + '\n' + ' Gravados = ' + str(self.gravados) \
              + '\n']

   def insertMensagensEntidades(self, codigoEntCol, origemMsg, tipoMsg, regra):

       codigos = self.getCodigos(origemMsg, tipoMsg, regra)

       try:
           self.mensagens.insert(codigoAplicacao = self.cAppl  \
                                ,codigoEntCol    = codigoEntCol\
                                ,codigoOrigemMsg = codigos[0]  \
                                ,codigoMsgPadrao = codigos[1])
           self.gravados = self.gravados +1
           return [1]
       except:
           return [0,"Ocorreu um erro no Insert da Tabela Programas.", sys.exc_info()[1]]

   def getMensagem(self, codigoEntCol, origemMsg, tipoMsg, regra, nova=None):
       nova = nova or 0

       codigos = self.getCodigos(origemMsg, tipoMsg, regra)

       try:
           query=self.db((self.mensagens.codigoAplicacao == self.cAppl)
                       & (self.mensagens.codigoEntCol    == codigoEntCol)
                       & (self.mensagens.codigoOrigemMsg == codigos[0])
                       & (self.mensagens.codigoMsgPadrao == codigos[1])).select()
       except:
           return [0,'Ocorreu um erro no Select da Tabela Mensagens.', sys.exc_info()[1]]
       if query:
           codigoMensagem = query[0].id
       else:
           if nova:
               msgNova = self.insertMensagensEntidades(codigoEntCol, origemMsg, tipoMsg, regra)
               if msgNova[0]:
                   self.db.commit()
                   return self.getMensagem(codigoEntCol, origemMsg, tipoMsg, regra)
           else:
               return [0, 0, 0]
       return [1, codigoMensagem]

   def getCodigos(self, origemMsg, tipoMsg, regra):
       codigoOrigemMsg = self.origem[origemMsg]
       codigoTipoMsg   = self.tipo[tipoMsg]
       codigoRegra     = self.regra[regra][0]
       codigoMsgPadrao = self.codigoMsgPadrao[str(self.cAppl)    + str(codigoOrigemMsg)\
                                            + str(codigoTipoMsg) + str(codigoRegra)]
       return (codigoOrigemMsg, int(codigoMsgPadrao))
