# -*- coding:utf-8
'''
   Created on 07/05/2013
   @author: C&C - HardSoft
'''
from datetime import date
from Gerutl import *

class GerBook:

    def __init__(self, db):
        self.parms = db(db.parametros.id==1).select()[0]
        self.tmplt = os.path.join( '\\\\'
                                 , '127.0.0.1'
                                 , 'c$'
                                 , self.parms.web2py
                                 , 'applications'
                                 , self.parms.soag
                                 , 'Template'
                                 , 'cpy') + os.sep

    def gerBook(self, properties, prms):
        lisBookE = prms[0]
        lisBookI = prms[1]
        lisBookC = lisBookI
        lisBookS = prms[2]
        lisBookR = prms[3]
        lisCol   = prms[4]
        dicCol   = prms[5]
        dicRegras= prms[6]
        pks      = prms[7]

        contratante = properties['CONTRATANTE']
        sp = '  ' if len(contratante) < 21 else ' ' if len(contratante) < 32 else ''

        dicBook = {'@ANALISTA'   :properties['ANALISTA']
                  ,'@APPLID'     :properties['APPLID']
                  ,'@APPLNAME'   :properties['APPLNAME']
                  ,'@CONTRATANTE':'{:^64}'.format(sp.join([x for x in contratante[:62]]))
                  ,'@AUTHOR'     :'{}/{}'.format(properties['USERNAME'], properties['EMPRESA'])
                  ,'@DATE'       :date.today().strftime('%d %b %Y').upper()
                  ,'@ENTIDADE1'  :properties['ENTIDADE'][:30]
                  ,'@ENTIDADE2'  :properties['ENTIDADE'][30:60]
                  ,'@GRUPO'      :properties['GRUPO']
                  ,'@SERVICO'    :properties['SERVICO']}

        path = os.path.join( '\\\\'
                           , '127.0.0.1'
                           , 'c$'
                           , self.parms.raiz
                           , properties['EMPRESA'].replace(' ', '_')
                           , properties['APPLID']
                           , 'GERADOS'
                           , 'CPY') + os.sep

        if  properties['COORDENADOR']:
            sufBooks = ['E', 'S'] if lisBookS else ['E']
        else:
            sufBooks = []
        sufBooks+=['I', 'C']
        qocc = 0

        for sufBook in sufBooks:
            nameBook ='{}W{}{}'.format(properties['APPLID']
                                      ,properties['SIGLAPGM']
                                      ,sufBook)
            template = open(os.path.join(self.tmplt,'WXX{}N.CPY'.format(sufBook))).read()
            navega = ''
            occurs = False
            lenEntrada = 0
            remBook, book, level, esif = entradaBook(sufBook)
            for n, coluna in enumerate(eval('lisBook' + sufBook)):
                col=dicCol[coluna]
                remBook += remarksBook(col)
                if  n == 1 and properties['TYPEPGM'] == 'L' and sufBook == 'S':
                    remBook, book, level, esif, occurs = inclOccurs(properties, remBook, book,
                                                                    level, esif, sufBook)

                book += fieldDescription(level, col, esif)
                if  sufBook == 'I' and coluna in dicRegras:
                    for k in dicRegras[coluna].keys():
                        if k in ('VL', 'RG'):
                           book += level88(dicRegras[coluna][k]['regra'], level, col, esif)

            if  (sufBook == 'S' and lisBookS and properties['TYPEPGM'] in ('C', 'L')):
                for coluna in lisBookR:
                    col=dicCol[coluna]
                    remBook += remarksBook(col)
                    book += fieldDescription(level, col, esif)

            if  sufBook in 'I C' and lisBookS:
                lenEntrada = lreclCopy(book)['lrecl']
                remBook, book, level, esif = saidaBook(remBook, book)
                for n, coluna in enumerate(lisBookS):
                    col=dicCol[coluna]
                    remBook += remarksBook(col)
                    if  n == 1 and properties['TYPEPGM'] == 'L':
                        remBook, book, level, esif, occurs = inclOccurs(properties, remBook, book,
                                                                        level, esif , sufBook)
                    book += fieldDescription(level, col, esif)

            if  occurs:
                qocc = calcOccurs(book, lenEntrada) if qocc == 0 else qocc
                occurs = '@PREFIX-OCCURS{:14}OCCURS 0 TO {}\n'.format('',qocc)
                occurs += '{:31}DEPENDING ON @PREFIX-NREG-QTDE.'.format('')
                dic = {'@PREFIX-OCCURS.':occurs}
                book= change(dic, book)

            if  sufBook in 'I C' and properties['TYPEPGM'] == 'L':
                navega = self._navega(dicCol, pks)

            dic = {'@FIELDS\n' :book
                  ,'@REMARKS\n':remBook
                  ,'@NAVEGA\n' :navega}

            book = change(dic, template)

            dicBook['@PREFIX']=nameBook
            dicBook['@LENGTH']=str(lreclCopy(book)['lrecl'])
            book = insAster72(change(dicBook,book))
            bookName = os.path.join(path, '{}.cpy'.format(nameBook))
            bookWrite = open(bookName, 'w')
            bookWrite.write(book)
            bookWrite.close()

    def _navega(self, dicCol, pks):
        template = open(os.path.join(self.tmplt,'WXXPN.CPY')).read()
        level = 11
        esif = 'I'
        keyI = ''
        for coluna in pks:
            col=dicCol[coluna[0]]
            keyI += fieldDescription(level, col, esif)
        esif = 'F'
        keyF = ''
        for coluna in pks:
            col=dicCol[coluna[0]]
            keyF += fieldDescription(level, col, esif)
        dic = {'@CHAVEINICIAL\n':keyI
              ,'@CHAVEFINAL\n':keyF}
        return change(dic, template)
