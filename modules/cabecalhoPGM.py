# -*- coding:utf-8
'''
   Created on 04/06/2012
   @author: C&C - HardSoft
'''

import io, os
from   datetime  import date
import Aplicacao
import Empresa
import Entidades
import utilities as utl

class cabecalhoPGM(object):

    def __init__(self
                , db
                , cAppl=None
                , entidadeId=None
                , objetivo=None
                , pgmid=None
                , servico=None
                , tppgm=None
                , userName=None
                ):
        self.cAppl          = cAppl or 0
        self.entidadeId     = entidadeId or 0
        self.objetivo       = objetivo or 'OBJETIVO'
        self.pgmid          = pgmid.upper() or 'XXX'
        self.servico        = servico.upper() or 'SERVICO'
        self.tppgm          = tppgm or 0
        self.userName       = userName.upper() or 'USER ADMIN'
        self.aplicacao      = Aplicacao.Aplicacao(db, self.cAppl)
        self.empresa        = Empresa.Empresa(db, self.aplicacao.getEmpresaId())
        Entidade            = Entidades.Entidades(db, cAppl=self.cAppl)
        self.entidade       = Entidade.selectEntidadesByEntidadeId(self.entidadeId)[1][0]
        self.parametros     = db.parametros
        self.parms          = db(self.parametros).select()[0]


    def montaCabecalho(self):
        dic                 = {}
        dic['@ANALISTA']    = utl.remover_acentos(self.aplicacao.getAnalista() + '/' + self.empresa.getNome()).upper()
        dic['@APPLID']      = self.aplicacao.getApplId().upper()
        dic['@APPLNAME']    = utl.remover_acentos(self.aplicacao.getApplName()).upper()
        dic['@AUTHOR']      = utl.remover_acentos(self.userName + '/' + self.aplicacao.getContratante()).upper()
        dic['@DATE']        = date.today().strftime('%d/%m/%Y')
        dic['@EMPRESA']     = utl.remover_acentos(self.empresa.getDescricao()).upper()
        dic['@ENTIDADE0']   = self.entidade.nomeExterno + ' - ' + self.entidade.nomeFisico
        dic['@ENTIDADE1']   = self.entidade.nomeAmigavel.upper()[:45]
        dic['@ENTIDADE2']   = self.entidade.nomeAmigavel.upper()[45:]
        dic['@GRUPO']       = self.aplicacao.getGrupo()
        dic['@OBJETIVO']    = self.objetivo.upper()
        dic['@PGMID']       = str(self.pgmid)
        dic['@SERVICO']     = utl.remover_acentos(self.servico).upper()
        dic['@TPPGM']       = str(self.tppgm)

        template            = os.path.join( '\\\\'
                                          , '127.0.0.1'
                                          , 'c$'
                                          , self.parms.web2py
                                          , 'applications'
                                          , self.parms.soag
                                          , 'Template'
                                          , 'PGM'
                                          , 'cabecalho.cbl')

        with open(template) as f:
            templ=str(f.read())

        return utl.change(dic, templ)
