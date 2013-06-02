# -*- coding:utf-8
'''
   Created on 27/04/2013
   @author: C&C - HardSoft
'''
from utilities import *

dicInv = {'EQ':'NOT EQUAL TO'
         ,'NE':'EQUAL TO'
         ,'LT':'NOT LESS THAN'
         ,'LE':'GREATER THAN'
         ,'GT':'NOT GREATER THAN'
         ,'GE':'LESS THAN'}

dicVal = {'X'        :'SPACES'
         ,'9'        :'ZEROS'
         ,'CHAR'     : "' '"
         ,'DATE'     : "'00.00.00'"
         ,'DECIMAL'  : '0'
         ,'INTEGER'  : '0'
         ,'TIME'     : "'00:00:00'"
         ,'TIMESTAMP': "'0001-01-01-01.01.01.000001'"
         ,'VARCHAR'  : "' '"}

dicCv  = {'X1':' EQUAL TO LOW-VALUES'
         ,'X2':' EQUAL TO HIGH-VALUES'
         ,'91':' IS NOT NUMERIC'}

dicOc  = {1:'>='
         ,2:'>'
         ,3:'<'
         ,4:'<='}

dicAd  = {1:'ASC'
         ,2:'ASC'
         ,3:'DESC'
         ,4:'DESC'}

class Label(object):
    def __init__(self, label):
        self.label = label

    def Label(self):
        self.label += 10
        return str(self.label)

class ErrLocal(object):
    def __init__(self, errLocal):
        self.errLocal = errLocal

    def ErrLocal(self):
        self.errLocal += 1
        return '{:04}'.format(self.errLocal)

class Cale(object):
    def __init__(self, cale):
        self.cale = cale

    def TrueCale(self):
        self.cale = True
        return self.cale

def remarksBook(col):
    remBook = ''
    linha = '{: >7} {:19}= '.format('*', col.colunas.columnName.replace('_','-'))
    if  col.colunas.descricao:
        descr = remover_acentos(col.colunas.descricao).upper()
    else:
        descr = remover_acentos(col.colunas.attributeName).upper()
    while len(descr):
        n = -1
        if  len(descr) > 41:
            idescr = iterInv(descr[:41])
            for n, i in enumerate(idescr):
                if  i == ' ':
                    break
            if  n + 1 == 41:
                n = -1
        linha += descr[:41-(n+1)] + '\n'
        remBook += linha
        linha = '{: >7} {:21}'.format('*', ' ')
        descr = descr[41-n:]
    return remBook

def remBookExtra(remarks):
    remBook = '{: >7} {}\n'.format('*', remarks)
    remBook += '{: >7}\n'.format('*')
    return remBook

def itemGroup(level, itemGroup, esif=''):
    esif = esif + '-' if esif else ''
    posLevel = ((level - 7) / 2) + 14
    lvl = '{: >{}}'.format('{:02}'.format(level), posLevel)
    return '{:19}@PREFIX-{}{}.\n'.format(lvl, esif, itemGroup)

def fieldDescription(level, col, esif=''):
    esif = esif + '-' if esif else ''
    posLevel = ((level - 7) / 2) + 14
    picture = col.datatypes.picture_cobol
    lenCol = col.colunas.tamanhoColuna
    lenDec = col.colunas.decimais
    decimais = ''
    if  picture == 9 and lenDec > 0:
        lenCol -= lenDec
        decimais = 'V9({:02})'.format(lenDec)
    lvl = '{: >{}}'.format('{:02}'.format(level), posLevel)
    lvlFld = '{:19}@PREFIX-{}{}'.format(lvl, esif, col.colunas.columnName.replace('_','-'))
    return '{:48}{}.\n'.format(lvlFld, 'PIC  {}({:05}){}'.format(picture, lenCol, decimais))

def level88(regra, level, col, esif=''):
    if  regra.regras.regra not in ['VL', 'RG']:
        return ''
    esif = esif + '-' if esif else ''
    thru = ' THRU ' if regra.regras.regra == 'RG' else ''
    arg1 = regra.regrasColunas.argumento1
    if  regra.regras.regra == 'VL':
        q = "'" if col.datatypes.picture_cobol == 'X' else ''
        arg1 = ', '.join([q + w + q for w in words(arg1)[1]])
    arg2 = regra.regrasColunas.argumento2
    posLevel = ((level - 7) / 2) + 16
    lvl = '{: >{}}'.format(88, posLevel)
    lvlFld = '{:19}{}'.format(lvl, '@PREFIX-{}{}-VALIDO'.format(esif, col.colunas.columnName.replace('_','-'))[:29])
    value = 'VALUE {}{}{}.'.format(arg1, thru, arg2)
    return '{:48}{}.\n'.format(lvlFld, 'VALUE {}{}{}'.format(arg1, thru, arg2))

