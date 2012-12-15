# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import os, pdb
from Aplicacao                     import Aplicacao
from Entidades                     import Entidades
from ColunasEntidades              import ColunasEntidades
from ColunasEntidadesReferenciadas import ColunasEntidadesReferenciadas
from Mensagens                     import Mensagens
from PrimaryKeys                   import PrimaryKeys
from ForeignKeys                   import ForeignKeys

dicDataTypes={'CHAR':''
             ,'DATE':'date'
             ,'DECIMAL':'integer'
             ,'INTEGER':''integer''
             ,'TIMESTAMP':'datetime'
             ,'VARCHAR':'text'}

class CreateTables:

    def __init__(self, db, sessionId=None, cAppl=None, userName=None):
        self.db                            = db
        self.cAppl                         = cAppl or 0
        self.aplicacao                     = Aplicacao(self.db, self.cAppl)
        self.applId                        = self.aplicacao.getApplId()
        self.entidades                     = Entidades(self.db)
        self.colunasEntidades              = ColunasEntidades(self.db, self.cAppl)
        self.ColunasEntidadesReferenciadas = ColunasEntidadesReferenciadas(self.db)
        self.primaryKeys                   = PrimaryKeys(self.db)
        self.foreignKeys                   = ForeignKeys(self.db)
        self.sessionId                     = sessionId or '1'
        self.parametros                    = self.db.parametros
        self.parms                         = self.db(self.parametros).select()[0]
        self.log                           = os.path.join( '\\\\'
                                                         , '127.0.0.1'
                                                         , 'c$'
                                                         , self.parms.log
                                                         , "createTable_{}.log".format(self.sessionId))

        arq                                = open(self.log, 'w')
        arq.close()
        self.submit                        = Submit(self.db, self.log, cAppl=self.cAppl, userName=self.userName)
        self.compact                       = Compact(self.db)
        self.validarPK                     = 0



    def createTables(self):
        retEntidade = entidades.selectEntidadesBycodigoAplicacao(self.cAppl)
        if  not retEntidade[0]:
            return [0,'Ocorreu um erro na chamada de selectEntidadesBycodigoAplicacao.', retEntidade[1]]
        entidades   = retEntidade[1][0]

        for entidade in entidades:



       retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidadeId)
       if  not retColunasEntidades[0]:
           if  retColunasEntidades[1]:
               return [0, retColunasEntidades[2]]
           else:
               return [0, 'Nao existem colunas para esta Entidade']
       colunasEntidade  = retColunasEntidades[1]
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
       regra             = 'IAECL'
       persistencia      = 'IUDSS'
       servico           = ('INCLUSAO', 'ALTERACAO', 'EXCLUSAO', 'CONSULTA', 'CONSULTALISTA')
       messageErro       = [0, 0, 0, 1, 1]
       path = os.path.join( '\\\\'
                          , '127.0.0.1'
                          , 'c$'
                          , self.parms.raiz
                          , self.empresa
                          , self.applId
                          , 'DEFINICOES')
       for i in xrange(5):
           if  not pgm[i]:
               continue
           retPrograma   = self.programas.selectProgramasByEntidadeRegra(entidadeId, regra[i])
           if  not retPrograma[0]:
               return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.', retPrograma[1]]
           programa      = retPrograma[1][0]
           self.bookSaiB = programa.bookSaida
           if  self.bookSaiB:
               bookSaida = 'S'
           else:
               bookSaida = ''
           nomePrograma  = os.path.join(path, (self.applId + '1' + programa.nomePrograma + regra[i]))
           properties    = nomePrograma + '.pro'
           pro           = open(properties, 'w')
           coordenador   = 'NAO'
           if  coo[i]: coordenador = self.applId + '1' + programa.nomePrograma + regra[i]
           linha         = 'COORDENADOR   ' + coordenador
           pro.write(linha + '\n')
           linha         = 'FUNCIONAL     ' + self.applId + '3' + programa.nomePrograma + regra[i]
           pro.write(linha + '\n')
           linha         = 'PERSISTENCIA  ' + self.applId + '4' + programa.nomePrograma + persistencia[i]
           pro.write(linha + '\n')
           linha         = 'ENTIDADE      ' + entidade.nomeAmigavel
           pro.write(linha + '\n')
           linha         = 'SERVICO       ' + servico[i]
           pro.write(linha + '\n')
           linha         = 'TABELA        ' + entidade.nomeExterno
           pro.write(linha + '\n')
           linha         = 'TABLENAME     ' + entidade.nomeFisico
           pro.write(linha + '\n')
           linha         = 'BOOKS         ' + 'E ' + bookSaida
           pro.write(linha + '\n')
           retMessage    = self.montaMensagem(entidadeId, 'E', 'S', regra[i])
           if  not retMessage[0]:
               return retMessage
           linha         = 'MSGSUCESSO    ' + retMessage[1]
           pro.write(linha + '\n')
           if  i == 0:
               self.validarPK = 0
               if  self.primaryKeys.primaryKeyInformada(entidadeId):
                   messageErro[0] = 1
                   self.validarPK = 1
           if  messageErro[i]:
               retMessage     = self.montaMensagem(entidadeId, 'E', 'E', regra[i])
               if  not retMessage[0]:
                   return retMessage
               linha       = 'MSGERRO       '  + retMessage[1]
               pro.write(linha + '\n')
           pro.close()
           gerados += 1

