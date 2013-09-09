# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import os
from Aplicacao                     import Aplicacao
from Empresa                       import Empresa
from Entidades                     import Entidades
from Colunas                       import Colunas
from ColunasEntidades              import ColunasEntidades
from ColunasEntidadesReferenciadas import ColunasEntidadesReferenciadas
from Programas                     import Programas
from Mensagens                     import Mensagens
from PrimaryKeys                   import PrimaryKeys
from ForeignKeys                   import ForeignKeys
from OrigemColunasAplicacao        import OrigemColunasAplicacao
from RegrasColunas                 import RegrasColunas
from GerBook                       import GerBook
from GerProg                       import GerProg
from CompactPy                     import Compact
from Gerutl                        import *

class Gerserv(object):

    def __init__(self, db, sessionId=None, cAppl=None, userName=None, gerar=True):
        self.gerar = gerar
        self.db = db
        self.cAppl = cAppl or 0
        self.aplicacao = Aplicacao(self.db, self.cAppl)
        self.applId = self.aplicacao.getApplId().upper()
        self.applName = ra(self.aplicacao.getApplName()).upper()
        self.contratante = self.aplicacao.getContratante().upper()
        self.analista = self.aplicacao.getAnalista().upper()
        self.ownerDb2 = self.aplicacao.getOwnerDb2().upper()
        self.grupo = self.aplicacao.getGrupo()
        self.soag = self.aplicacao.getSoag()
        self.delecaoLogica = self.aplicacao.getDelecaoLogica()
        self.colDelLog = self.aplicacao.getColunaDelecaoLogica()
        self.empresa = Empresa(self.db, self.aplicacao.getEmpresaId()).getNome().upper()
        self.entidades = Entidades(self.db)
        self.colunas = Colunas(self.db, self.cAppl)
        if  self.delecaoLogica:
            self.colDelLogName = self.colunas.selectColunasByColumnId(self.colDelLog)[1][0].columnName
        self.colunasEntidades = ColunasEntidades(self.db)
        self.ColunasEntidadesReferenciadas = ColunasEntidadesReferenciadas(self.db)
        self.programas = Programas(self.db)
        self.mensagens = Mensagens(self.db, cAppl=self.cAppl)
        self.primaryKeys = PrimaryKeys(self.db)
        self.foreignKeys = ForeignKeys(self.db)
        self.OrigemColunasAplicacao = OrigemColunasAplicacao(self.db)
        self.regrasColunas = RegrasColunas(self.db)
        self.bookSaiB = False
        self.userName = userName.upper()
        self.sessionId = sessionId or '1'
        self.parametros = self.db.parametros
        self.parms = self.db(self.parametros).select()[0]
        self.log = os.path.join( '\\\\', '127.0.0.1', 'c$', self.parms.log, "gerpro_%s.log" % (self.sessionId))
        arq = open(self.log, 'w')
        arq.close()
        self.gerBook = GerBook(self.db)
        self.gerProg = GerProg(self.db)
        self.compact = Compact(self.db)
        self.validarPK = 0

        self.ret=[]

    def gerserv(self, entidadeId=None):
        entidadeId = entidadeId or 0
        gerados = 0
        retEntidade = self.entidades.selectEntidadesByEntidadeId(entidadeId)
        if  not retEntidade[0]:
            return [0,'Ocorreu um erro na chamada de selectEntidadesByEntidadeId.', entidade[1]]
        entidade = retEntidade[1][0]
        retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidadeId)
        if  not retColunasEntidades[0]:
            if  retColunasEntidades[1]:
                return [0, retColunasEntidades[2]]
            else:
                return [0, 'Nao existem colunas para esta Entidade']
        colunasEntidade = retColunasEntidades[1]
        coo = []
        pgm = []
        coo.append(entidade.coordenadorInclusao)
        pgm.append(entidade.pgmInclusao)
        coo.append(entidade.coordenadorAlteracao)
        pgm.append(entidade.pgmAlteracao)
        coo.append(entidade.coordenadorExclusao)
        pgm.append(entidade.pgmExclusao)
        coo.append(entidade.coordenadorConsulta)
        pgm.append(entidade.pgmConsulta)
        coo.append(entidade.coordenadorLista)
        pgm.append(entidade.pgmLista)
        typePgm = 'IAECL'
        persistencia = 'IUDSS'
        servico = ('INCLUSAO', 'ALTERACAO', 'EXCLUSAO', 'CONSULTA', 'CONSULTALISTA')
        messageErro = [0, 0, 0, 1, 1]
        path = os.path.join( '\\\\', '127.0.0.1', 'c$', self.parms.raiz, self.empresa, self.applId)
        for i in xrange(5):
            if  not pgm[i]:
                continue
            retPrograma = self.programas.selectProgramasByEntidadeRegra(entidadeId, typePgm[i])
            if  not retPrograma[0]:
                return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.', retPrograma[1]]
            programa = retPrograma[1][0]
            self.bookSaiB = programa.bookSaida
            if  self.bookSaiB:
                bookSaida = 'S'
            else:
                bookSaida = ''
            properties = {}
            properties['ANALISTA']=self.analista
            properties['OWNERDB2']=self.ownerDb2
            properties['APPLID']=self.applId
            properties['APPLNAME']=self.applName
            properties['BOOKS']='E ' + bookSaida
            properties['CONTRATANTE']=self.contratante
            properties['COORDENADOR']= True if coo[i] else False
            properties['DCLGEN']=entidade.nomeExterno
            properties['EMPRESA']=self.empresa
            properties['ENTIDADE']=entidade.nomeAmigavel.upper()
            properties['GRUPO']=self.grupo
            properties['SERVICO']=servico[i]
            properties['SIGLAPGM']=programa.nomePrograma
            properties['TABLENAME']=entidade.nomeFisico
            properties['TYPEPGM']=typePgm[i]
            properties['PERSISTENCIA']=persistencia[i]
            properties['USERNAME']=self.userName
            properties['LOG']=self.log
            retMessage = self.montaMensagem(entidadeId, 'E', 'S', typePgm[i])
            if  not retMessage[0]:
                return retMessage
            properties['MSGSUCESSO']=retMessage[1]
            if  i == 0:
                self.validarPK = 0
                if  self.primaryKeys.primaryKeyInformada(entidadeId):
                    messageErro[0] = 1
                    self.validarPK = 1
            if  messageErro[i]:
                retMessage = self.montaMensagem(entidadeId, 'E', 'E', typePgm[i])
                if  not retMessage[0]:
                    return retMessage
                properties['MSGERRO']=retMessage[1]
                properties['LOG']=self.log
            else:
                properties['MSGERRO']=''

            gerados += 1

            retGerarColunas = self.gerarColunas(colunasEntidade
                                               ,entidadeId
                                               ,typePgm[i])
            if  not retGerarColunas[0]:
                return [0, 'Ocorreu algum erro >>> ' + retGerarColunas[1] + ' <<< na geracao das colunas']

            if  self.gerar:
                self.gerBook.gerBook(properties, retGerarColunas[1])
                self.gerProg.gerProg(properties, retGerarColunas[1])
            else:
                self.ret.append([properties , retGerarColunas[1]])

        if  self.gerar:
            cpy = os.path.join( path, 'GERADOS', 'CPY')
            pgm = os.path.join( path, 'GERADOS', 'PGM')
            self.compact.compact(entidade.nomeExterno, [cpy, pgm])
            print 'Servicos Gerados = ' + str(gerados)
            return [1, 'Servicos Gerados = ' + str(gerados)]
        else:
            return [1, self.ret]


    def gerarColunas(self, colunasEntidade, entidadeId, typePgm):
        retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidadeId)
        if  not retColunasEntidades[0]:
            if  retColunasEntidades[1]:
                return [0, retColunasEntidades[2]]
            else:
                return [0, 'Nao existem colunas para esta Entidade']
        colunasEntidade = retColunasEntidades[1]

        dicPrimaryKeys = self.primaryKeys.selectPrimaryKeysByCodigoEntidade(entidadeId)
        dicForeignKeys = self.foreignKeys.selectForeignKeysByCodigoEntidade(entidadeId)

        lisBookE = []
        lisBookI = []
        lisBookS = []
        lisBookR = []
        lisCol = []
        dicCol = {}
        auxBookI = []
        dicRegras = {}
        pks = []
        dicModulos = {}

        if  typePgm == 'L':
            col = self.colunas.selectColunasResolvidasByColumnName('NREG_QTDE')[1][0]
            self.EntityColumns(col, lisCol, dicCol)
            self.bookSaida(col, lisBookS)

        for col in colunasEntidade:

