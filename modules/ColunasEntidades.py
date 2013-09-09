# -*- coding:utf-8
'''
   Created on 12/09/2011
   @author: C&C - HardSoft
'''
import sys
import Entidades
import Colunas
import PrimaryKeys
import OrigemColunasAplicacao
import Regras
import CheckList

class ColunasEntidades:

    def __init__(self, db, cAppl=0, model=None):
        self.db                     = db
        self.cAppl                  = cAppl
        self.model                  = model
        self.entidades              = Entidades.Entidades(self.db, cAppl=self.cAppl)
        self.coluna                 = Colunas.Colunas(self.db, cAppl=self.cAppl)
        self.primaryKeys            = PrimaryKeys.PrimaryKeys(self.db)
        self.OrigemColunasAplicacao = OrigemColunasAplicacao.OrigemColunasAplicacao(self.db)
        self.regra                  = Regras.Regras(self.db).getRegras(1)
        self.checkList              = CheckList.CheckList(self.db, cAppl=self.cAppl)
        self.colunasEntidades       = self.db.colunasEntidades
        self.datatypes              = self.db.datatypes
        self.colunas                = self.db.colunas

    def insertColunasEntidades(self):
        lidos               = 0
        gravados            = 0
        nomeFisicoEntidadeA = ''
        generate            = lambda ent: ent['Do_Not_Generate']==False
        nomeFisico          = lambda line: line['User_Formatted_Physical_Name']

        for nomeFisicoEntidade in map(nomeFisico, filter(generate, self.model.getEntidades(''))):
            if  nomeFisicoEntidadeA != nomeFisicoEntidade:
                returnEntidade       = self.entidades.selectEntidadesByNomeFisico(nomeFisicoEntidade)
                if  not returnEntidade[0]:
                    print "CE - CodigoEntidade de %s nao encontrado na Tabela Entidades." % (nomeFisicoEntidade)
                    continue
                entidade             = returnEntidade[1][0]
                nomeFisicoEntidadeA  = nomeFisicoEntidade
                entCols              = self.model.getEntidadeColunas(nomeFisicoEntidade)
                for lisCols in entCols:
                    lidos     += 1
                    columnName = lisCols['nomeFisico']
                    ehNotNull  = False if lisCols['null'] else True
                    returnCodigoColuna = self.coluna.selectColunasByColumnName(columnName)
                    if  not returnCodigoColuna[0]:
                        print "CE - CodigoColuna de %s nao encontrado na Tabela Colunas." % (columnName)
                        continue
                    coluna     = returnCodigoColuna[1][0]
                    try:
                        self.colunasEntidades.insert(codigoAplicacao = self.cAppl
                                                    ,codigoEntidade  = entidade.id
                                                    ,codigoColuna    = coluna.id
                                                    ,ehNotNull       = ehNotNull)
                        gravados += 1
                    except:
                        return [0,"CE - Ocorreu um erro no Insert da Tabela colunasEntidades.", sys.exc_info()[1]]
        self.db.commit()
        return [1,('Colunas das Entidades >>>'
               + '\n' + ' Lidos    = ' + str(lidos)
               + '\n' + ' Gravados = ' + str(gravados)
               + '\n')]

    def updateColunasEntidadesBycAppl(self):
        altEntidades = 0
        altColunas   = 0
        returnEntidades = Entidades.Entidades(self.db, cAppl=self.cAppl).selectEntidadesBycodigoAplicacao()
        if  not returnEntidades[0]:
            return [0, "CE - Não existem Entidades para esta Aplicação."]
        entidades = returnEntidades[1]
        for entidade in entidades:
            processaEntidade =  self.processaEntidade(entidade)
            if  not processaEntidade[0]:
                return [0,"CE - Ocorreu um erro no processamento da Entidade.", processaEntidade[1]]
            altEntidades += 1
            altColunas   = altColunas + processaEntidade[1]

        ckListCE = self.checkList.updateCheckListColunasEntidades()
        if  not ckListCE[0]:
            return ckListCE

        self.db.commit()
        return [1, ('Colunas das Entidades Atualizadas>>>'
               + '\n' + ' Entidades = ' + str(altEntidades)
               + '\n' + ' Colunas   = ' + str(altColunas)
               + '\n')]

    def updateColunasEntidadesByCodigoEntidade(self, codigoEntidade):
        altEntidades = 0
        altColunas   = 0
        returnEntidades = Entidades.Entidades(self.db).selectEntidadesByEntidadeId(codigoEntidade)
        if  not returnEntidades[0]:
            return [0, "CE - Não existem Entidades para esta Aplicação."]
        entidade     = returnEntidades[1][0]
        procEntidade = self.processaEntidade(entidade)
        if  not procEntidade[0]:
            return [0,"CE - Ocorreu um erro no processamento da Entidade.", procEntidade[1]]
        altEntidades += 1
        altColunas   = altColunas + procEntidade[1]
        self.db.commit()
        return [1, ('updateColunasEntidades >>>'
               + '\n' + 'Entidades = ' + str(altEntidades)
               + '\n' + 'Colunas   = ' + str(altColunas)
               + '\n')]

    def selectColunasEntidadesByCodigoEntidade(self, codigoEntidade):
        try:
            query = self.db(self.colunasEntidades.codigoEntidade == codigoEntidade)   \
                        .select(self.colunasEntidades.ALL,orderby=self.colunasEntidades.id)
        except:
            return [0, 'CE - Ocorreu um erro no Select da Tabela ColunasEntidades.', sys.exc_info()[1]]
        return [1, query]

    def selectColunasEntidadesByCodigoEntidadeCodigoColuna(self, codigoEntidade, codigoColuna):
        try:
            query = self.db((self.colunasEntidades.codigoEntidade == codigoEntidade)
                          & (self.colunasEntidades.codigoColuna   == codigoColuna)).select()
        except:
            return [0, 'CE - Ocorreu um erro no Select da Tabela ColunasEntidades.', sys.exc_info()[1]]
        return [1, query]

    def selectColunasEntidadesResolvidasByCodigoEntidade(self, codigoEntidade):
        try:
            query = self.db((self.colunasEntidades.codigoEntidade == codigoEntidade)
                          & (self.colunas.id   == self.colunasEntidades.codigoColuna)
                          & (self.datatypes.id == self.colunas.codigoDatatype))\
                            .select(orderby=self.colunasEntidades.id)

        except:
            return [0, 'CE - Ocorreu um erro no Select da Tabela ColunasEntidades.', sys.exc_info()[1]]
        return [1, query]

    def updateColunasEntidades(self, colunaEntidade):
        try:
            self.db(self.colunasEntidades.id             == colunaEntidade.id)   \
                                .update( inclusaoEntrada  = colunaEntidade.inclusaoEntrada
                                       , inclusaoSaida    = colunaEntidade.inclusaoSaida
                                       , alteracaoEntrada = colunaEntidade.alteracaoEntrada
                                       , alteracaoSaida   = colunaEntidade.alteracaoSaida
                                       , exclusaoEntrada  = colunaEntidade.exclusaoEntrada
                                       , exclusaoSaida    = colunaEntidade.exclusaoSaida
                                       , consultaEntrada  = colunaEntidade.consultaEntrada
                                       , consultaSaida    = colunaEntidade.consultaSaida
                                       , listaEntrada     = colunaEntidade.listaEntrada
                                       , listaSaida       = colunaEntidade.listaSaida)
        except:
            return [0, 'CE - Ocorreu um erro no Update da Tabela colunasEntidades.', sys.exc_info()[1]]
        return [1, 1]

    def processaEntidade(self, entidade):
        updtColEnt           = 0
        retColunasEntidades  = self.selectColunasEntidadesByCodigoEntidade(entidade.id)
        if  not retColunasEntidades[0]:
            return [0, retColunasEntidades[2]]
        colunasEntidades     = retColunasEntidades[1]
