# -*- coding:cp1252
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import sys
import utilities as utl
import DicAbrev
import LengthCols

class Colunas:

    def __init__(self, db, cAppl=0, model=None):
        self.db          = db
        self.cAppl       = cAppl
        self.model       = model
        self.colunas     = self.db.colunas
        self.parametros  = self.db.parametros
        self.parms       = self.db(self.parametros).select()[0]
        self.dicAbrev    = DicAbrev.DicAbrev(self.db)
        self.lengthCols  = LengthCols.LengthCols(self.db)
        self.datatypes   = self.db.datatypes

    def insertColunas(self):
        lidos      = 0
        gravados   = 0
        dicCols = {}
        dicPre ={'C':u'CD', 'D':u'DT', 'R':u'DS', 'E':u'EN', 'H':u'HR', 'M':u'MD',
                 'B':u'MM', 'I':u'NM', 'N':u'NU', 'P':u'PC', 'T':u'PZ', 'Q':u'QT',
                 'U':u'UN', 'V':u'VR', 'W':u'WK', 'CD':u'Código ', 'DS':u'Descrição ',
                 'DT':u'Data ', 'EN':u'Endereço ', 'HR':u'Hora ', 'ID':u'Identificador',
                 'NM':u'Nome ', 'NU':u'Número ', 'MD':u'Medida ', 'MM':u'Multimídia ',
                 'PC':u'Percentual ', 'PR':u'Prazo ', 'QT':u'Quantidade ', 'VR':u'Valor ',
                 'UN':u'Unidade ', 'WK':''}

        dicabrev = self.dicAbrev.getDicAbrev()

        for lisCols in self.model.getColunas(''):
            lidos += 1
            columnname         = lisCols['Physical_Name'].upper()
            attributename      = lisCols['Name']
            descricao          = lisCols['Definition']
            if  not descricao:
                descricao      = lisCols['Comment']
            Physical_Data_Type = lisCols['Physical_Data_Type']
            dicCols[columnname] = {'Physical_Data_Type':Physical_Data_Type
                                  ,'attributename':attributename
                                  ,'descricao':descricao}

        for k in dicCols:

#  Trata Physical_Data_Type

            dicCols[k]['Physical_Data_Type'] = self.lengthCols.db2DatatypeLength(dicCols[k]['Physical_Data_Type'])

#  Trata atributo
            attr = dicCols[k]['attributename']
            if not attr:
                attr=dicPre[k[:1]] if k[:1] in dicPre else 'WK'
                attt=k[1:].replace('_',' ')
                for word in utl.words(attt)[1]:
                    if word in dicabrev:
                        attr=attr+dicabrev[word][0].capitalize()
                    else:
                        attr=attr+word.capitalize()
            nAttr=dicPre[attr[0:2].upper()]
            strt = 2
            for chr in xrange(3,len(attr)):
                if  attr[chr].isupper():
                    nAttr = nAttr + attr[strt:chr] + ' '
                    strt  = chr
            nAttr = nAttr + attr[strt:chr+1]
            dicCols[k]['attributename'] = nAttr

#  Trata label
            wrd = 0
            if  len(nAttr.split()) > 0:
                wrd = 1
            dicCols[k]['label'] = ' '.join(nAttr.split()[wrd:])

#  Trata descrição
            if  dicCols[k]['descricao']:
                try:
                    dicCols[k]['descricao'] = ' '.join(dicCols[k]['descricao'].split())
                except UnicodeEncodeError:
                    desc = dicCols[k]['descricao'].encode('cp1252')
                    for l in desc:
                        if  ord(l) > 255:
                            desc = desc.replace(l, ' ')
                    dicCols[k]['descricao'] = ' '.join(desc.split())
            else:
                dicCols[k]['descricao'] = dicCols[k]['attributename']

        for k in sorted(dicCols.keys()):
            try:
                self.colunas.insert(codigoAplicacao = (int(self.cAppl))
                                   ,columnName      = k
                                   ,codigoDatatype  = dicCols[k]['Physical_Data_Type'][0]
                                   ,tamanhoColuna   = dicCols[k]['Physical_Data_Type'][1]
                                   ,decimais        = dicCols[k]['Physical_Data_Type'][2]
                                   ,attributeName   = dicCols[k]['attributename']
                                   ,label           = dicCols[k]['label']
                                   ,descricao       = dicCols[k]['descricao']
                                   )
                gravados += 1
            except:
                return [0,"Ocorreu um erro no Insert da Tabela Colunas.", sys.exc_info()[1]]
        self.db.commit()
        return [1, ('Colunas >>>'
               + '\n' + ' Lidos    = ' + str(lidos)
               + '\n' + ' Gravados = ' + str(gravados)
               + '\n')]

    def selectColunasByColumnName(self, columnName):
        try:
            query=self.db((self.colunas.codigoAplicacao == int(self.cAppl))
                        & (self.colunas.columnName == columnName)).select()
        except:
            return [0,'Ocorreu um erro no Select da Tabela Colunas.', sys.exc_info()[1]]
        if not query:
            return [0,'(selectColunasByColumnName) Não foi encontrada a Coluna %s.' % columnName]
        return [1, query]

    def selectColunasResolvidasByColumnName(self, columnName):
        try:
            query=self.db((self.colunas.codigoAplicacao == int(self.cAppl))
                        & (self.colunas.columnName == columnName)
                        & (self.datatypes.id == self.colunas.codigoDatatype)).select()
        except:
            return [0,'Ocorreu um erro no Select da Tabela Colunas.', sys.exc_info()[1]]
        if not query:
            return [0,'(selectColunasByColumnName) Não foi encontrada a Coluna %s.' % columnName]
        return [1, query]

    def selectColunasByColumnId(self, columnId):
        try:
            query=self.db(self.colunas.id == int(columnId)).select()
        except:
            return [0,'Ocorreu um erro no Select da Tabela Colunas.', sys.exc_info()[1]]
        if not query:
            return [0,'(selectColunasByColumnId) Não foi encontrada a Coluna %s.' % columnId]
        return [1, query]

    def selectColunasByCodigoAplicacao(self):
        try:
            query=self.db((self.colunas.codigoAplicacao == int(self.cAppl))).select(orderby=self.colunas.id)
        except:
            return [0,'Ocorreu um erro no Select da Tabela Colunas.', sys.exc_info()[1]]
        if not query:
            return [0,'(selectColunasByCodigoAplicacao) Não foi encontrada nenhuma Coluna para a Aplicação %s.'
                    % self.cAppl]
        return [1, query]