#>>>>>>> Regras de Dominio
            retRegras = self.regrasColunas.selectRegrasColunasByColumnId(col.colunas.id)
            if  not retRegras[0] and retRegras[1]:
                return [0,'Ocorreu um erro na chamada de selectRegrasColunasByColumnId.', retRegras[2]]
            regras = retRegras[1]

            self.rowsPrimaryKeys(col, dicPrimaryKeys, pks)
            self.EntityColumns(col, lisCol, dicCol)

#>>>>>>>>> Inclusao
            if  typePgm == 'I':
           #>>>>>> Book de Entrada

                if  col.colunasEntidades.inclusaoEntrada:

                 # Verifica se a coluna tem Origem
                    retOrigemColuna = self.origemColuna(col, dicRegras, auxBookI, dicPrimaryKeys, typePgm)
                    if  not retOrigemColuna[0]:
                        return retOrigemColuna

                 # Coluna tem Origem do FrameWork
                    if  retOrigemColuna[1] == 2 :
                        retRegraPreenchimento = self.regraPreenchimento(col, dicRegras)
                        if  not retRegraPreenchimento[0]:
                            return retRegraPreenchimento

                 # Coluna nao tem Origem ou eh Primary Key Informada
                    if  not retOrigemColuna[1]                                 \
                     or self.ehPrimaryKeyInformada(col, dicPrimaryKeys, typePgm):

                        self.bookEntrada(col, lisBookE)
                        self.bookInterface(col, lisBookI)

                      #>> Regra Preenchimento
                        retRegraPreenchimento = self.regraPreenchimento(col, dicRegras)
                        if  not retRegraPreenchimento[0]:
                            return retRegraPreenchimento

                      #>> Regra Data
                        self.regraData(col, dicRegras)

                      #>> Regra Time
                        self.regraTime(col, dicRegras)

                      #>> Regra Timestamp
                        self.regraTimestamp(col, dicRegras)

                      #>> Regras de Dominio
                        retRegrasDominio = self.regrasDominio(col, regras, dicRegras)
                        if  not retRegrasDominio[0]:
                            return retRegrasDominio

                      #>> Regra Nao Existencia na própria entidade
                        regraEx = 'NX'
                        retExisteEntidade = self.existeEntidade(entidadeId, col, dicPrimaryKeys, regraEx, typePgm, dicRegras)
                        if  not retExisteEntidade[0]:
                            return retExisteEntidade

                      #>> Regra Existencia nas Entidades Relacionadas
                        retEntidadeRelacionada = self.entidadeRelacionada(col, dicForeignKeys, dicRegras, typePgm)
                        if  not retEntidadeRelacionada[0]:
                            return retEntidadeRelacionada


           #>>>>>> Book de Saida
                if  col.colunasEntidades.inclusaoSaida:
                    self.bookSaida(col, lisBookS)