def entradaBook(sufBook):
    remBook = remBookExtra('BLOCO-ENTRADA') if sufBook in 'I C' else ''
    book = itemGroup(7, 'BLOCO-ENTRADA') if sufBook in 'I C' else ''
    level = 9 if sufBook in 'I C' else 7
    esif = 'E' if sufBook in 'I C' else ''
    return (remBook, book, level, esif)

def saidaBook(remBook, book):
    level = 7
    remBook += remBookExtra('BLOCO-SAIDA')
    book += itemGroup(level, 'BLOCO-SAIDA')
    level += 2
    esif = 'S'
    return (remBook, book, level, esif)

def inclOccurs(properties, remBook, book, level, esif, sufBook):
    occurs = False
    if  sufBook in 'I C S':
        book += itemGroup(level, '{}'.format(properties['ENTIDADE'][:18].replace('_','-')), esif)
        level +=2
        book += itemGroup(level, 'OCCURS')
        level +=2
        occurs = True
    return (remBook, book, level, esif, occurs)

def calcOccurs(book, lenEntrada):
    lenBook = lreclCopy(book)['lrecl'] - (lenEntrada + 2)
    occ = 16000 / lenBook
    return occ if occ < 51 else 50

def montaMove(fieldI, fieldO, bookI, bookO, esifI, esifO, spi, pt, idxI='', idxO=''):
    esifI = esifI + '-' if esifI else ''
    esifO = esifO + '-' if esifO else ''
    bookI = bookI + '-' if bookI else ''
    ret = '{:{}}MOVE {}{}{}{}\n'.format('', spi, bookI, esifI, fieldI.replace('_','-'), idxI)
    ret += '{:{}}TO {}-{}{}{}{}\n'.format('', spi+2, bookO, esifO, fieldO.replace('_','-'), idxO, pt)
    return ret

def moveDclToBook(field, qlf, bookO, esifO, spi, pt, idxO=''):
    esifO = esifO + '-' if esifO else ''
    ret = '{:{}}MOVE{:12}{:24}{}\n'.format('', spi, '', field.replace('_','-'), qlf)
    ret += '{:{}}TO {}-{}{}{}{}\n'.format('', spi+2, bookO, esifO, field.replace('_','-'), idxO, pt)
    return ret

def moveBookToDcl(fieldI, fieldO, qlf, bookI, esifI, spi, pt):
    esifI = esifI + '-' if esifI else ''
    bookI = bookI + '-' if bookI else ''
    ret = '{:{}}MOVE {}{}{}\n'.format('', spi, bookI, esifI, fieldI.replace('_','-'))
    ret += '{:{}}TO{:12}{:24}{}{}\n'.format('', spi+2, '', fieldO.replace('_','-'), qlf, pt)
    return ret

def calculaLenVarchar(field, qlf):
    ret  = '{:11}PERFORM VARYING {}-LEN  {}\n'.format('', field.replace('_','-'), qlf)
    ret += '{:14}FROM LENGTH OF {}-TEXT {}\n'.format('', field.replace('_','-'), qlf)
    ret += '{:16}BY -1\n'.format('')
    ret += '{:13}UNTIL {}-TEXT {}\n'.format('', field.replace('_','-'), qlf)
    ret += '{:18}({}-LEN  {}:1)\n'.format('', field.replace('_','-'), qlf)
    ret += '{:15}NOT EQUAL TO SPACE\n'.format('')
    ret += '{:16}OR {}-LEN  {} EQUAL TO 1\n'.format('', field.replace('_','-'), qlf)
    ret += '{:11}END-PERFORM.\n'.format('')
    return ret

def calcLenblpag(lisBook, dicCol):
    ret = 0
    for c in lisBook:
        col = dicCol[c]
        ret += col.colunas.tamanhoColuna
    return ret

def calcOptimize(lisBookS, dicCol):
    lenBook = calcLenblpag(lisBookS, dicCol) - 2
    occ = 16000 / lenBook
    return occ if occ < 51 else 50

