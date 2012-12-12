# -*- coding:utf-8
'''
   Created on 10/10/2011
   @author: C&C - HardSoft
'''
import sys

class MensagensPadrao:

   def __init__(self, db, cAppl=None):
       self.db              = db
       self.cAppl           = cAppl or 0
       self.mensagensPadrao = self.db.mensagensPadrao

   def criaMensagensPadrao(self):
       mensagensPadraoSoag = self.db.mensagensPadraoSoag
       gravados             = 0
       try:
           for query in self.db(mensagensPadraoSoag).select(orderby=mensagensPadraoSoag.id):
               try:
                   self.mensagensPadrao.insert(codigoAplicacao  = int(self.cAppl)       \
                                              ,codigoOrigemMsg  = query.codigoOrigemMsg \
                                              ,codigoTipoMsg    = query.codigoTipoMsg   \
                                              ,codigoRegra      = query.codigoRegra    \
                                              ,codigoMsgPrefixo = query.codigoMsgPrefixo\
                                              ,codigoMsgSufixo  = query.codigoMsgSufixo )
                   gravados = gravados +1
               except:
                   return [0,"Ocorreu um erro no Insert da Tabela mensagensPadrao.", sys.exc_info()[1]]
       except:
           return [0, 'Ocorreu um erro na Leitura da Tabela MensagensPadraoSoag.', sys.exc_info()[1]]
       self.db.commit()
       return [1,'Mensagens Padrao  >>>'              \
              + '\n' + ' Gravados = ' + str(gravados) \
              + '\n']

   def selectMensagensPadraoBycodigoAplicacao(self):
       dicMensagens  = {}
       try:
           for query in self.db(self.mensagensPadrao.codigoAplicacao == int(self.cAppl)).select():
               codigoMensagem         = query.id
               mensagem               = str(query.codigoAplicacao) \
                                      + str(query.codigoOrigemMsg) \
                                      + str(query.codigoTipoMsg)   \
                                      + str(query.codigoRegra)
               dicMensagens[mensagem] = codigoMensagem
       except:
           return [0, 'Ocorreu um erro no Select da Tabela MensagensPadrao.', sys.exc_info()[1]]
       return dicMensagens
