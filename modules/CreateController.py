# -*- coding:utf-8
'''
   Created on 04/06/2013
   @author: C&C - HardSoft
'''

import os, sys, traceback
from utilities import *
from Aplicacao import Aplicacao
from Entidades import Entidades
from ColunasEntidades import ColunasEntidades
from PrimaryKeys import PrimaryKeys
from OrigemColunasAplicacao import OrigemColunasAplicacao
from Mensagens import Mensagens



class CreateController(object):

    def __init__(self, db, cAppl=0, info=False):
        self.db = db
        self.cAppl = cAppl
        self.info = info
        self.aplicacao = Aplicacao(self.db, self.cAppl)
        self.applId = self.aplicacao.getApplId()
        modeloDB = {0:'Soag', 1:'legacy'}
        self.modeloDb = modeloDB[self.aplicacao.getModeloDb()]
        self.entidades = Entidades(self.db, cAppl=self.cAppl)
        self.colunasEntidades = ColunasEntidades(self.db)
        self.primaryKeys = PrimaryKeys(self.db)
        self.OrigemColunasAplicacao = OrigemColunasAplicacao(self.db)
        self.mensagens = Mensagens(self.db, cAppl=self.cAppl)
        self.menu = self.db.menu
        self.parametros = self.db.parametros
        self.parms = self.db(self.parametros).select()[0]
        self.checkListPrototipo = self.db.checkListPrototipo
        self.pathApp = os.path.join('\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', self.applId)
        self.pathTempl = os.path.join( '\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', self.parms.soag
                                      , 'Template', 'web2py', 'templates')

    def createController(self):
        try:
            template = open(os.path.join(self.pathTempl, 'controller.py')).read()
            query=self.db(self.menu.codigoAplicacao == self.cAppl).select()
            labelController = ''
            nomeController = ''
            for q in query:
                if  q.url == 0:
                    continue

                retEntidade = self.entidades.selectEntidadesByEntidadeId(q.url)
                if  not retEntidade[0]:
                    if  self.info:
                        return False, traceback.format_exc(sys.exc_info)
                    else:
                        return False, None
                ent = retEntidade[1][0]

                if  ent.pgmExclusao:
                    deletable = ', deletable=True'
                    optionDelete= 'True'
                    msgexcluida = self.montaMensagem(ent.id, 'E', 'S', 'E')
                else:
                    deletable = ', deletable=False'
                    optionDelete= 'False'
                    msgexcluida = ''
                if  ent.pgmAlteracao:
                    msgalterada = self.montaMensagem(ent.id, 'E', 'S', 'A')
                else:
                    msgalterada = ''
                if  ent.pgmInclusao:
                    msgincluida = self.montaMensagem(ent.id, 'E', 'S', 'I')
                else:
                    msgincluida = ''

                auto = False
                dicPK = {}
                retPK = self.primaryKeys.selectPrimaryKeysByCodigoEntidade(ent.id)
                if  retPK:
                    dicPK = retPK

                campos, lengths, dicOrigIncl, dicOrigAlt, dicCols, pks, lisCols = self.colunasEntidade(ent.id, dicPK)

                importDatetime = importNumAuto = False
                inclusao = alteracao = imports = ''

                sp = 12

                for k in dicPK.keys():
                    if  dicPK[k] == 3 and dicCols[k].datatypes.descricao != 'TIMESTAMP':
                        auto = True

                if  auto:
                    where = ''
                    spn = sp
                    imports += 'from numAuto import numAuto\n'
                    if  len(dicPK) == 1:
                        where += '{:{}}where = ({})\n'.format('', sp, ent.nomeFisico)
                        column = dicCols[dicPK.keys()[0]].colunas.columnName
                        campo = '{:{}}campo = ({}.{})\n'.format('', sp, ent.nomeFisico, column)
                    else:
                        ifap = 'if  ('
                        for k in lisCols:
                            if  k not in dicPK.keys() or dicPK[k] == 3:
                                continue
                            column = dicCols[k].colunas.columnName
                            inclusao += '{:{}}{}request.vars.{} and\n'.format('', sp, ifap, column)
                            ifap = '     '
                        inclusao = inclusao[:-5] + '):\n'
                        spn += 4
                        lAnd  = 'where = ('
                        for k in lisCols:
                            if  k not in dicPK.keys():
                                continue
                            column = dicCols[k].colunas.columnName
                            if  dicPK[k] != 3:
                                where += '{0:{1}}{2}({3}.{4}==int(request.vars.{4}))\n'.format(''
                                                                                              , spn
                                                                                              , lAnd
                                                                                              ,ent.nomeFisico
                                                                                              ,column)
                                lAnd  = '        &'
                            else:
                                campo = '{:{}}campo = ({}.{})\n'.format('', spn, ent.nomeFisico, column)
                        where=where[:-1] + ')\n'
                    nAuto = '{0:{1}}form.vars.{2} = request.vars.{2} = numAuto(db, campo, where)\n'.format(''
                                                                                                          , spn
                                                                                                          , column)
                    inclusao += where
                    inclusao += campo
                    inclusao += nAuto

                if  dicOrigIncl:
                    for k, v in dicOrigIncl.items():
                        if  v[0] == 'PARTITIONH' or v[0] == 'PARTITIONV':
                            inclusao += self.montaPartition(k, pks, v, sp)
                        else:
                            inclusao += '{0:{1}}form.vars.{2} = request.vars.{2} = {3}\n'.format('', sp, k, v[0])
                            if  'datetime' in v[0]:
                                importDatetime = True

                if  not inclusao:
                    inclusao = '{:>{}}\n'.format('pass', sp+4)

                if  dicOrigAlt:
                    for k, v in dicOrigAlt.items():
                        alteracao += '{0:{1}}form.vars.{2} = request.vars.{2} = {3}\n'.format('', sp, k, v[0])
                        if  'datetime' in v[0]:
                            importDatetime = True
                else:
                    alteracao = '{:>{}}\n'.format('pass', sp+4)

                if  importDatetime:
                    imports += 'import datetime\n'

                dic = {'@IMPORTS\n':imports
                      ,'@INCLUSAO\n':inclusao
                      ,'@ALTERACAO\n':alteracao
                      ,'@MSGEXCLUIDA':msgexcluida
                      ,'@MSGALTERADA':msgalterada
                      ,'@MSGINCLUIDA':msgincluida
                      ,'@DELETABLE':deletable
                      ,'@OPTIONDELETE':optionDelete
                      ,'@ENTIDADE':ent.nomeFisico
                      ,'@LABEL'   :q.descricao
                      ,'@QUERYID':'.id > 0' if self.modeloDb == 'Soag' else ''
                      ,'@FIELDSID':"'id'," if self.modeloDb == 'Soag' else ''
                      ,'@SCROLL':"'5%'," if self.modeloDb == 'Soag' else ''
                      ,'@CAMPOS'  :campos
                      ,'@LENGTHS' :lengths}

                nomeController = ''.join(Capitalize(ent.nomeFisico.replace('_',' ')).split())
                controller = open(os.path.join( self.pathApp
                                              , 'controllers'
                                              , nomeController + '.py'), 'w')
                controller.write(change(dic, template))
                controller.close()
                viewOrig = os.path.join(self.pathTempl, 'viewController')
                viewDest = os.path.join(self.pathApp, 'views', nomeController)
                try:
                    shutil.rmtree(viewDest)
                except:
                    pass
                shutil.copytree(viewOrig, viewDest)
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        return self.atualizaCheckListPrototipo()

    def colunasEntidade(self, entidadeId, dicPK):
        retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidadeId)
        if  not retColunasEntidades[0]:
            if  retColunasEntidades[1]:
                if  self.info:
                    return False, traceback.format_exc(sys.exc_info)
                else:
                    return False, None
            else:
                return [False, 'Nao existem colunas para esta Entidade']
        colunasEntidade = retColunasEntidades[1]
        dicOrigIncl = {}
        dicOrigAlt = {}
        dicCols = {}
        lisCols = []
        pks = []
        columns = ''
        n = 0
        for col in colunasEntidade:
            if  col.colunasEntidades.consultaSaida:
                n += 1
                if  n < 6:
                    columns += "'{}',".format(col.colunas.columnName)
                    nc = n
            dicCols[col.colunas.id]=col
            lisCols.append(col.colunas.id)
            origCol = self.origemColuna(col)
            if  origCol:
                if  origCol[0] == 'I':
                    dicOrigIncl[col.colunas.columnName]=[origCol[1], col.colunas.tamanhoColuna]
                elif origCol[0] == 'A':
                    dicOrigAlt[col.colunas.columnName]=[origCol[1], col.colunas.tamanhoColuna]
            if  col.colunas.id in dicPK.keys():
                pks.append(col.colunas.columnName)

        percent = 95 if self.modeloDb == 'Soag' else 100
        lengths = '{}'.format("'{:d}%',".format(int(percent/nc))*nc)[:-1]
        return columns, lengths, dicOrigIncl, dicOrigAlt, dicCols, pks, lisCols

    def origemColuna(self, col):
        origem = self.OrigemColunasAplicacao.selectOrigemColunasAplicacaoByCodigoColuna(col.colunas.id)
        if  origem[0] and origem[1]:
            return [origem[1][0].regras.regra, origem[1][0].origemColunasApoio.controller]
        else:
            return []

    def montaMensagem(self, codigoEntCol, origemMsg, tipoMsg, regra, nova=None):
        retMessage = self.mensagens.getMensagem(codigoEntCol, origemMsg, tipoMsg, regra, nova)
        if  retMessage[0]:
            return '{}{:04}'.format(self.applId, retMessage[1])
        else:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None

    def montaPartition(self, column, pks, pl, sp):
        partition = pl[0]
        lenCol = pl[1]
        pks = pks[:lenCol]
        iPk = iterInv(pks) if partition[-1] == 'V' else iter(pks)
        ifap = 'if  ('
        ret = ''
        for pk in iPk:
            ret += '{:{}}{}request.vars.{} and\n'.format('', sp, ifap, pk)
            ifap = '     '
        ret = ret[:-5] + '):\n'
        sp += 4
        retmp = "{0:{1}}form.vars.{2} = request.vars.{2} = '{3}'.format(".format(''
                                                                                , sp
                                                                                , column
                                                                                , '{}'.format('{}'* lenCol))
        lenRet = len(retmp)-1
        ret += retmp
        space = 1
        comma = ''
        iPk = iterInv(pks) if partition[-1] == 'V' else iter(pks)
        for pk in iPk:
            ret += '{:{}}{}int(request.vars.{}[-1])\n'.format('', space, comma, pk)
            space = lenRet
            comma = ', '
        for x in xrange(lenCol - len(pks)):
            ret += '{:{}}{}{}\n'.format('', space, comma, 0)
        ret = ret[:-1] + ')\n'
        return ret

    def atualizaCheckListPrototipo(self):
        try:
            self.db(self.checkListPrototipo.codigoAplicacao == self.cAppl).update(controllers = True)
        except:
            if  self.info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
        self.db.commit()
        return True, None