def montaWorkingFuncionais(modulo, controle, interface):
    ret = '{:7}01  WRK-{}.\n'.format('', modulo)
    ret += '{:11}COPY {}.\n'.format('', controle)
    ret += '{:11}COPY {}.\n'.format('', interface)
    ret += '{:<7}{:->64}\n'.format('*', '')
    return ret

def montaWorkingCALE():
    ret  = '{:<7}    AREA DO CALE1000 PARA CONSISTENCIA DE DATA/HORA\n'.format('*')
    ret += '{:<7}{:->64}\n'.format('*', '')
    ret += '{:11}COPY CALEWAAC.\n'.format('', interface)
    ret += '{:<7}{:->64}\n'.format('*', '')
    return ret

def montaModulos(modulo, controle, bookI, esifI, idxI, lbl, errLoc, tmplt, dicRegras, tpm, spi, pt):
    mdl, cmdl = montaModulo(modulo, controle, bookI, esifI, idxI, lbl, errLoc, tmplt, dicRegras, tpm, spi, pt)
    if  tpm == 'NX':
        dic ={'@ERRLOCAL2':errLoc.ErrLocal()}
        mdl = change(dic, mdl)
    return (mdl, cmdl)

def montaModulo(modulo, controle, bookI, esifI, idxI, lbl, errLoc, tmplt, dicRegras, tpm, spi, pt):
    movekeys = ''
    esifO = ''
    for k in dicRegras.keys():
        if 'EX' in dicRegras[k]:
            if  dicRegras[k]['EX']['modulo'] == modulo:
                fieldI = k
                fieldO = dicRegras[k]['EX']['coluna']
                bookO = dicRegras[k]['EX']['interface']
                movekeys += montaMove(fieldI, fieldO, bookI, bookO, esifI, esifO, 11, '.', idxI)
    label = lbl.Label()
    dic ={'@LABEL':label
         ,'@MODULO':modulo
         ,'@CONTROLE':controle
         ,'@ERRLOCAL1':errLoc.ErrLocal()
         ,'@MOVEKEYS':movekeys}
    template = open(os.path.join(tmplt,'modulo{}.cbl'.format(tpm))).read()
    cmdl = '{:{}}PERFORM {}-CHAMAR-{}{}\n'.format('', spi, label, modulo, pt)
    return (change(dic, template), cmdl)

def montaPartition(column, book, pks, dicRegras, dicCol, qlf):
    iPk = iterInv(pks) if dicRegras[column]['OR']['origem'][-1] == 'V' else iter(pks)
    string='STRING '
    ret = ''
    for pk in iPk:
        es = 'S-' if pk[1] == '3' else 'E-'
        ret += '{:11}{}{}-{}{}\n'.format('', string, book, es, pk[0].replace('_','-'))
        ret += '{:18}(LENGTH OF {}-{}{}:1)\n'.format('', book, es, pk[0].replace('_','-'))
        string='     , '
    for x in xrange(dicCol[column].colunas.tamanhoColuna - len(pks)):
        ret += '{:11}{}ZEROS\n'.format('', string)
    ret += '{:18}DELIMITED BY SIZE\n'.format('')
    ret += '{:18}INTO      {:23}{}\n'.format('', column.replace('_','-'), qlf)
    ret += '{:11}END-STRING.\n\n'.format('')
    return ret

def tratarRegras(regra, regras, field, col, bookI, esifO, errLoc, cale):
    return eval('regra{}(regra, regras, field, col, bookI, esifO, errLoc, cale)'.format(regra))

# Inicializa campos sem Regra de Preenchimento
def regraIN(field, col, bookI, esif):
    esif = esif + '-' if esif else ''
    natur = col.datatypes.picture_cobol
    cd = '{:11}IF  {}-{}{}{}\n'.format('', bookI, esif, field.replace('_','-'), dicCv[natur+'1'])
    if  natur == 'X':
        cd +='{:12}OR {}-{}{}{}\n'.format('', bookI, esif, field.replace('_','-'), dicCv[natur+'2'])
    cd += '{:15}MOVE {} TO {}-{}{}\n'.format('', dicVal[natur], bookI, esif, field.replace('_','-'))
    cd += '{:11}END-IF.\n\n'.format('')
    return cd

#  Preenchimento
def regraPR(regra, regras, field, col, bookI, esifO, errLoc, cale):
    esifO = esifO + '-' if esifO else ''
    natur = col.datatypes.picture_cobol
    cd = '{:11}IF  {}-{}{} {}\n'.format('', bookI, esifO, field.replace('_','-'), dicCv[natur+'1'])
    if  natur == 'X':
        cd +='{:12}OR {}-{}{} {}\n'.format('', bookI, esifO, field.replace('_','-'), dicCv[natur+'2'])
    cd += messageError(errLoc, regras[regra]['message'])
    return cd