#        retPrimaryKeys       = None
        retPrimaryKeys       = self.primaryKeys.selectPrimaryKeysByCodigoEntidade(entidade.id)
        if not retPrimaryKeys:
            return [0, retPrimaryKeys[1]]
        primaryKeys          = retPrimaryKeys
        for colunaEntidade in colunasEntidades:
            retOrigemColuna = self.origemColuna(colunaEntidade.codigoColuna)
            if  not retOrigemColuna[0]:
                return retOrigemColuna
#>>>   seta book inclusao
            if  entidade.pgmInclusao:
                if  (colunaEntidade.codigoColuna in primaryKeys
                 and primaryKeys[colunaEntidade.codigoColuna] == 3):
                    colunaEntidade.inclusaoEntrada     = False
                    colunaEntidade.inclusaoSaida       = True
                elif retOrigemColuna[1]:
                    if  retOrigemColuna[1] == self.regra['I'][0]:
                        colunaEntidade.inclusaoEntrada  = True
                        colunaEntidade.inclusaoSaida    = False
                    else:
                        colunaEntidade.inclusaoEntrada  = False
                        colunaEntidade.inclusaoSaida    = False
                else:
                    colunaEntidade.inclusaoEntrada      = True
                    colunaEntidade.inclusaoSaida        = False
            else:
                colunaEntidade.inclusaoEntrada          = False
                colunaEntidade.inclusaoSaida            = False