#           pdb.set_trace()

           retGerarColunas = self.gerarColunas(colunasEntidade, entidadeId, nomePrograma, regra[i])
           if  not retGerarColunas[0]:
               return [0, 'Ocorreu algum erro >>> ' + retGerarColunas[1] + ' <<< na geracao das colunas']
           self.submit.submit(properties)

       cpy = os.path.join( '\\\\'
                         , '127.0.0.1'
                         , 'c$'
                         , self.parms.raiz
                         , self.empresa
                         , self.applId
                         , 'GERADOS'
                         , 'CPY')
       pgm = os.path.join( '\\\\'
                         , '127.0.0.1'
                         , 'c$'
                         , self.parms.raiz
                         , self.empresa
                         , self.applId
                         , 'GERADOS'
                         , 'PGM')
       self.compact.compact(entidade.nomeExterno, [cpy, pgm])
       print 'Expecificacoes Geradas = ' + str(gerados)
       return [1, 'Expecificacoes Geradas = ' + str(gerados)]

   def gerarColunas(self, colunasEntidade, entidadeId, nomePrograma, regra):
       retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidadeId)
       if  not retColunasEntidades[0]:
           if  retColunasEntidades[1]:
               return [0, retColunasEntidades[2]]
           else:
               return [0, 'Nao existem colunas para esta Entidade']
       colunasEntidade = retColunasEntidades[1]

       dicPrimaryKeys = self.primaryKeys.selectPrimaryKeysByCodigoEntidade(entidadeId)
       dicForeignKeys = self.foreignKeys.selectForeignKeysByCodigoEntidade(entidadeId)

       remBookE     = open(nomePrograma + '.rme', 'w')
       bookE        = open(nomePrograma + '.bke', 'w')
       regBookE     = open(nomePrograma + '.regras', 'w')
       remBookI     = open(nomePrograma + '.rmic', 'w')
       bookI        = open(nomePrograma + '.bkic', 'w')
       lisBookI     = []
       lisRemBookI  = []
       pks          = open(nomePrograma + '.pks', 'w')
       sql          = open(nomePrograma + '.sql', 'w')
       if  self.bookSaiB:
           remBookS = open(nomePrograma + '.rms', 'w')
           bookS    = open(nomePrograma + '.bks', 'w')


       for cols in colunasEntidade:

#>>>>>>> Regras de Dominio
           retRegras = self.regrasColunas.selectRegrasColunasByColumnId(cols.colunas.id)
           if  not retRegras[0] and retRegras[1]:
               return [0,'Ocorreu um erro na chamada de selectRegrasColunasByColumnId.', retRegras[2]]
           regras = retRegras[1]

           self.rowsPrimaryKeys(cols, dicPrimaryKeys, pks)
           self.EntityColumns(cols, sql)