#  Operadores de Comparacao
def regraOC(regra, regras, field, col, bookI, esifO, errLoc, cale):
    esifO = esifO + '-' if esifO else ''
    regraCol = regras[regra]['regra'][regrasColunas]
    cmprdr = regraCol.regrasColunas.argumento1
    cd = '{:11}IF  {}-{}{} {} {}\n'.format('', bookI, esifO, field.replace('_','-'), dicInv[regra], cmprdr)
    cd += messageError(errLoc, regras[regra]['message'])
    return cd

regraEQ = regraOC    # Igual
regraNE = regraOC    # Diferente
regraLT = regraOC    # Menor Que
regraLE = regraOC    # Menor ou Igual
regraGT = regraOC    # Maior Que
regraGE = regraOC    # Maior ou Igual

# Range e Valores
def regraRV(regra, regras, field, col, bookI, esifO, errLoc, cale):
    esifO = esifO + '-' if esifO else ''
    fieldValid = '{}-{}{}-VALIDO'.format(bookI, esifO, field.replace('_','-'))[:30]
    cd = '{:11}IF NOT {}\n'.format('', fieldValid)
    cd += messageError(errLoc, regras[regra]['message'])
    return cd

regraRG = regraRV    # Range
regraVL = regraRV    # Valores

# Date
def regraDT(regra, regras, field, col, bookI, esifO, errLoc, cale):
    esifO = esifO + '-' if esifO else ''
    cd  = '{:11}MOVE 6 TO CALEWAAC-FMT-ARGMTO.\n'.format('')
    cd += '{:11}MOVE {}-{}{} TO CALEWAAC-VLR-ARGMTO\n'.format('', bookI, esifO, field.replace('_','-'))
    cd += '{:11}PERFORM 2800-CHAMAR-CALE1000.\n'.format('')
    cale.TrueCale()
    return cd

# Time
def regraTM(regra, regras, field, col, bookI, esifO, errLoc, cale):
    esifO = esifO + '-' if esifO else ''
    cd  = '{:11}MOVE 33 TO CALEWAAC-FMT-ARGMTO.\n'.format('')
    cd += '{:11}MOVE {}-{}{} TO CALEWAAC-VLR-ARGMTO\n'.format('', bookI, esifO, field.replace('_','-'))
    cd += '{:11}PERFORM 2800-CHAMAR-CALE1000.\n'.format('')
    cale.TrueCale()
    return cd

# Timestamp
def regraTS(regra, regras, field, col, bookI, esifO, errLoc, cale):
    esifO = esifO + '-' if esifO else ''
    cd  = '{:11}MOVE ?? TO CALEWAAC-FMT-ARGMTO.\n'.format('')
    cd += '{:11}MOVE {}-{}{} TO CALEWAAC-VLR-ARGMTO\n'.format('', bookI, esifO, field.replace('_','-'))
    cd += '{:11}PERFORM 2800-CHAMAR-CALE1000.\n'.format('')
    cale.TrueCale()
    return cd

def messageError(errLoc, message):
    preCon = '@APPLIDW00C'
    sufCon = 'OF LNK-@APPLID3@SIGLAPGM@TYPEPGM'
    errLocal = errLoc.ErrLocal()
    cd  = '{:15}MOVE {:11}TO {}-COD-RETORNO  {}\n'.format('', '08', preCon, sufCon)
    cd += "{:15}MOVE '{:}'     TO {}-COD-ERRO     {}\n".format('', errLocal, preCon, sufCon)
    cd += "{:15}MOVE '{:}' TO {}-COD-MENSAGEM {}\n".format('', message, preCon, sufCon)
    cd += '{:15}PERFORM 3000-FINALIZAR\n'.format('')
    cd += '{:11}END-IF.\n\n'.format('')
    return cd

def montaInsert(lisSql):
    comma = '('
    mi = '\n'
    mi += '{:11}EXEC SQL INSERT INTO @OWNERDB2.@TABLENAME\n'.format('')
    for column in lisSql:
        mi += '{:30}{} {}\n'.format('', comma, column[0])
        comma = ','
    comma = ') VALUES ( '
    for column in lisSql:
        mi += '{:21}{}{}\n'.format('', comma, column[1])
        comma = '         , '
    mi += '{:21})\n'.format('')
    mi += '{:11}END-EXEC.\n'.format('')
    return mi

