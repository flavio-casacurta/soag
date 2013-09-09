# -*- coding:utf-8
'''
   Created on 07/05/2013
   @author: C&C - HardSoft
'''
#import pdb

from datetime import date
from Gerutl import *

class GerProg:

    def __init__(self, db):
        self.parms = db(db.parametros.id==1).select()[0]
        self.tmplt = os.path.join( '\\\\'
                                 , '127.0.0.1'
                                 , 'c$'
                                 , self.parms.web2py
                                 , 'applications'
                                 , self.parms.soag
                                 , 'Template'
                                 , 'PROG') + os.sep

    def gerProg(self, properties, prms):
        lisBookE   = prms[0]
        lisBookI   = prms[1]
        lisBookC   = lisBookI
        lisBookS   = prms[2]
        lisBookR   = prms[3]
        lisCol     = prms[4]
        dicCol     = prms[5]
        dicRegras  = prms[6]
        pks        = prms[7]
        dicModulos = prms[8]

        contratante = properties['CONTRATANTE']
        sp = '  ' if len(contratante) < 21 else ' ' if len(contratante) < 32 else ''
        ls = 45 - (len(properties['SERVICO']) + 1)
        lf = 90 - len(properties['SERVICO'])

        dicProg={'@ANALISTA'    :properties['ANALISTA']
                ,'@APPLID'      :properties['APPLID']
                ,'@APPLNAME'    :properties['APPLNAME']
                ,'@AUTHOR'      :'{}/{}'.format(properties['USERNAME'], properties['EMPRESA'])
                ,'@CONTRATANTE' :'{:^64}'.format(sp.join([x for x in contratante[:62]]))
                ,'@DATE'        :date.today().strftime('%d %b %Y').upper()
                ,'@ENTIDADE1'   :properties['ENTIDADE'][:ls]
                ,'@ENTIDADE2'   :properties['ENTIDADE'][ls:lf]
                ,'@ERROCICS'    :'{}9999'.format(properties['APPLID'])
                ,'@ERROMOD'     :'{}9999'.format(properties['APPLID'])
                ,'@ERROLIV'     :'{}9999'.format(properties['APPLID'])
                ,'@ERRODB2'     :'{}9999'.format(properties['APPLID'])
                ,'@GRUPO'       :properties['GRUPO']
                ,'@SIGLAPGM'    :properties['SIGLAPGM']
                ,'@TYPEPGM'     :properties['TYPEPGM']
                ,'@PERSISTENCIA':properties['PERSISTENCIA']
                ,'@SERVICO'     :properties['SERVICO']
                ,'@MSGSUCESSO'  :properties['MSGSUCESSO']
                ,'@MSGERRO'     :properties['MSGERRO']
                ,'@TABLENAME'   :properties['TABLENAME']
                }

        path = os.path.join( '\\\\'
                           , '127.0.0.1'
                           , 'c$'
                           , self.parms.raiz
                           , properties['EMPRESA'].replace(' ', '_')
                           , properties['APPLID']
                           , 'GERADOS'
                           , 'PGM') + os.sep

        if  properties['COORDENADOR']:
            self.coordenador( properties, lisBookE, lisBookI, lisBookS, lisBookR, dicRegras, dicModulos
                            , dicCol, dicProg, path)

        self.funcional( properties, lisBookE, lisBookI, lisBookS, lisBookR, dicRegras, dicModulos, dicCol
                      , dicProg, path)

        self.persistencia( properties, lisBookE, lisBookI, lisBookS, lisBookR, dicRegras, dicModulos, dicCol
                         , dicProg, lisCol, pks, path)

        nameProg = '{}1{}{}'.format(properties['APPLID'], properties['SIGLAPGM'], properties['TYPEPGM'])

        log = open(properties['LOG'], 'a')
        log.write('Gerserv - Programas e Books do modulo: {} - gerados OK\n'.format(nameProg))
        log.close()

    def coordenador(self, properties, lisBookE, lisBookI, lisBookS, lisBookR
                        , dicRegras, dicModulos, dicCol, dicProg, path):
        applId = properties['APPLID']
        siglapgm = properties['SIGLAPGM']
        booke = '{}W{}E'.format(applId, siglapgm)
        booki = '{}W{}I'.format(applId, siglapgm)
        books = '{}W{}S'.format(applId, siglapgm)
        typePgm = properties['TYPEPGM']
        tp = 'L' if typePgm == 'L' else 'X'
        lbl = Label(2690) if typePgm == 'L' else Label(2490)
        errLoc = ErrLocal(14) if typePgm == 'L' else ErrLocal(13)
        alimentarFuncional=''
        esifI = ''
        esifO = 'E'
        spi = 11
        pt = '.'
        for field in lisBookE:
            alimentarFuncional += montaMove(field, field, booke, booki, esifI, esifO, spi, pt)
        for k in dicRegras.keys():
            if  'OR' in dicRegras[k]:
                if  dicRegras[k]['OR']['fonte'] == 'F':
                    fldI = dicRegras[k]['OR']['origem']
                    fldO = k
                    alimentarFuncional += montaMove(fldI, fldO, '', booki, esifI, esifO, spi, pt)

        gravarDadosSaida = ''
        areaDeSaida = ''
        rembookSaida = ''
        dadosSaida = ''
        remBookFuncionais=''
        remModlFuncionais=''
        workingFuncionais=''
        modulosFuncionais=''

        if  lisBookS:
            rembookSaida += '{:>7}{:4}{} - BOOK SAIDA DE DADOS PARA FRAMEWORK\n'.format('*', '',books)
            esifI = 'S'
            esifO = ''
            spi = 14 if typePgm == 'L' else 11
            pt = '' if typePgm == 'L' else '.'
            idxI = '(WRK-IDX)' if typePgm == 'L' else ''
            idxO = '(WRK-IDX)' if typePgm == 'L' else ''
            for field in lisBookS:
                dadosSaida += montaMove(field, field, booki, books, esifI, esifO, spi, pt, idxI, idxO)

            if  lisBookR:
                idxI = ''
                modulosProc = []
                for field in lisBookR:
                    modulo = dicModulos[field]['modulo']
                    if  modulo not in modulosProc:
                        interface = dicModulos[field]['interface']
                        controle = dicModulos[field]['controle']
                        remBookFuncionais+='{:>7}{:4}{} - BOOK COMUNICACAO COM FUNCIONAL {}\n'.format('*', ''
                                                                                                   ,interface, modulo)
                        remModlFuncionais+='{:>7}{:4}{} - MODULO FUNCIONAL\n'.format('*', '', modulo)
                        workingFuncionais+= montaWorkingFuncionais(modulo, controle, interface)
                        mdl, cmdl = montaModulos(modulo, controle, booki, esifI, idxI, lbl
                                                , errLoc, self.tmplt, dicRegras, 'FU', spi, pt)
                        modulosFuncionais += mdl
                        dadosSaida += cmdl
                        modulosProc.append(modulo)
                    dadosSaida += montaMove(field, field, booki, books, esifI, esifO, spi, pt, idxI, idxO)

            areaDeSaida = open(os.path.join(self.tmplt,'areadesaida.CBL')).read()

            gds = open(os.path.join(self.tmplt,'GDS{}.CBL'.format(tp))).read()
            dic = {'@DADOSSAIDA\n'  :dadosSaida}
            gravarDadosSaida = change(dic, gds)

        dic = {'@ALIMENTARFUNCIONAL\n':alimentarFuncional
              ,'@REMBOOKSAIDA\n'      :rembookSaida
              ,'@AREADESAIDA\n'       :areaDeSaida
              ,'@GRAVARDADOSSAIDA\n'  :gravarDadosSaida
              ,'@REMBOOKFUNCIONAIS\n' :remBookFuncionais
              ,'@REMMODLFUNCIONAIS\n' :remModlFuncionais
              ,'@WORKINGFUNCIONAIS\n' :workingFuncionais
              ,'@MODULOSFUNCIONAIS\n' :modulosFuncionais}

        template = open(os.path.join(self.tmplt,'1XX{}.CBL'.format(tp))).read()
        prog = change(dic, template)

        lenblpag = calcLenblpag(lisBookE, dicCol)
        dicProg['@LENBLPAG'] = str(lenblpag)
        dicProg['@LENBOOKP'] = str(lenblpag + 13)
        prog = insAster72(change(dicProg,prog))
        nameProg = '{}1{}{}'.format(applId, siglapgm, typePgm)
        progName = os.path.join(path, '{}.cbl'.format(nameProg))
        progWrite = open(progName, 'w')
        progWrite.write(prog)
        progWrite.close()

    def funcional(self, properties, lisBookE, lisBookI, lisBookS, lisBookR
                      , dicRegras, dicModulos, dicCol, dicProg, path):
        applId = properties['APPLID']
        siglapgm = properties['SIGLAPGM']
        booki = '{}W{}I'.format(applId, siglapgm)
        typePgm = properties['TYPEPGM']
        tp = 'L' if typePgm == 'L' else 'X'
        lbl = Label(2690) if typePgm == 'L' else Label(2490)
        errLoc = ErrLocal(34) if typePgm == 'L' else ErrLocal(33)
        esifI = 'E'
        cale = Cale(False)
        remBookArquitetur = ''
        remBookFuncionais = ''
        remModlFuncionais = ''
        workingFuncionais = ''
        chamarFuncionais = ''
        modulosFuncionais = ''
        consistirDados = '\n'
        for field in lisBookI:
            if  field in dicRegras:
                regras = dicRegras[field]
                col = dicCol[field]
                if  'PR' not in regras:
                    consistirDados += regraIN(field, col, booki, esifI)
                for regra in regras:
                    if  regra not in ('XE', 'OR', 'EX', 'NX'):
                        errLocal = errLoc.ErrLocal()
                        consistirDados += tratarRegras(regra, regras, field , col
                                                      , booki, esifI, errLoc, cale)

        if  typePgm == 'I':
            dicModulo = {}
            for k in dicRegras.keys():
                for r in dicRegras[k]:
                    if  r == 'NX':
                        if  dicRegras[k][r]['modulo'] not in dicModulo.keys():
                            dicModulo[dicRegras[k][r]['modulo']]={'interface':dicRegras[k][r]['interface']
                                                                 ,'controle':dicRegras[k][r]['controle']}
            for modulo in dicModulo.keys():
                controle  = dicModulo[modulo]['controle']
                interface = dicModulo[modulo]['interface']
                if  modulo[:4] != applId:
                    remBookFuncionais+='{:>7}{:4}{} - BOOK DE CONTROLE DO  FUNCIONAL {}\n'.format('*', ''
                                                                                                 ,controle, modulo)
                remBookFuncionais+='{:>7}{:4}{} - BOOK COMUNICACAO COM FUNCIONAL {}\n'.format('*', ''
                                                                                           ,interface, modulo)
                remModlFuncionais+='{:>7}{:4}{} - MODULO FUNCIONAL\n'.format('*', '', modulo)
                workingFuncionais+= montaWorkingFuncionais(modulo, controle, interface)
                mdl, cmdl = montaModulos(modulo, controle, booki, esifI, '', lbl
                                        , errLoc, self.tmplt, dicRegras, 'NX', 11, '.')
                modulosFuncionais += mdl
                chamarFuncionais += cmdl

        if  typePgm in ('I','A'):
            dicModulo = {}
            for k in dicRegras.keys():
                for r in dicRegras[k]:
                    if  r == 'EX':
                        if  dicRegras[k][r]['modulo'] not in dicModulo.keys():
                            dicModulo[dicRegras[k][r]['modulo']]={'interface':dicRegras[k][r]['interface']
                                                                 ,'controle':dicRegras[k][r]['controle']}
            for modulo in dicModulo.keys():
                controle  = dicModulo[modulo]['controle']
                interface = dicModulo[modulo]['interface']
                if  modulo[:4] != applId:
                    remBookFuncionais+='{:>7}{:4}{} - BOOK DE CONTROLE DO  FUNCIONAL {}\n'.format('*', ''
                                                                                                 ,controle, modulo)
                remBookFuncionais+='{:>7}{:4}{} - BOOK COMUNICACAO COM FUNCIONAL {}\n'.format('*', ''
                                                                                           ,interface, modulo)
                remModlFuncionais+='{:>7}{:4}{} - MODULO FUNCIONAL\n'.format('*', '', modulo)
                workingFuncionais+= montaWorkingFuncionais(modulo, controle, interface)
                mdl, cmdl = montaModulos(modulo, controle, booki, esifI, '', lbl
                                        , errLoc, self.tmplt, dicRegras, 'EX', 11, '.')
                modulosFuncionais += mdl
                chamarFuncionais += cmdl
        elif typePgm == 'E':
            field = lisBookE[0]
            if  'EX' in dicRegras[field].keys():
                modulo = dicRegras[field]['EX']['modulo']
                controle  = dicRegras[field]['EX']['controle']
                interface = dicRegras[field]['EX']['interface']
                if  modulo[:4] != applId:
                    remBookFuncionais+='{:>7}{:4}{} - BOOK DE CONTROLE DO  FUNCIONAL {}\n'.format('*', ''
                                                                                                 ,controle, modulo)
                remBookFuncionais+='{:>7}{:4}{} - BOOK COMUNICACAO COM FUNCIONAL {}\n'.format('*', ''
                                                                                           ,interface, modulo)
                remModlFuncionais+='{:>7}{:4}{} - MODULO FUNCIONAL\n'.format('*', '', modulo)
                workingFuncionais+= montaWorkingFuncionais(modulo, controle, interface)
                mdl, cmdl = montaModulos(modulo, controle, booki, esifI, '', lbl
                                        , errLoc, self.tmplt, dicRegras, 'EX', 11, '.')
                modulosFuncionais += mdl
                chamarFuncionais += cmdl

        if  cale.cale:
            remBookArquitetur += '{:>7}{:4}CALEWAAC - AREA DO CALE1000  - CONSISTENCIA DATA/HORA\n'.format('*', '')
            remModlFuncionais+='{:>7}{:4}{} - CONSISTENCIA DATA/HORA\n'.format('*', '', 'CALE1000')
            dic ={'@ERRLOCAL':errLoc.ErrLocal()}
            moduloCALE = open(os.path.join(self.tmplt,'moduloCALE.cbl')).read()
            modulosFuncionais += change(dic, moduloCALE)

        dic = {'@REMBOOKARQUITETUR\n' :remBookArquitetur
              ,'@REMBOOKFUNCIONAIS\n' :remBookFuncionais
              ,'@REMMODLFUNCIONAIS\n' :remModlFuncionais
              ,'@WORKINGFUNCIONAIS\n' :workingFuncionais
              ,'@CONSISTIRDADOS\n'    :consistirDados
              ,'@CHAMARFUNCIONAIS\n'  :chamarFuncionais
              ,'@MODULOSFUNCIONAIS\n' :modulosFuncionais}

        if  typePgm in ('C','L'):
            dic['@INVOKINGPROG\n'] = ''
            dic['@WRKINVOKINGPROG\n'] = ''
        else:
            dic['@INVOKINGPROG\n'] = open(os.path.join(self.tmplt,'invokingprog.cbl')).read()
            dic['@WRKINVOKINGPROG\n'] = '{:7}77  WRK-INVOKINGPROG{:12}PIC  X(008) VALUE SPACES.\n'.format('','')

        template = open(os.path.join(self.tmplt,'3XXX.CBL')).read()
        prog = change(dic, template)

        prog = insAster72(change(dicProg,prog))
        nameProg = '{}3{}{}'.format(applId, siglapgm, typePgm)
        progName = os.path.join(path, '{}.cbl'.format(nameProg))
        progWrite = open(progName, 'w')
        progWrite.write(prog)
        progWrite.close()

    def persistencia(self, properties, lisBookE, lisBookI, lisBookS, lisBookR
                         , dicRegras, dicModulos, dicCol, dicProg, lisCol, pks, path):
        applId = properties['APPLID']
        siglapgm = properties['SIGLAPGM']
        bookC = '{}W{}C'.format(applId, siglapgm)
        typePgm = properties['TYPEPGM']
        tp = 'L' if typePgm == 'L' else 'X'
        errlocal = '0045' if typePgm == 'L' else '0044'
        persistencia = properties['PERSISTENCIA']
        esifI = 'E'
        esifO = 'S'
        spi = 11
        pt = '.'
        idxO = '(WRK-NREG-QTDE)' if typePgm == 'L' else ''
        label = '2300' if typePgm == 'L' else '2200'
        dclgen =properties['DCLGEN']
        qlf = 'OF {}'.format(dclgen)
        dicSql = {'I':'INSERT', 'U':'UPDATE', 'D':'DELETE', 'S':'SELECT'}
        comandosql = dicSql[persistencia]
        sqlselectmax = ''
        performLabel = ''
        movedclgen = ''
        valorizarpks = ''
        instrucaosql = ''
        valorizardclgen = ''
        valorizarbook = ''
        pksdclgen = ''
        pksProcessadas=[]
        wheredclgen = ''
        movetobooks = ''
        where = 'WHERE'
        if  typePgm == 'I':
            pkI = False
            for pk in pks:
                if  pk[1] != '3':
                    pksdclgen += moveBookToDcl(pk[0], pk[0], qlf, bookC, esifI, spi, pt)
                    wheredclgen += '{:21}{:16}{:23}=\n'.format('', where, pk[0])
                    wheredclgen += '{:27}:{}.{}\n'.format('', dclgen, pk[0].replace('_', '-'))
                    where = '  AND'
                else:
                    pkI = True
                    colpk = pk[0]
                    colcbl = pk[0].replace('_', '-')
                    movetobooks += moveDclToBook(pk[0], qlf, bookC, esifO, spi, pt)
                    movetobooks += '\n'
            if  pkI and dicCol[pk[0]].datatypes.descricao != 'TIMESTAMP':
                pksProcessadas = [pk[0] for pk in pks]
                wheredclgen += '{:11}END-EXEC.\n'.format('')
                dic = {'@PKSDCLGEN\n'  :pksdclgen
                      ,'@ERRLOCAL'     :errlocal
                      ,'@COLPK'        :colpk
                      ,'@COLCBL'       :colcbl
                      ,'@MOVETOBOOKS\n':movetobooks
                      ,'@WHEREDCLGEN\n':wheredclgen}
                selMax = open(os.path.join(self.tmplt,'selectmax.cbl')).read()
                sqlselectmax = change(dic, selMax)

        if  typePgm == 'L':
            for p in xrange(len(pks)-1):
                pk = pks[p]
                valorizardclgen += moveBookToDcl(pk[0], pk[0], qlf, bookC, esifI, spi, pt)
                wheredclgen += '{:21}{:16}{:23}=\n'.format('', where, pk[0])
                wheredclgen += '{:27}:{}.{}\n'.format('', dclgen, pk[0].replace('_', '-'))
                where = '  AND'
            wheredclgen += '{:11}END-EXEC.\n'.format('')
            pk = pks[len(pks)-1]
            colpk = pk[0]
            colcbl = pk[0].replace('_', '-')
            moveultimakey = moveBookToDcl(pk[0], pk[0], qlf, bookC, esifI, 14, '')
            pksProcessadas = [pk[0] for pk in pks]
            dic = {'@PKSDCLGEN\n'  :pksdclgen
                  ,'@ERRLOCAL'     :errlocal
                  ,'@COLPK'        :colpk
                  ,'@COLCBL'       :colcbl
                  ,'@MOVETOBOOKS\n':movetobooks
                  ,'@WHEREDCLGEN\n':wheredclgen}
            selMax = open(os.path.join(self.tmplt,'selectmax.cbl')).read()
            sqlselectmax = change(dic, selMax)

        colTimestamp = []
        colPartition = []
        if  typePgm in ('I','A'):
            for f in dicRegras.keys():
                if  'OR'in dicRegras[f].keys():
                    if  dicRegras[f]['OR']['fonte'] == 'S':
                        if  dicRegras[f]['OR']['origem'] == 'CURRENT TIMESTAMP':
                            colTimestamp.append(f)
                        elif (dicRegras[f]['OR']['origem'] == 'PARTITIONH'
                          or  dicRegras[f]['OR']['origem'] == 'PARTITIONV'):
                            colPartition.append(f)

        lisSql = []
        for column in lisCol:
            host = ':@DCLGEN.{}'.format(column.replace('_','-'))
            if  column in pksProcessadas:
                lisSql.append((column, host))
            elif column not in lisBookI:
                if  column in colTimestamp:
                    lisSql.append((column, 'CURRENT_TIMESTAMP'))
                elif column in colPartition:
                    lisSql.append((column, host))
                    valorizardclgen += montaPartition(column, bookC, pks, dicRegras, dicCol, qlf)
            else:
                lisSql.append((column, host))
                if dicCol[column].datatypes.descricao == 'VARCHAR':
                    valorizardclgen += moveBookToDcl(column, column + '-TEXT', qlf, bookC, esifI, spi, pt)
                    valorizardclgen += calculaLenVarchar(column, qlf)
                else:
                    valorizardclgen += moveBookToDcl(column, column, qlf, bookC, esifI, spi, pt)

        if   typePgm == 'I':
             instrucaosql += montaInsert(lisSql)
        elif typePgm == 'A':
             instrucaosql += montaUpdate(lisSql, pks)
        elif typePgm == 'E':
             instrucaosql += montaDelete(lisSql)
        elif typePgm == 'C':
             instrucaosql += montaSelect(lisBookS, pks, dicCol)