#>>>>>>>>> Inclusão
           if  regra == 'I':
           #>>>>>> Book de Entrada


               if  cols.colunasEntidades.inclusaoEntrada:

                 # Verifica se a coluna tem Origem
                   retOrigemColuna = self.origemColuna(cols, regBookE, lisRemBookI, lisBookI, dicPrimaryKeys, regra)
                   if  not retOrigemColuna[0]:
                       return retOrigemColuna

                 # Coluna tem Origem do FrameWork
                   if  retOrigemColuna[1] == 2 :
                       retRegraPreenchimento = self.regraPreenchimento(cols, regBookE)
                       if  not retRegraPreenchimento[0]:
                           return retRegraPreenchimento

                 # Coluna não tem Origem ou eh Primary Key Informada
                   if  not retOrigemColuna[1]                                 \
                    or self.ehPrimaryKeyInformada(cols, dicPrimaryKeys, regra):

                       self.bookEntrada(cols, remBookE, bookE)
                       self.remarksBookInterface(cols, remBookI)
                       self.bookInterface(cols, bookI)

                      #>> Regra Preenchimento
                       retRegraPreenchimento = self.regraPreenchimento(cols, regBookE)
                       if  not retRegraPreenchimento[0]:
                           return retRegraPreenchimento

                      #>> Regra Data
                       self.regraData(cols, regBookE)

                      #>> Regra Time
                       self.regraTime(cols, regBookE)

                      #>> Regra Timestamp
                       self.regraTimestamp(cols, regBookE)

                      #>> Regras de Dominio
                       retRegrasDominio = self.regrasDominio(cols, regras, regBookE)
                       if  not retRegrasDominio[0]:
                           return retRegrasDominio

                      #>> Regra Nao Existencia na própria entidade
                       regraEx = 'NX'
                       retExisteEntidade = self.existeEntidade(entidadeId, cols, dicPrimaryKeys, regraEx, regra, regBookE)
                       if  not retExisteEntidade[0]:
                           return retExisteEntidade

                      #>> Regra Existencia nas Entidades Relacionadas
                       retEntidadeRelacionada = self.entidadeRelacionada(cols, dicForeignKeys, regBookE, regra)
                       if  not retEntidadeRelacionada[0]:
                           return retEntidadeRelacionada


           #>>>>>> Book de Saida
               if  cols.colunasEntidades.inclusaoSaida:
                   self.bookSaida(cols, remBookS, bookS)

#>>>>>>>>> Alteração
           elif  regra == 'A':
           #>>>>>> Book de Entrada
               if  cols.colunasEntidades.alteracaoEntrada:

                 # Verifica se a coluna tem Origem
                   retOrigemColuna = self.origemColuna(cols, regBookE, lisRemBookI, lisBookI, dicPrimaryKeys, regra)
                   if  not retOrigemColuna[0]:
                       return retOrigemColuna

                 # Coluna tem Origem do FrameWork
                   if  retOrigemColuna[1] == 2:
                       retRegraPreenchimento = self.regraPreenchimento(cols, regBookE)
                       if  not retRegraPreenchimento[0]:
                           return retRegraPreenchimento

                 # Coluna não tem Origem ou eh Primary Key Informada
                   if  not retOrigemColuna[1]                            \
                    or self.ehPrimaryKeyInformada(cols, dicPrimaryKeys, regra):

                       self.bookEntrada(cols, remBookE, bookE)
                       self.remarksBookInterface(cols, remBookI)
                       self.bookInterface(cols, bookI)

                      #>> Regra Preenchimento
                       retRegraPreenchimento = self.regraPreenchimento(cols, regBookE)
                       if  not retRegraPreenchimento[0]:
                           return retRegraPreenchimento

                      #>> Regra Data
                       self.regraData(cols, regBookE)

                      #>> Regra Time
                       self.regraTime(cols, regBookE)

                      #>> Regra Timestamp
                       self.regraTimestamp(cols, regBookE)

                      #>> Regras de Dominio
                       retRegrasDominio = self.regrasDominio(cols, regras, regBookE)
                       if  not retRegrasDominio[0]:
                           return retRegrasDominio

                      #>> Regra Existencia na própria entidade
                       regraEx = 'EX'
                       retExisteEntidade = self.existeEntidade(entidadeId, cols, dicPrimaryKeys, regraEx, regra, regBookE)
                       if  not retExisteEntidade[0]:
                           return retExisteEntidade


                      #>> Regra Existencia nas Entidades Relacionadas
                       retEntidadeRelacionada = self.entidadeRelacionada(cols, dicForeignKeys, regBookE, regra)
                       if  not retEntidadeRelacionada[0]:
                           return retEntidadeRelacionada

           #>>>>>> Book de Saida
               if  cols.colunasEntidades.alteracaoSaida:
                   self.bookSaida(cols, remBookS, bookS)

