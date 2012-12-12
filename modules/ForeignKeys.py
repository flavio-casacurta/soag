# -*- coding:utf-8
'''
   Created on 12/09/2011
   @author: C&C - HardSoft
'''
import sys
import Entidades
import Colunas

class ForeignKeys(object):

    def __init__(self, db, cAppl=0, model=None):
        self.db          = db
        self.cAppl       = cAppl
        self.model       = model
        self.foreignkeys = self.db.foreignKeys

    def insertForeignKeys(self):
        lidos       = 0
        gravados    = 0
        entidades   = Entidades.Entidades(self.db, cAppl=self.cAppl)
        colunas     = Colunas.Colunas(self.db, cAppl=self.cAppl)
        generate    = lambda ent: ent['Do_Not_Generate']==False
        nomeFisico  = lambda line: line['User_Formatted_Physical_Name']
        isFk        = lambda line: line['fk']<>[]

        nomeFisicoEntidades = map(nomeFisico, filter(generate, self.model.getEntidades('')))
        for nomeFisicoEntidade in nomeFisicoEntidades:            
            returnEntidade       = entidades.selectEntidadesByNomeFisico(nomeFisicoEntidade)
            if  not returnEntidade[0]:
                return [0,"CE - CodigoEntidade de %s nao encontrado na Tabela Entidades." % (nomeFisicoEntidade)]
            codigoEntidade       = returnEntidade[1][0].id

            lisCols = self.model.getEntidadeColunas(nomeFisicoEntidade)
            fks     = filter(isFk, lisCols)

            for fk in fks:
                lidos                = lidos + 1
                colunaForeignKey     = fk['nomeFisico']
                colunaReferenciada   = fk['fk'][0][0]
                nomeFisicoEntRef     = fk['fk'][0][1]
                if  not nomeFisicoEntRef in nomeFisicoEntidades:
                    continue
                else:
                    returnEntidadeReferenciada = entidades.selectEntidadesByNomeFisico(nomeFisicoEntRef)
                    if not returnEntidadeReferenciada[0]:
                        return [0,"CodigoEntidade de " + nomeFisico + " nao encontrado na Tabela Entidades." \
                                 , returnEntidadeReferenciada[1]]
                    codigoEntidadeReferenciada = returnEntidadeReferenciada[1][0].id

                    returnColuna   = colunas.selectColunasByColumnName(colunaForeignKey)
                    if not returnColuna[0]:
                        return [0,"FK1 - CodigoColuna de " + colunaForeignKey + "  nao encontrado na Tabela Colunas." \
                               , returnColuna[1]]
                    codigoColuna   = returnColuna[1][0].id

                    if colunaForeignKey == colunaReferenciada:
                        codigoColunaReferenciada = codigoColuna
                    else:
                        returnColunaReferenciada = colunas.selectColunasByColumnName(colunaReferenciada)
                        if not returnColunaReferenciada[0]:
                            return [0,"FK2 - CodigoColuna de " + colunaReferenciada + "  nao encontrado na Tabela Colunas." \
                                   , returnColunaReferenciada[1]]
                        codigoColunaReferenciada  = returnColunaReferenciada[1][0].id

                    try:
                        self.foreignkeys.insert(codigoEntidade             = codigoEntidade
                                               ,codigoColuna               = codigoColuna
                                               ,codigoEntidadeReferenciada = codigoEntidadeReferenciada
                                               ,codigoColunaReferenciada   = codigoColunaReferenciada
                                               ,ativo                      = True)
                        gravados = gravados +1
                    except:
                        return [0,"Ocorreu um erro no Insert da Tabela ForeignKeys.", sys.exc_info()[1]]
        self.db.commit()
        return [1,('Foreign Keys >>>'
               + '\n' + ' Lidos    = ' + str(lidos)
               + '\n' + ' Gravados = ' + str(gravados)
               + '\n')]

    def selectForeignKeysByCodigoEntidade(self, codigoEntidade):
        dicForeignKeys = {}
        try:
            for query in self.db(self.foreignkeys.codigoEntidade == codigoEntidade).select():
                dicForeignKeys [query.codigoColuna]=[ query.codigoEntidadeReferenciada
                                                    , query.codigoColunaReferenciada
                                                    , query.ativo                      ]
        except:
            return [0,"FK - Ocorreu um erro no Select da Tabela ForeignKeys.", sys.exc_info()[1]]
        return dicForeignKeys