#       elif typePgm == 'L':
        else:
             declarecursor = montaDeclarecursor(lisBookS, pks, dicCol)
             fetchcursor = montaFetch(lisBookS)

        if  lisBookS:
            performLabel += '{:11}PERFORM {}-MOVE-@DCLGEN-TO-@APPLIDW@SIGLAPGMC.\n'.format('', label)
            for field in lisBookS:
                if  field == 'NREG_QTDE':
                    continue
                valorizarbook += moveDclToBook(field, qlf, bookC, esifO, spi, pt, idxO)
            mdc = open(os.path.join(self.tmplt,'movedclgen.cbl')).read()
            dic = {'@LABEL'          :label
                  ,'@VALORIZARBOOK\n':valorizarbook}
            movedclgen = change(dic, mdc)

        dic = {'@COMANDOSQL'        :comandosql
              ,'@SQLSELECTMAX\n'    :sqlselectmax
              ,'@PERFORMLABEL\n'    :performLabel
              ,'@MOVEDCLGEN\n'      :movedclgen
              ,'@INSTRUCAOSQL\n'    :instrucaosql
              ,'@VALORIZARDCLGEN\n' :valorizardclgen}

        if  typePgm == 'L':
            wherecursor1, wherecursor2, wherecursor3, wherecursor4 = montaWherecursores(pks)
            optimize = calcOptimize(lisBookS, dicCol)
            dic['@WHERECURSOR1\n'] = wherecursor1
            dic['@WHERECURSOR2\n'] = wherecursor2
            dic['@WHERECURSOR3\n'] = wherecursor3
            dic['@WHERECURSOR4\n'] = wherecursor4
            dic['@OPTIMIZE'] = str(optimize + 1)
            dic['@QOCC'] = str(optimize)
            dic['@DECLARECURSOR\n'] = declarecursor
            dic['@FETCHCURSOR\n'] = fetchcursor
            dic['@MOVEULTIMAKEY\n'] = moveultimakey

        template = open(os.path.join(self.tmplt,'4XX{}.CBL'.format(tp))).read()
        prog = change(dic, template)
        dicProg['@ENTIDADELABEL'] = properties['ENTIDADE'][:18].replace(' ', '-')
        dicProg['@ENTIDADE3'] = properties['ENTIDADE'][:31]
        dicProg['@ENTIDADE4'] = properties['ENTIDADE'][31:62]
        dicProg['@DCLGEN'] = properties['DCLGEN']
        dicProg['@OWNERDB2'] = properties['OWNERDB2']

        prog = insAster72(change(dicProg,prog))
        nameProg = '{}4{}{}'.format(applId, siglapgm, persistencia)
        progName = os.path.join(path, '{}.cbl'.format(nameProg))
        progWrite = open(progName, 'w')
        progWrite.write(prog)
        progWrite.close()
