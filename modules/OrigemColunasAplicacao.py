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
        self.regras                 = self.db.regras

    def selectOrigemColunasAplicacaoByCodigoColuna(self, codigoColuna):
        try:
            query = self.db((self.origemColunasAplicacao.codigoColuna == codigoColuna)
                          & (self.origemColunasApoio.id == self.origemColunasAplicacao.origem)
                          & (self.regras.id == self.origemColunasAplicacao.codigoRegra)).select()
        except:
            return [0, 'Ocorreu um erro no Select da Tabela origemColunasAplicacao.', sys.exc_info()[1]]
        return [1, query]

    def insertOrigemColunasAplicacao(self, cAppl, codigoColuna):
        try:
            query = self.db((self.origemColunasAplicacao.codigoAplicacao == cAppl)
                           &(self.origemColunasAplicacao.codigoColuna == codigoColuna)).select()
            if  not query:
                codigoRegra = self.db(self.regras.descricao == "Inclusao").select().first().id
                origem = self.db(self.origemColunasApoio.origem == "CURRENT TIMESTAMP").select().first().id
                self.origemColunasAplicacao.insert(codigoAplicacao = cAppl
                                                  , codigoColuna = codigoColuna
                                                  , codigoRegra = codigoRegra
                                                  , origem = origem)
                self.db.commit()
        except:
            return False
        return True