#>>>>>>>>>>>>>> Exclusão
           elif  regra == 'E':
           #>>>>>> Book de Entrada
               if  cols.colunasEntidades.exclusaoEntrada:
                   self.bookEntrada(cols, remBookE, bookE)
                   self.remarksBookInterface(cols, remBookI)
                   self.bookInterface(cols, bookI)

               #>> Regra Preenchimento
                   retRegraPreenchimento = self.regraPreenchimento(cols, regBookE)
                   if  not retRegraPreenchimento[0]:
                       return retRegraPreenchimento

               #>> Regra Data
                   self.regraData(cols, regBookE)

               #>> Regra Time
                   self.regraTime(cols, regBookE)

               #>> Regra Timestamp
                   self.regraTimestamp(cols, regBookE)

               #>> Regras de Dominio
                   retRegrasDominio = self.regrasDominio(cols, regras, regBookE)
                   if  not retRegrasDominio[0]:
                       return retRegrasDominio

               #>> Regra Existencia na própria entidade
                   regraEx = 'EX'
                   retExisteEntidade = self.existeEntidade(entidadeId, cols, dicPrimaryKeys, regraEx, regra, regBookE)
                   if  not retExisteEntidade[0]:
                       return retExisteEntidade


           #>>>>>> Book de Saida
               if  cols.colunasEntidades.exclusaoSaida:
                   self.bookSaida(cols, remBookS, bookS)

#>>>>>>>>>>>>>> Consulta
           elif  regra == 'C':
           #>>>>>> Book de Entrada
               if  cols.colunasEntidades.consultaEntrada:
                   self.bookEntrada(cols, remBookE, bookE)
                   self.remarksBookInterface(cols, remBookI)
                   self.bookInterface(cols, bookI)

               #>> Regra Preenchimento
                   retRegraPreenchimento = self.regraPreenchimento(cols, regBookE)
                   if  not retRegraPreenchimento[0]:
                       return retRegraPreenchimento

               #>> Regra Data
                   self.regraData(cols, regBookE)

               #>> Regra Time
                   self.regraTime(cols, regBookE)

               #>> Regra Timestamp
                   self.regraTimestamp(cols, regBookE)

               #>> Regras de Dominio
                   retRegrasDominio = self.regrasDominio(cols, regras, regBookE)
                   if  not retRegrasDominio[0]:
                       return retRegrasDominio


           #>>>>>> Book de Saida
               if  cols.colunasEntidades.consultaSaida:
                   self.bookSaida(cols, remBookS, bookS)
                   self.remarksBookInterface(cols, remBookI)
                   self.bookInterface(cols, bookI)

              #>> Regra Existencia nas Entidades Relacionadas
               retEntidadeRelacionada = self.entidadeRelacionada(cols, dicForeignKeys, regBookE, regra)
               if  not retEntidadeRelacionada[0]:
                   return retEntidadeRelacionada