#>>>>>>>>> Alteracao
            elif  typePgm == 'A':
           #>>>>>> Book de Entrada
                if  col.colunasEntidades.alteracaoEntrada:

                 # Verifica se a coluna tem Origem
                    retOrigemColuna = self.origemColuna(col, dicRegras, auxBookI, dicPrimaryKeys, typePgm)
                    if  not retOrigemColuna[0]:
                        return retOrigemColuna

                 # Coluna tem Origem do FrameWork
                    if  retOrigemColuna[1] == 2:
                        retRegraPreenchimento = self.regraPreenchimento(col, dicRegras)
                        if  not retRegraPreenchimento[0]:
                            return retRegraPreenchimento

                 # Coluna não tem Origem ou eh Primary Key Informada
                    if  not retOrigemColuna[1]                            \
                     or self.ehPrimaryKeyInformada(col, dicPrimaryKeys, typePgm):

                        self.bookEntrada(col, lisBookE)
                        self.bookInterface(col, lisBookI)

                      #>> Regra Preenchimento
                        retRegraPreenchimento = self.regraPreenchimento(col, dicRegras)
                        if  not retRegraPreenchimento[0]:
                            return retRegraPreenchimento

                      #>> Regra Data
                        self.regraData(col, dicRegras)

                      #>> Regra Time
                        self.regraTime(col, dicRegras)

                      #>> Regra Timestamp
                        self.regraTimestamp(col, dicRegras)

                      #>> Regras de Dominio
                        retRegrasDominio = self.regrasDominio(col, regras, dicRegras)
                        if  not retRegrasDominio[0]:
                            return retRegrasDominio

                      #>> Regra Existencia na própria entidade
                        regraEx = 'EX'
                        retExisteEntidade = self.existeEntidade(entidadeId, col, dicPrimaryKeys, regraEx
                                                               , typePgm, dicRegras)
                        if  not retExisteEntidade[0]:
                            return retExisteEntidade


                      #>> Regra Existencia nas Entidades Relacionadas
                        retEntidadeRelacionada = self.entidadeRelacionada(col, dicForeignKeys, dicRegras, typePgm)
                        if  not retEntidadeRelacionada[0]:
                            return retEntidadeRelacionada

           #>>>>>> Book de Saida
                if  col.colunasEntidades.alteracaoSaida:
                    self.bookSaida(col, lisBookS)