#>>>   seta book alteracao
            colunaEntidade.alteracaoSaida               = False
            if  entidade.pgmAlteracao:
                if  colunaEntidade.codigoColuna in primaryKeys:
                    colunaEntidade.alteracaoEntrada     = True
                elif retOrigemColuna[1]:
                    if  retOrigemColuna[1] == self.regra['A'][0]:
                        colunaEntidade.alteracaoEntrada = True
                    else:
                        colunaEntidade.alteracaoEntrada = False
                else:
                    colunaEntidade.alteracaoEntrada     = True
            else:
                colunaEntidade.alteracaoEntrada         = False
#>>>   seta book exclusao
            if  entidade.pgmExclusao:
                colunaEntidade.exclusaoSaida            = False
                if  colunaEntidade.codigoColuna in primaryKeys:
                    colunaEntidade.exclusaoEntrada      = True
                else:
                    colunaEntidade.exclusaoEntrada      = False
            else:
                colunaEntidade.exclusaoEntrada          = False
                colunaEntidade.exclusaoSaida            = False
#>>>   seta book consulta
            if  entidade.pgmConsulta:
                if  colunaEntidade.codigoColuna in primaryKeys:
                    colunaEntidade.consultaEntrada      = True
                    colunaEntidade.consultaSaida        = False
                else:
                    colunaEntidade.consultaEntrada      = False
                    colunaEntidade.consultaSaida        = True
            else:
                colunaEntidade.consultaEntrada          = False
                colunaEntidade.consultaSaida            = False
#>>>   seta book lista
            if  entidade.pgmLista:
                colunaEntidade.listaSaida               = True
                if  colunaEntidade.codigoColuna in primaryKeys:
                    colunaEntidade.listaEntrada         = True
                else:
                    colunaEntidade.listaEntrada         = False
            else:
                colunaEntidade.listaltaEntrada          = False
                colunaEntidade.listaltaSaida            = False
            updateColunaEntidade                        = self.updateColunasEntidades(colunaEntidade)
            if  updateColunaEntidade[0]:
                updtColEnt                             += 1
            else:
                return [0, updateColunaEntidade[2]]
        return [1, updtColEnt]

    def origemColuna(self, codigoColuna):
        retOrigemColuna = self.OrigemColunasAplicacao.selectOrigemColunasAplicacaoByCodigoColuna(codigoColuna)
        if  not retOrigemColuna[0]:
            return [0,'Ocorreu um erro na chamada de selectOrigemColunasAplicacaoByCodigoColuna.' + str(retOrigemColuna[2])]
        if  not retOrigemColuna[1]:
            return [1, 0]
        origemColuna = retOrigemColuna[1][0]
        return [1, origemColuna.origemColunasAplicacao.codigoRegra]