#>>>>>>>>>>>>>> Lista
           else:
           #>>>>>> Book de Entrada
               if  cols.colunasEntidades.listaEntrada:
                   self.bookEntrada(cols, remBookE, bookE)
                   self.remarksBookInterface(cols, remBookI)

               #>> Regra Preenchimento
                   retRegraPreenchimento = self.regraPreenchimento(cols, regBookE)
                   if  not retRegraPreenchimento[0]:
                       return retRegraPreenchimento

               #>> Regra Data
                   self.regraData(cols, regBookE)

               #>> Regra Time
                   self.regraTime(cols, regBookE)

               #>> Regra Timestamp
                   self.regraTimestamp(cols, regBookE)

               #>> Regras de Dominio
                   retRegrasDominio = self.regrasDominio(cols, regras, regBookE)
                   if  not retRegrasDominio[0]:
                       return retRegrasDominio


           #>>>>>> Book de Saida
               if  cols.colunasEntidades.listaSaida:
                   self.bookSaida(cols, remBookS, bookS)
                   self.remarksBookInterface(cols, remBookI)
                   self.bookInterface(cols, bookI)

              #>> Regra Existencia nas Entidades Relacionadas
               retEntidadeRelacionada = self.entidadeRelacionada(cols, dicForeignKeys, regBookE, regra)
               if  not retEntidadeRelacionada[0]:
                   return retEntidadeRelacionada

       retColunasEntidades = self.ColunasEntidadesReferenciadas.selectColunasEntidadesReferenciadasByCodigoEntidade(entidadeId)
       if  not retColunasEntidades[0]:
           if  retColunasEntidades[1]:
               return [0, retColunasEntidades[2]]
           else:
               return [0, 'Nao existem colunas para esta Entidade']
       colunasEntidade = retColunasEntidades[1]

       for cols in colunasEntidade:
#>>>>>>>>>>>>>> Consulta
           if  regra == 'C':
           #>>>>>> Book de Saida
               if  cols.colunasEntidadesReferenciadas.consultaSaida:
                   self.bookSaida(cols, remBookS, bookS)
                   self.remarksBookInterface(cols, remBookI)
                   self.bookInterface(cols, bookI)

                  #>> Regra Coluna Existente em Entidades relacionadas
                   retColunaEntidadeRelacionada = self.colunaEntidadeRelacionada(cols, regBookE)
                   if  not retColunaEntidadeRelacionada[0]:
                       return retColunaEntidadeRelacionada