def montaUpdate(lisSql, pks):
    pkk = [pk[0] for pk in pks]
    litset = 'SET'
    mu = '\n'
    mu += '{:11}EXEC SQL UPDATE @OWNERDB2.@TABLENAME\n'.format('')
    for column in lisSql:
        if  column[0] not in pkk:
#            mu += '{:16}{} {:19}= {}\n'.format('', litset, column[0], column[1])
            mu += '{:16}{:13}{:22}=\n'.format('', litset, column[0])
            mu += '{:19}{}\n'.format('', column[1])
            litset = '  ,'
    where = 'WHERE'
    for column in lisSql:
        if  column[0] in pkk:
            mu += '{:14}{:14} {:22}=\n'.format('', where, column[0])
            mu += '{:19}{}\n'.format('', column[1])
            where = '  AND'
    mu += '{:11}END-EXEC.\n'.format('')
    return mu

def montaDelete(lisSql):
    where = 'WHERE'
    md = '\n'
    md += '{:11}EXEC SQL DELETE FROM @OWNERDB2.@TABLENAME\n'.format('')
    for column in lisSql:
        md += '{:14}{:14} {:22}=\n'.format('', where, column[0])
        md += '{:19}{}\n'.format('', column[1])
        where = '  AND'
    md += '{:11}END-EXEC.\n'.format('')
    return md

def montaSelect(lisBookS, pks, dicCol):
    select = 'EXEC SQL SELECT'
    ms = '\n'
    for column in lisBookS:
        col = dicCol[column]
        if  col.colunasEntidades.ehNotNull:
            ms += '{:11}{} {}\n'.format('', select, column)
        else:
            if  col.datatypes.descricao == 'TIMESTAMP':
                ms += '{:11}{} IFNULL({},\n'.format('', select, column)
                ms += '{:43}{})\n'.format('', dicVal[col.datatypes.descricao])
            else:
                ms += '{:11}{} IFNULL({}, {})\n'.format('', select, column, dicVal[col.datatypes.descricao])
        select = '              ,'
    into = 'INTO'
    for column in lisBookS:
        ms += '{:22}{} :@DCLGEN.{}\n'.format('', into, column.replace('_','-'))
        into = '   ,'
    ms += '{:22}FROM @OWNERDB2.@TABLENAME\n'.format('')
    where = 'WHERE'
    for column in pks:
            ms += '{:21}{:16}{:22}=\n'.format('', where, column[0])
            ms += '{:27}:@DCLGEN.{}\n'.format('', column[0].replace('_','-'))
            where = '  AND'
    ms += '{:11}END-EXEC.\n'.format('')
    return ms

def montaDeclarecursor(lisBookS, pks, dicCol):
    select = 'SELECT'
    dc = ''
    for column in lisBookS:
        if  column == 'NREG_QTDE':
            continue
        col = dicCol[column]
        if  col.colunasEntidades.ehNotNull:
            dc += '{:21}{} {}\n'.format('', select, column)
        else:
            if  col.datatypes.descricao == 'TIMESTAMP':
                dc += '{:21}{} IFNULL({},\n'.format('', select, column)
                dc += '{:43}{})\n'.format('', dicVal[col.datatypes.descricao])
            else:
                dc += '{:21}{} IFNULL({}, {})\n'.format('', select, column, dicVal[col.datatypes.descricao])
        select = '     ,'
    return dc

def montaWherecursores(pks):
    ret = []
    for n in xrange(1,5):
        ret.append(montaWherecursor(pks, n))
    return ret

def montaWherecursor(pks, n):
    where = 'WHERE'
    mw = ''
    for column in pks:
        mw += '{:22}{:16}{:21}{}\n'.format('', where, column[0], dicOc[n])
        mw += '{:28}:@DCLGEN.{}\n'.format('', column[0].replace('_','-'))
        where = '  AND'
    orderby = 'ORDER BY'
    for column in pks:
        mw += '{:19}{} {:31}{}\n'.format('', orderby, column[0], dicAd[n])
        orderby = '       ,'
    return mw

def montaFetch(lisBookS):
    into = 'INTO'
    mf = ''
    for column in lisBookS:
        if  column == 'NREG_QTDE':
            continue
        mf += '{:15}{} :@DCLGEN.{}\n'.format('', into, column.replace('_','-'))
        into = '   ,'
    mf += '{:11}END-EXEC.\n\n'.format('')
    return mf
