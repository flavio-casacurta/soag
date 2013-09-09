# -*- coding:utf-8
'''
   Created on 27/04/2013
   @author: C&C - HardSoft
'''
from utilities import *
from Aplicacao import Aplicacao

class DumpMsg(object):

    def __init__(self, db, cAppl=0, info=False):
        self.db = db
        self.cAppl = cAppl
        self.aplicacao = Aplicacao(self.db, self.cAppl).getApplId()
        parms = db(db.parametros.id==1).select()[0]
        self.checkListPrototipo = self.db.checkListPrototipo
        self.fileDump = os.path.join('\\\\', '127.0.0.1', 'c$', parms.web2py, 'applications'
                                           , self.aplicacao, 'private', 'msgDump.pickle')

    def dumpMsg(self):
        try:
            sqlE = """
            SELECT aplicacoes.aplicacao
                 , mensagensentcol.codigoMensagem
                 , mensagenspadraoprefixo.descricao
                 , entidades.nomeamigavel
                 , mensagenspadraosufixo.descricao
              FROM ((((aplicacoes
                       INNER JOIN mensagensentcol
                               ON aplicacoes.id = mensagensentcol.codigoaplicacao)
                       INNER JOIN entidades
                               ON mensagensentcol.codigoentcol = entidades.id)
                       INNER JOIN mensagenspadrao
                               ON mensagensentcol.codigomsgpadrao = mensagenspadrao.id)
                       INNER JOIN mensagenspadraoprefixo
                               ON mensagenspadrao.codigomsgprefixo = mensagenspadraoprefixo.id)
                       INNER JOIN mensagenspadraosufixo
                               ON mensagenspadrao.codigomsgsufixo = mensagenspadraosufixo.id
             WHERE (((mensagensentcol.codigoaplicacao)={})
               AND  ((mensagensentcol.codigoorigemmsg)=1));
            """.format(self.cAppl)
            sqls = self.db.executesql(sqlE)
            msgs = {}

            for sql in sqls:
                msgs['{}{:04}'.format(sql[0],sql[1])]='{}'.format(((sql[2] + ' ' if sql[2].strip() else '') +
                                                                   (sql[3] + ' ' if sql[3].strip() else '') +
                                                                   (sql[4]       if sql[4].strip() else '')))

            sqlC = """
            SELECT aplicacoes.aplicacao
                 , mensagensentcol.codigoMensagem
                 , mensagenspadraoprefixo.descricao
                 , colunas.attributename
                 , mensagenspadraosufixo.descricao
                 , colunas.id
                 , mensagenspadrao.codigoregra
              FROM ((((aplicacoes
                       INNER JOIN mensagensentcol
                               ON aplicacoes.id = mensagensentcol.codigoaplicacao)
                       INNER JOIN colunas
                               ON mensagensentcol.codigoentcol = colunas.id)
                       INNER JOIN mensagenspadrao
                               ON mensagensentcol.codigomsgpadrao = mensagenspadrao.id)
                       INNER JOIN mensagenspadraoprefixo
                               ON mensagenspadrao.codigomsgprefixo = mensagenspadraoprefixo.id)
                       INNER JOIN mensagenspadraosufixo
                               ON mensagenspadrao.codigomsgsufixo = mensagenspadraosufixo.id
             WHERE (((mensagensentcol.codigoaplicacao)={})
               AND  ((mensagensentcol.codigoorigemmsg)=2));
            """.format(self.cAppl)

            sqls = self.db.executesql(sqlC)
            for sql in sqls:
                args = self.db.executesql("""SELECT regrascolunas.argumento1,
                                                    regrascolunas.argumento2
                                               FROM regrascolunas
                                              WHERE  regrascolunas.codigocoluna = {:d}
                                                AND  regrascolunas.codigoregra  = {:d};
                                          """.format(sql[5], sql[6]))
                msgs['{}{:04}'.format(sql[0],sql[1])]='{}{}{} {}'.format(((sql[2] + ' ' if sql[2].strip() else '') +
                                                                          (sql[3] + ' ' if sql[3].strip() else '') +
                                                                          (sql[4]       if sql[4].strip() else ''))
                                                                         ,' - ' if  args else ''
                                                                         ,args[0][0] if  args else ''
                                                                         ,args[0][1] if  args else '')


            pic(msgs, self.fileDump)

        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        return self.atualizaCheckListPrototipo()

    def atualizaCheckListPrototipo(self):
        try:
            self.db(self.checkListPrototipo.codigoAplicacao == self.cAppl).update(mensagens = True)
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        self.db.commit()
        return True, None