#>>>>>>>>>>>>>> Lista
           elif  regra == 'L':
           #>>>>>> Book de Saida
               if  cols.colunasEntidadesReferenciadas.listaSaida:
                   self.bookSaida(cols, remBookS, bookS)
                   self.remarksBookInterface(cols, remBookI)
                   self.bookInterface(cols, bookI)

                  #>> Regra Coluna Existente em Entidades relacionadas
                   retColunaEntidadeRelacionada = self.colunaEntidadeRelacionada(cols, regBookE)
                   if  not retColunaEntidadeRelacionada[0]:
                       return retColunaEntidadeRelacionada


       remBookE.close()
       bookE.close()
       regBookE.close()
       self.completaInterface(lisRemBookI, remBookI, lisBookI, bookI)
       remBookI.close()
       bookI.close()
       pks.close()

       if  self.bookSaiB:
           remBookS.close()
           bookS.close()
       return [1]

   def bookEntrada(self, cols, remBookE, bookE):
       if  not cols.colunas.descricao:
           cols.colunas.descricao = ''
       linha = cols.colunas.columnName + ' = ' + cols.colunas.descricao
       remBookE.write(linha + '\n')
       linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
             + cols.datatypes.picture_cobol + ' ' \
             + str(cols.colunas.tamanhoColuna)
       if  cols.datatypes.picture_cobol == '9' and cols.colunas.decimais > 0:
           linha = linha + 'V' + str(cols.colunas.decimais)
       linha = linha + (' ' * (34 - len(linha))) + cols.datatypes.descricao
       if  cols.colunasEntidades.ehNotNull:
           ehNull = '0'
       else:
           ehNull = '1'
       linha = linha + (' ' * (49 - len(linha))) + ehNull
       bookE.write(linha + '\n')

   def remarksBookInterface(self, cols, remBookI):
       if  not cols.colunas.descricao:
           cols.colunas.descricao = ''
       linha = cols.colunas.columnName + ' = ' + cols.colunas.descricao
       remBookI.write(linha + '\n')

   def bookInterface(self, cols, bookI):
       linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
             + cols.datatypes.picture_cobol + ' ' \
             + str(cols.colunas.tamanhoColuna)
       if  cols.datatypes.picture_cobol == '9' and cols.colunas.decimais > 0:
           linha = linha + 'V' + str(cols.colunas.decimais)
       linha = linha + (' ' * (34 - len(linha))) + cols.datatypes.descricao
       if  cols.colunasEntidades.ehNotNull:
           ehNull = '0'
       else:
           ehNull = '1'
       linha = linha + (' ' * (49 - len(linha))) + ehNull
       bookI.write(linha + '\n')

   def completaInterface(self, lisRemBookI, remBookI, lisBookI, bookI):
       for linha in lisRemBookI:
           remBookI.write(linha.replace('|',',') + '\n')
       for linha in lisBookI:
           bookI.write(linha + '\n')

   def origemColuna(self, cols, regBookE, lisRemBookI, lisBookI, dicPrimaryKeys, regra):
       retOrigemColuna = self.OrigemColunasAplicacao.selectOrigemColunasAplicacaoByCodigoColuna(cols.colunas.id)
       if  not retOrigemColuna[0]:
           return [0,'Ocorreu um erro na chamada de selectorigemColunasAplicacaoByCodigoColuna.' + str(retOrigemColuna[2])]
       if  not retOrigemColuna[1]:
           return [1, 0]
       if  self.ehPrimaryKeyInformada(cols, dicPrimaryKeys, regra):
           return [1, 0]
       origemColuna = retOrigemColuna[1][0]
       linha        = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
                    + 'OR' + (' ' * 15) + origemColuna.origemColunasApoio.origem            \
                    + (' ' * (30 - len(origemColuna.origemColunasApoio.origem)))            \
                    + origemColuna.origemColunasApoio.fonte
       regBookE.write(linha + '\n')
       if  origemColuna.origemColunasApoio.fonte == 'S':
           return [1, 1]
       if  not cols.colunas.descricao:
           cols.colunas.descricao = ''
       linha = cols.colunas.columnName + ' = ' + cols.colunas.descricao
       lisRemBookI.append(linha.replace(',','|'))
       linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
             + cols.datatypes.picture_cobol + ' ' \
             + str(cols.colunas.tamanhoColuna)
       if  cols.datatypes.picture_cobol == '9' and cols.colunas.decimais > 0:
           linha = linha + 'V' + str(cols.colunas.decimais)
       linha = linha + (' ' * (34 - len(linha))) + cols.datatypes.descricao
       if  cols.colunasEntidades.ehNotNull:
           ehNull = '0'
       else:
           ehNull = '1'
       linha = linha + (' ' * (49 - len(linha))) + ehNull
       lisBookI.append(linha)
       return [1, 2]

   def regraPreenchimento(self, cols, regBookE):
       if  cols.colunasEntidades.ehNotNull:
           retMessage = self.montaMensagem(cols.colunas.id, 'C', 'E', 'PR', nova=1)
           if  not retMessage[0]:
               return retMessage
           linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
                 + 'PR' + (' ' * 5) + retMessage[1]
           regBookE.write(linha + '\n')
       return [1]

   def regraData(self, cols, regBookE):
       if  cols.datatypes.descricao == 'DATE':
           linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) + 'DT'
           regBookE.write(linha + '\n')

   def regraTime(self, cols, regBookE):
       if  cols.datatypes.descricao == 'TIME':
           linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) + 'TM'
           regBookE.write(linha + '\n')

   def regraTimestamp(self, cols, regBookE):
       if  cols.datatypes.descricao == 'TIMESTAMP':
           linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) + 'TS'
           regBookE.write(linha + '\n')

   def regrasDominio(self, cols, regras, regBookE):
       for r in regras:
           arg1   = ''
           arg2   = ''
           if  r.regrasColunas.argumento1:
               arg1   = r.regrasColunas.argumento1
           if  r.regrasColunas.argumento2:
               arg2   = r.regrasColunas.argumento2
           retMessage = self.montaMensagem(cols.colunas.id, 'C', 'E', r.regras.regra, nova=1)
           if  not retMessage[0]:
               return retMessage
           linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName)))  \
                 + r.regras.regra + (' ' * 5) + retMessage[1] + '  ' + arg1               \
                 + (' ' * (20 - len(arg1))) + arg2
           regBookE.write(linha + '\n')
       return [1]

   def ehPrimaryKeyInformada(self, cols, dicPrimaryKeys, regra):
       if  cols.colunas.id in dicPrimaryKeys:
           if  (regra == 'I' and dicPrimaryKeys[cols.colunas.id] != 3) \
           or (regra != 'I'):
               return 1
       return 0

   def existeEntidade(self, entidadeId, cols, dicPrimaryKeys, regraEx, regra, regBookE):
       if  cols.colunas.id in dicPrimaryKeys:
#           if  (regra == 'I' and dicPrimaryKeys[cols.colunas.id] != 3) \
           if  (regra == 'I' and self.validarPK) \
           or (regra != 'I'):
               retPrograma = self.programas.selectProgramasByEntidadeRegra(entidadeId, 'C')
               if  not retPrograma[0]:
                   return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.' + str(retPrograma[2])]
               pgmConsulta = retPrograma[1][0]
               if  self.soag:
                   arg1      = self.applId + '3' + pgmConsulta.nomePrograma + 'C'
                   arg3      = self.applId + 'W' + pgmConsulta.nomePrograma + 'I'
                   arg4      = self.applId + 'W00C'
               else:
                   arg1      = pgmConsulta.nomePrograma
                   arg3      = pgmConsulta.bookInterface
                   arg4      = pgmConsulta.bookControle
               arg2          = cols.colunas.columnName
               if  regraEx == 'NX':
                   retMessage  = self.montaMensagem(entidadeId, 'E', 'E', regra)
                   if  not retMessage[0]:
                       return retMessage
                   message = retMessage[1]
               else:
                   message = (' ' * 8)
               linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
                     + regraEx + (' ' * 5) + message + '  ' + arg1 + (' ' * (20 - len(arg1))) + arg2 \
                     + ' ' + arg3 + ' ' + arg4
               regBookE.write(linha + '\n')
       return [1]

   def EntityColumns(self, cols, sql):
       linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
             + cols.datatypes.picture_cobol + ' ' \
             + str(cols.colunas.tamanhoColuna)
       if  cols.datatypes.picture_cobol == '9' and cols.colunas.decimais > 0:
           linha = linha + 'V' + str(cols.colunas.decimais)
       sql.write(linha + '\n')

   def rowsPrimaryKeys(self, cols, dicPrimaryKeys, pks):
       if  cols.colunas.id in dicPrimaryKeys:
           linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
                   + str(dicPrimaryKeys[cols.colunas.id])
           pks.write(linha + '\n')

   def entidadeRelacionada(self, cols, dicForeignKeys, regBookE, regra):
       if  cols.colunas.id in dicForeignKeys:
           entidadeIdRef = dicForeignKeys[cols.colunas.id][0]
           retPrograma   = self.programas.selectProgramasByEntidadeRegra(entidadeIdRef, 'C')
           if  not retPrograma[0]:
               return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.' + str(retPrograma[2])]
           pgmConsulta   = retPrograma[1][0]
           if  pgmConsulta.codigoAplicacao == self.cAppl:
               soag = self.soag
           else:
               soag = Aplicacao(self.db, pgmConsulta.codigoAplicacao).getSoag()
           if  soag:
               arg1      = self.applId + '3' + pgmConsulta.nomePrograma + 'C'
               arg3      = self.applId + 'W' + pgmConsulta.nomePrograma + 'I'
               arg4      = self.applId + 'W00C'
           else:
               arg1      = pgmConsulta.nomePrograma
               arg3      = pgmConsulta.bookInterface
               arg4      = pgmConsulta.bookControle
           if  dicForeignKeys[cols.colunas.id][1] == cols.colunas.id:
               arg2      = cols.colunas.columnName
           else:
               retColRef = self.colunas.selectColunasByColumnId(dicForeignKeys[cols.colunas.id][1])
               if  not retColRef:
                   return [0,'Ocorreu um erro na chamada de selectColunasByColumnId.' + str(retColRef[2])]
               arg2      = retColRef[1][0].columnName
           if  regra == 'C':
               if  cols.colunasEntidades.consultaSaida:
                   arg5 = 'S'
               else:
                   arg5 = 'E'
           elif  regra == 'L':
               if  cols.colunasEntidades.listaSaida:
                   arg5 = 'S'
               else:
                   arg5 = 'E'
           else:
                 arg5 = ''
           linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
                 + 'EX' + (' ' * 15) + arg1 + (' ' * (20 - len(arg1))) + arg2            \
                 + ' ' + arg3 + ' ' + arg4 + ' ' + arg5
           regBookE.write(linha + '\n')
