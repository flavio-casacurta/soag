# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import sys
import Entidades
import Colunas
import Datatypes
import OrigemColunasAplicacao

class PrimaryKeys(object):

    def __init__(self, db, cAppl=0, model=None):
        self.db          = db
        self.cAppl       = cAppl
        self.model       = model
        self.primarykeys = self.db.primaryKeys


    def insertPrimaryKeys(self):
        lidos       = 0
        gravados    = 0

        entidades   = Entidades.Entidades(self.db, cAppl=self.cAppl)
        colunas     = Colunas.Colunas(self.db, cAppl=self.cAppl)
        orca        = OrigemColunasAplicacao.OrigemColunasAplicacao(self.db)
        lisAuto     = Datatypes.Datatypes(self.db).getDatatypesNumerics()
        lisAuto.append('TIMESTAMP')
        generate    = lambda ent: ent['Do_Not_Generate']==False
        nomeFisico  = lambda line: line['User_Formatted_Physical_Name']
        isPk        = lambda line: line['pk']==True
        isFk        = lambda line: line['fk']<>[]
        isAuto      = lambda line: line['dataType'].split('(')[0] in lisAuto
        isTimestamp = lambda line: line['dataType'].split('(')[0] == 'TIMESTAMP'

        for nomeFisicoEntidade in map(nomeFisico, filter(generate, self.model.getEntidades(''))):
            returnEntidade       = entidades.selectEntidadesByNomeFisico(nomeFisicoEntidade)
            if  not returnEntidade[0]:
                return [0,"CE - CodigoEntidade de %s nao encontrado na Tabela Entidades." % (nomeFisicoEntidade)]
            entidade             = returnEntidade[1][0]

            lisCols = self.model.getEntidadeColunas(nomeFisicoEntidade)
            pks     = filter(isPk, lisCols)
            lenPk   = len(pks)
            qtdPk   = 0
            for pk in pks:
                lidos += 1
                qtdPk += 1
                columnName         = pk['nomeFisico']
                returnCodigoColuna = colunas.selectColunasByColumnName(columnName)
                if  not returnCodigoColuna[0]:
                    return [0,"PK - CodigoColuna de %s nao encontrado na Tabela Colunas." % columnName \
                           , returnCodigoColuna[1]]
                coluna             = returnCodigoColuna[1][0]

                codigoInsercao = 1
                if  not isFk(pk) and qtdPk == lenPk and isAuto(pk):
                    codigoInsercao = 3
                    if  isTimestamp(pk):
                        orca.insertOrigemColunasAplicacao(self.cAppl, coluna.id)
                try:
                    self.primarykeys.insert(codigoAplicacao = self.cAppl
                                           ,codigoEntidade  = entidade.id
                                           ,codigoColuna    = coluna.id
                                           ,codigoInsercao  = codigoInsercao)
                    gravados = gravados +1

                except:
                   return [0,"PK - Ocorreu um erro no Insert da Tabela PrimaryKeys.", sys.exc_info()[1]]
        self.db.commit()
        return [1,('Primary Keys >>>'
               + '\n' + ' Lidos    = ' + str(lidos)
               + '\n' + ' Gravados = ' + str(gravados)
               + '\n')]

    def selectPrimaryKeysByCodigoEntidade(self, codigoEntidade):
        dicPrimaryKeys = {}
        try:
            for query in self.db(self.primarykeys.codigoEntidade == codigoEntidade).select():
                dicPrimaryKeys   [query.codigoColuna]=query.codigoInsercao
        except:
            return [0,"PK - Ocorreu um erro no Select da Tabela PrimaryKeys.", sys.exc_info()[1]]
        return dicPrimaryKeys

    def primaryKeyInformada(self, codigoEntidade):
        ret = 1
        primaryKey = self.selectPrimaryKeysByCodigoEntidade(codigoEntidade)
        for pk, pr in primaryKey.items():
            if  pr == 3:
                ret = 0
                break
        return ret