#>>>>>>>>>>>>>> Exclusao
            elif  typePgm == 'E':
           #>>>>>> Book de Entrada
                if  col.colunasEntidades.exclusaoEntrada:
                    self.bookEntrada(col, lisBookE)
                    self.bookInterface(col, lisBookI)

               #>> Regra Preenchimento
                    retRegraPreenchimento = self.regraPreenchimento(col, dicRegras)
                    if  not retRegraPreenchimento[0]:
                        return retRegraPreenchimento

               #>> Regra Data
                    self.regraData(col, dicRegras)

               #>> Regra Time
                    self.regraTime(col, dicRegras)

               #>> Regra Timestamp
                    self.regraTimestamp(col, dicRegras)

               #>> Regras de Dominio
                    retRegrasDominio = self.regrasDominio(col, regras, dicRegras)
                    if  not retRegrasDominio[0]:
                        return retRegrasDominio

               #>> Regra Existencia na própria entidade
                    regraEx = 'EX'
                    retExisteEntidade = self.existeEntidade(entidadeId, col, dicPrimaryKeys, regraEx, typePgm, dicRegras)
                    if  not retExisteEntidade[0]:
                        return retExisteEntidade


           #>>>>>> Book de Saida
                if  col.colunasEntidades.exclusaoSaida:
                    self.bookSaida(col, lisBookS)

#>>>>>>>>>>>>>> Consulta
            elif  typePgm == 'C':
           #>>>>>> Book de Entrada
                if  col.colunasEntidades.consultaEntrada:
                    self.bookEntrada(col, lisBookE)
                    self.bookInterface(col, lisBookI)

               #>> Regra Preenchimento
                    retRegraPreenchimento = self.regraPreenchimento(col, dicRegras)
                    if  not retRegraPreenchimento[0]:
                        return retRegraPreenchimento

               #>> Regra Data
                    self.regraData(col, dicRegras)

               #>> Regra Time
                    self.regraTime(col, dicRegras)

               #>> Regra Timestamp
                    self.regraTimestamp(col, dicRegras)

               #>> Regras de Dominio
                    retRegrasDominio = self.regrasDominio(col, regras, dicRegras)
                    if  not retRegrasDominio[0]:
                        return retRegrasDominio


           #>>>>>> Book de Saida
                if  col.colunasEntidades.consultaSaida:
                    self.bookSaida(col, lisBookS)

              #>> Regra Existencia nas Entidades Relacionadas
                retEntidadeRelacionada = self.entidadeRelacionada(col, dicForeignKeys, dicRegras, typePgm)
                if  not retEntidadeRelacionada[0]:
                    return retEntidadeRelacionada

#>>>>>>>>>>>>>> Lista
            else:
           #>>>>>> Book de Entrada
                if  col.colunasEntidades.listaEntrada:
                    self.bookEntrada(col, lisBookE)
                    self.bookInterface(col, lisBookI)

               #>> Regra Preenchimento
                    retRegraPreenchimento = self.regraPreenchimento(col, dicRegras)
                    if  not retRegraPreenchimento[0]:
                        return retRegraPreenchimento

               #>> Regra Data
                    self.regraData(col, dicRegras)

               #>> Regra Time
                    self.regraTime(col, dicRegras)

               #>> Regra Timestamp
                    self.regraTimestamp(col, dicRegras)

               #>> Regras de Dominio
                    retRegrasDominio = self.regrasDominio(col, regras, dicRegras)
                    if  not retRegrasDominio[0]:
                        return retRegrasDominio


           #>>>>>> Book de Saida
                if  col.colunasEntidades.listaSaida:
                    self.bookSaida(col, lisBookS)

              #>> Regra Existencia nas Entidades Relacionadas
                retEntidadeRelacionada = self.entidadeRelacionada(col, dicForeignKeys, dicRegras, typePgm)
                if  not retEntidadeRelacionada[0]:
                    return retEntidadeRelacionada

        retColunasEntidades = self.ColunasEntidadesReferenciadas.selectColunasEntidadesReferenciadasByCodigoEntidade(entidadeId)
        if  not retColunasEntidades[0]:
            if  retColunasEntidades[1]:
                return [0, retColunasEntidades[2]]
            else:
                return [0, 'Nao existem colunas para esta Entidade']
        colunasEntidade = retColunasEntidades[1]

        for col in colunasEntidade:
#>>>>>>>>>>>>>> Consulta
            if  typePgm == 'C':
           #>>>>>> Book de Saida
                if  col.colunasEntidadesReferenciadas.consultaSaida:
                    self.bookRefer(col, lisBookR)
                    self.EntityColumns(col, lisCol, dicCol)

                  #>> Regra Coluna Existente em Entidades relacionadas
                    retColunaEntidadeRelacionada = self.colunaEntidadeRelacionada(col, dicModulos)
                    if  not retColunaEntidadeRelacionada[0]:
                        return retColunaEntidadeRelacionada

#>>>>>>>>>>>>>> Lista
            elif  typePgm == 'L':
           #>>>>>> Book de Saida
                if  col.colunasEntidadesReferenciadas.listaSaida:
                    self.bookRefer(col, lisBookR)
                    self.EntityColumns(col, lisCol, dicCol)

                  #>> Regra Coluna Existente em Entidades relacionadas
                    retColunaEntidadeRelacionada = self.colunaEntidadeRelacionada(col, dicModulos)
                    if  not retColunaEntidadeRelacionada[0]:
                        return retColunaEntidadeRelacionada

        for column in auxBookI:
            lisBookI.append(column)
        return [1, [lisBookE, lisBookI, lisBookS, lisBookR, lisCol, dicCol, dicRegras, pks, dicModulos]]

    def EntityColumns(self, col, lisCol, dicCol):
        lisCol.append(col.colunas.columnName)
        dicCol[col.colunas.columnName]=col

    def bookEntrada(self, col, lisBookE):
        lisBookE.append(col.colunas.columnName)

    def bookInterface(self, col, lisBookI):
        lisBookI.append(col.colunas.columnName)

    def bookSaida(self, col, lisBookS):
        lisBookS.append(col.colunas.columnName)

    def bookRefer(self, col, lisBookR):
        lisBookR.append(col.colunas.columnName)

    def origemColuna(self, col, dicRegras, auxBookI, dicPrimaryKeys, typePgm):
        retOrigemColuna = self.OrigemColunasAplicacao.selectOrigemColunasAplicacaoByCodigoColuna(col.colunas.id)
        if  not retOrigemColuna[0]:
            return [0,'Ocorreu um erro na chamada de selectorigemColunasAplicacaoByCodigoColuna.' + str(retOrigemColuna[2])]
        if  not retOrigemColuna[1]:
            return [1, 0]
        if  self.ehPrimaryKeyInformada(col, dicPrimaryKeys, typePgm):
            return [1, 0]
        origemColuna = retOrigemColuna[1][0]
        dic = {'origem':origemColuna.origemColunasApoio.origem,
               'fonte':origemColuna.origemColunasApoio.fonte}
        if  col.colunas.columnName in dicRegras:
            oldDic = dicRegras[col.colunas.columnName]
            oldDic['OR']=dic
            dicRegras[col.colunas.columnName]=oldDic
        else:
            dicRegras[col.colunas.columnName]={'OR':dic}

        if  origemColuna.origemColunasApoio.fonte == 'S':
            return [1, 1]
      # Origem do FrameWork
        auxBookI.append(col.colunas.columnName)
        return [1, 2]

    def regraPreenchimento(self, col, dicRegras):
        if  col.colunasEntidades.ehNotNull:
            retMessage = self.montaMensagem(col.colunas.id, 'C', 'E', 'PR', nova=1)
            if  not retMessage[0]:
                return retMessage
            dic = {'message':retMessage[1]}
            if  col.colunas.columnName in dicRegras:
                oldDic = dicRegras[col.colunas.columnName]
                oldDic['PR']=dic
                dicRegras[col.colunas.columnName]=oldDic
            else:
                dicRegras[col.colunas.columnName]={'PR':dic}
        return [1]

    def regraData(self, col, dicRegras):
        if  col.datatypes.descricao == 'DATE':
            if  col.colunas.columnName in dicRegras:
                oldDic = dicRegras[col.colunas.columnName]
                oldDic['DT']=''
                dicRegras[col.colunas.columnName]=oldDic
            else:
                dicRegras[col.colunas.columnName]={'DT':''}

    def regraTime(self, col, dicRegras):
        if  col.datatypes.descricao == 'TIME':
            if  col.colunas.columnName in dicRegras:
                oldDic = dicRegras[col.colunas.columnName]
                oldDic['TM']=''
                dicRegras[col.colunas.columnName]=oldDic
            else:
                dicRegras[col.colunas.columnName]={'TM':''}

    def regraTimestamp(self, col, dicRegras):
        if  col.datatypes.descricao == 'TIMESTAMP':
            if  col.colunas.columnName in dicRegras:
                oldDic = dicRegras[col.colunas.columnName]
                oldDic['TS']=''
                dicRegras[col.colunas.columnName]=oldDic
            else:
                dicRegras[col.colunas.columnName]={'TS':''}

    def regrasDominio(self, col, regras, dicRegras):
        for r in regras:
            retMessage = self.montaMensagem(col.colunas.id, 'C', 'E', r.regras.regra, nova=1)
            if  not retMessage[0]:
                return retMessage
            dic = {'regra':r
                  ,'message':retMessage[1]}
            if  col.colunas.columnName in dicRegras:
                oldDic = dicRegras[col.colunas.columnName]
                oldDic[r.regras.regra]=dic
                dicRegras[col.colunas.columnName]=oldDic
            else:
                dicRegras[col.colunas.columnName]={r.regras.regra:dic}
        return [1]

    def ehPrimaryKeyInformada(self, col, dicPrimaryKeys, typePgm):
        if  col.colunas.id in dicPrimaryKeys:
            if  (typePgm == 'I' and dicPrimaryKeys[col.colunas.id] != 3) \
            or (typePgm != 'I'):
                return 1
        return 0

    def existeEntidade(self, entidadeId, col, dicPrimaryKeys, regraEx, typePgm, dicRegras):
        if  col.colunas.id in dicPrimaryKeys:
            if  ((typePgm == 'I' and self.validarPK)
             or (typePgm != 'I')):
                retPrograma = self.programas.selectProgramasByEntidadeRegra(entidadeId, 'C')
                if  not retPrograma[0]:
                    return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.' + str(retPrograma[2])]
                pgmConsulta = retPrograma[1][0]
                if  self.soag:
                    modulo = self.applId + '3' + pgmConsulta.nomePrograma + 'C'
                    interface = self.applId + 'W' + pgmConsulta.nomePrograma + 'I'
                    controle = self.applId + 'W00C'
                else:
                    modulo = pgmConsulta.nomePrograma
                    interface = pgmConsulta.bookInterface
                    controle = pgmConsulta.bookControle
                dic = {'modulo':modulo
                      ,'interface':interface
                      ,'controle':controle
                      ,'coluna':col.colunas.columnName}
                if  col.colunas.columnName in dicRegras:
                    oldDic = dicRegras[col.colunas.columnName]
                    oldDic[regraEx]=dic
                    dicRegras[col.colunas.columnName]=oldDic
                else:
                    dicRegras[col.colunas.columnName]={regraEx:dic}
        return [1]

    def rowsPrimaryKeys(self, col, dicPrimaryKeys, pks):
        if  col.colunas.id in dicPrimaryKeys:
            pks.append((col.colunas.columnName, str(dicPrimaryKeys[col.colunas.id])))

    def entidadeRelacionada(self, col, dicForeignKeys, dicRegras, typePgm):
        if  col.colunas.id in dicForeignKeys:
            entidadeIdRef = dicForeignKeys[col.colunas.id][0]
            retPrograma = self.programas.selectProgramasByEntidadeRegra(entidadeIdRef, 'C')
            if  not retPrograma[0]:
                if  retPrograma[1]:
                    return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.' + str(retPrograma[2])]
                else:
                    return [1]
            pgmConsulta = retPrograma[1][0]
            if  pgmConsulta.codigoAplicacao == self.cAppl:
                soag = self.soag
            else:
                soag = Aplicacao(self.db, pgmConsulta.codigoAplicacao).getSoag()
            if  soag:
                modulo = self.applId + '3' + pgmConsulta.nomePrograma + 'C'
                interface = self.applId + 'W' + pgmConsulta.nomePrograma + 'I'
                controle = self.applId + 'W00C'
            else:
                modulo = pgmConsulta.nomePrograma
                interface = pgmConsulta.bookInterface
                controle = pgmConsulta.bookControle
            if  dicForeignKeys[col.colunas.id][1] == col.colunas.id:
                coluna = col.colunas.columnName
            else:
                retColRef = self.colunas.selectColunasByColumnId(dicForeignKeys[col.colunas.id][1])
                if  not retColRef:
                    return [0,'Ocorreu um erro na chamada de selectColunasByColumnId.' + str(retColRef[2])]
                coluna = retColRef[1][0].columnName
            if  typePgm == 'C':
                if  col.colunasEntidades.consultaSaida:
                    esif = 'S'
                else:
                    esif = 'E'
            elif  typePgm == 'L':
                if  col.colunasEntidades.listaSaida:
                    esif = 'S'
                else:
                    esif = 'E'
            else:
                  esif = ''

            dic = {'modulo':modulo
                  ,'interface':interface
                  ,'controle':controle
                  ,'coluna':coluna}