#>>>>>>> regra Registro Ativo
           if  self.delecaoLogica:
               retColunaDelecaoLogica = self.colunasEntidades.selectColunasEntidadesByCodigoEntidadeCodigoColuna \
                                        (entidadeIdRef, self.colDelLog)
               if  not retColunaDelecaoLogica[0]:
                   return [0,'Ocorreu um erro na chamada de selectColunasEntidadesByCodigoEntidadeCodigoColuna.' \
                            + str(retColunaDelecaoLogica[2])]
               if  retColunaDelecaoLogica[1]         \
               and dicForeignKeys[cols.colunas.id][2]:
                   retMessage = self.montaMensagem(entidadeIdRef, 'E', 'E', 'AT', nova=1)
                   if  not retMessage[0]:
                       return retMessage
                   linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName)))     \
                         + 'AT' + (' ' * 5) + retMessage[1] + '  ' + arg1 + (' ' * (20 - len(arg1))) \
                         + self.colDelLogName
                   regBookE.write(linha + '\n')
       return [1]

   def colunaEntidadeRelacionada(self, cols, regBookE):
       entidadeIdRef = cols.colunasEntidadesReferenciadas.entidadeReferenciada
       retPrograma   = self.programas.selectProgramasByEntidadeRegra(entidadeIdRef, 'C')
       if  not retPrograma[0]:
           return [0,'Ocorreu um erro na chamada de selectProgramasByEntidadeRegra.' + str(retPrograma[2])]
       pgmConsulta   = retPrograma[1][0]
       if  self.soag:
           arg1      = self.applId + '3' + pgmConsulta.nomePrograma + 'C'
       else:
           arg1      = pgmConsulta.nomePrograma
       linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
             + 'XE' + (' ' * 15) + arg1
       regBookE.write(linha + '\n')
       return [1]


   def bookSaida(self, cols, remBookS, bookS):
       if  not cols.colunas.descricao:
           cols.colunas.descricao = ''
       linha = cols.colunas.columnName + ' = ' + cols.colunas.descricao
       remBookS.write(linha + '\n')
       linha = cols.colunas.columnName + (' ' * (22 - len(cols.colunas.columnName))) \
             + cols.datatypes.picture_cobol + ' ' \
             + str(cols.colunas.tamanhoColuna)
       if  cols.datatypes.picture_cobol == '9' and cols.colunas.decimais > 0:
           linha = linha + 'V' + str(cols.colunas.decimais)
       linha = linha + (' ' * (34 - len(linha))) + cols.datatypes.descricao
       if  cols.colunasEntidades.ehNotNull:
           ehNull = '0'
       else:
           ehNull = '1'
       linha = linha + (' ' * (49 - len(linha))) + ehNull
       bookS.write(linha + '\n')

   def montaMensagem(self, codigoEntCol, origemMsg, tipoMsg, regra, nova=None):
       retMessage  = self.mensagens.getMensagem(codigoEntCol, origemMsg, tipoMsg, regra, nova)
       if  not retMessage[0]:
           return [0, 'Ocorreu um erro na chamada de getMensagem.'  + str(retMessage[2])]
       codMsg      = str(retMessage[1])
       return [1, self.applId + ('0' * (4 - len(codMsg))) + codMsg]