#                  ,'esif':esif}
            if  col.colunas.columnName in dicRegras:
                oldDic = dicRegras[col.colunas.columnName]
                oldDic['EX']=dic
                dicRegras[col.colunas.columnName]=oldDic
            else:
                dicRegras[col.colunas.columnName]={'EX':dic}

#>>>>>>> regra Registro Ativo
#            if  self.delecaoLogica:
#                retColunaDelecaoLogica = self.colunasEntidades.selectColunasEntidadesByCodigoEntidadeCodigoColuna \
#                                         (entidadeIdRef, self.colDelLog)
#                if  not retColunaDelecaoLogica[0]:
#                    return [0,'Ocorreu um erro na chamada de selectColunasEntidadesByCodigoEntidadeCodigoColuna.' \
#                             + str(retColunaDelecaoLogica[2])]
#                if  (retColunaDelecaoLogica[1]
#                and dicForeignKeys[col.colunas.id][2]):
#                    retMessage = self.montaMensagem(entidadeIdRef, 'E', 'E', 'AT', nova=1)
#                    if  not retMessage[0]:
#                        return retMessage
#                    dic = {'modulo':modulo
#                          ,'colDelLogName':self.colDelLogName
#                          ,'message':retMessage[1]}
#                    if  col.colunas.columnName in dicRegras:
#                        oldDic = dicRegras[col.colunas.columnName]
#                        oldDic['AT']=dic
#                        dicRegras[col.colunas.columnName]=oldDic
#                    else:
#                        dicRegras[col.colunas.columnName]={'AT':dic}
        return [1]

    def colunaEntidadeRelacionada(self, col, dicModulos):
        entidadeIdRef = col.colunasEntidadesReferenciadas.entidadeReferenciada
        retPrograma = self.programas.selectProgramasByEntidadeRegra(entidadeIdRef, 'C')
        if  not retPrograma[0]:
            if  retPrograma[1]:
                return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.' + str(retPrograma[2])]
            else:
                return [1]
        pgmConsulta = retPrograma[1][0]
        if  pgmConsulta.codigoAplicacao == self.cAppl:
            soag = self.soag
        else:
            soag = Aplicacao(self.db, pgmConsulta.codigoAplicacao).getSoag()
        if  soag:
            modulo = self.applId + '3' + pgmConsulta.nomePrograma + 'C'
            interface = self.applId + 'W' + pgmConsulta.nomePrograma + 'I'
            controle = self.applId + 'W00C'
        else:
            modulo = pgmConsulta.nomePrograma
            interface = pgmConsulta.bookInterface
            controle = pgmConsulta.bookControle

        dic = {'modulo':modulo
              ,'interface':interface
              ,'controle':controle}

        dicModulos[col.colunas.columnName]=dic
        return [1]

    def montaMensagem(self, codigoEntCol, origemMsg, tipoMsg, regra, nova=None):
        retMessage = self.mensagens.getMensagem(codigoEntCol, origemMsg, tipoMsg, regra, nova)
        if  not retMessage[0]:
            return [0, 'Ocorreu um erro na chamada de getMensagem.'  + str(retMessage[2])]
        return [1, '{}{:04}'.format(self.applId, retMessage[1])]
