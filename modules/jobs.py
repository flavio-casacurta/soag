# -*- coding: utf-8 -*-

from   datetime import date
import utilities as utl
import datetime, traceback, os
import ColunasEntidades

def lrecl(db, entidade_id):

    retColunasEntidades = ColunasEntidades.ColunasEntidades(db).\
               selectColunasEntidadesResolvidasByCodigoEntidade(entidade_id)[1]

    length = 0

    for regcampo in retColunasEntidades:

        if  not regcampo.colunasEntidades.ehNotNull:
            length += 1
        if  regcampo.datatypes.picture_cobol == '9':
            length += ((regcampo.colunas.tamanhoColuna / 2) + 1)
        else:
            length += regcampo.colunas.tamanhoColuna

        if  regcampo.datatypes.descricao == 'NCHAR'    or \
            regcampo.datatypes.descricao == 'NVARCHAR' or \
            regcampo.datatypes.descricao == 'VARCHAR':
            length += 2

    return length

def startLength(db, entidade, idcampo):

    regcampos = ColunasEntidades.ColunasEntidades(db).\
               selectColunasEntidadesResolvidasByCodigoEntidade(entidade)[1]
    start     = 0
    length    = 0
    tipocampo = 'CH'

    for regcampo in regcampos:

        cpo   = regcampo.colunas.id

        if  cpo == idcampo:
            start += 1
            length = 0
            if  regcampo.datatypes.picture_cobol == '9':
                length += ((regcampo.colunas.tamanhoColuna / 2) + 1)
                tipocampo   = 'PD'
            else:
                length   += regcampo.colunas.tamanhoColuna
                tipocampo = 'CH'
            if  regcampo.datatypes.datatype == '-9' or \
                regcampo.datatypes.datatype == '-15' or \
                regcampo.datatypes.datatype == '12':
                length   += 2
            break

        if  regcampo.datatypes.picture_cobol == '9':
            start += ((regcampo.colunas.tamanhoColuna / 2) + 1)
        else:
            start += regcampo.colunas.tamanhoColuna
        if  str(regcampo.datatypes.datatype) == '-9'  or \
            str(regcampo.datatypes.datatype) == '-15' or \
            str(regcampo.datatypes.datatype) == '12':
            start += 2

    return ['%s,%s%s' % (start, length, ',%s' % tipocampo), tipocampo]

def lreclBook(db, table, book, book_id):

    regcampos = db(db[table][book]==book_id).select()

    length    = 0
    nivel     = 0

    for regcampo in regcampos:

        if  regcampo.redefines:
            nivel = regcampo.nivel
            continue

        if  nivel and regcampo.nivel > nivel:
            continue

        nivel   = 0

        length += (regcampo.bytes * (regcampo.occurs \
                                                    if regcampo.occurs else 1))

    return length

def startLengthBook(db, table, book, book_id, idcampo):

    regcampos = db(db[table][book]==book_id).select()

    start     = 0
    length    = 0
    tipocampo = 'CH'

    for regcampo in regcampos:

        cpo = regcampo.id

        if  cpo == idcampo:
            start  = regcampo.posicao * (regcampo.occurs \
                                                     if regcampo.occurs else 1)
            length = regcampo.bytes
            if  regcampo.natureza == '9':
                if  regcampo.tipo.find('COMP-3') > -1:
                    tipocampo = 'PD'
                elif  regcampo.tipo.find('COMP') > -1:
                    tipocampo = 'BI'
                else:
                    tipocampo = 'ZD'
            else:
                tipocampo = 'CH'
            break

    return ['%s,%s%s' % (start, length, ',%s' % tipocampo), tipocampo]

def booksImport(ids, db, folder, aplicacao, user):

    if  not ids:
        return {'retorno': False, 'flash': 'Nenhum book selecionado', \
                                  'labelErrors': '', 'msgsErrors': {}}

    bookTxts    = db(db.booksTxt.id.belongs((int(x) for x in ids))).select()

    procs       = 0
    flash       = 'Processamento efetuado'
    labelErrors = 'Resultado do processamento'
    msgsErrors  = {}

    for bookTxt in bookTxts:
        if  bookTxt.codigoAplicacao <> aplicacao or \
            bookTxt.status          <> 2:
            continue
        procs  += 1
        book    = bookTxt.nome
        rowbook = db(db.books.nome==book).select().first()
        if  not rowbook:
            db(db.books.insert(codigoAplicacao=aplicacao, \
                                    nome=book, \
                                    descricao='Book ' + book, \
                                    usuarioConfirmacao=user, \
                                    dataConfirmacao=datetime.datetime.\
                                    today()))
        else:
            db(db.books.id==rowbook.id).update(nome=book, \
                                                    descricao='Book %s' % \
                                                    book, \
                                                    usuarioConfirmacao=\
                                                    user, \
                                                    dataConfirmacao=\
                                                    datetime.datetime.today())
            db(db.booksCampos.book==rowbook.id).delete()
        rowbook = db(db.books.nome==book).select().first()
        if  bookTxt.nomeExtenso:
            arqFile = bookTxt.nomeExtenso
        else:
            arqFile = os.path.join( folder
                                  , 'uploads'
                                  , str(bookTxt.arquivo))
        ib = importBook(db, arqFile, rowbook, user, folder)
        if  not ib['retorno']:
            return {'retorno': False, \
                    'flash': ib['flash'], \
                    'labelErrors': ib['labelErrors'], \
                    'msgsErrors': ib['msgsErrors']}
        db(db.booksTxt.id==bookTxt.id).update(status=3, \
                                          mensagem='Carga efetuada no Sistema')

    if  bookTxts:
        if  procs:
            msgsErrors[0] = 'Importacao de Book. Done.'
        else:
            msgsErrors[0] = \
                           'Nenhum book pendente encontrado para processamento'

    return {'retorno': True, 'flash': flash, 'labelErrors': labelErrors, \
                             'msgsErrors': msgsErrors, 'id': rowbook.id}

def importBook(db, arqFile, rowbook, user, folder):

    flash       = 'book importado'
    labelErrors = 'Resultado da importacao'
    msgsErrors  = {}

    try:
        linFile = file(arqFile).readlines()
    except:
        erros = traceback.format_exc()
        if  erros:
            idx = 0
            for erro in erros.split('\n'):
                if  len(erro) > 1:
                    idx += 1
                    msgsErrors[idx] = erro
        return {'retorno': False, \
                'flash': 'Erro na leitura do arquivo', \
                'labelErrors': arqFile, 'msgsErrors': msgsErrors}

    linhas = []

    for arq in linFile:
        arq = arq.replace('\r', '').replace('\n', '')
        if  arq <> '' and arq[6: 7] <> '*':
            linhas.append(arq.upper())

    while True:
        copy = False
        for li in linhas:
            if  li.find('COPY') > -1:
                copy = True
                break
        if  not copy:
            break
        idx = -1
        for li in linhas:
            idx += 1
            if  li.find('COPY') > -1:
                cols  = li.split()
                book  = cols[1].replace("'",'').replace('.','')
                rbook = db(db.books.nome==book).select().first()
                if  not rbook:
                    msgsErrors[idx] = 'COPY nao importado na ferramenta.'
                    return {'retorno': False, \
                            'flash': 'Erro na leitura do COPY', \
                            'labelErrors': 'COPY: %s' % book, \
                            'msgsErrors': msgsErrors}
                bookTxt = db(db.booksTxt.nome==book).select().first()
                if  bookTxt.nomeExtenso:
                    arqFile = bookTxt.nomeExtenso
                else:
                    arqFile = os.path.join( folder
                                          , 'uploads'
                                          , str(bookTxt.arquivo))
                try:
                    linFile = file(arqFile).readlines()
                except:
                    erros = traceback.format_exc()
                    if  erros:
                        idx = 0
                        for erro in erros.split('\n'):
                            if  len(erro) > 1:
                                idx += 1
                                msgsErrors[idx] = erro
                    return {'retorno': False, \
                            'flash': 'Erro na leitura do arquivo', \
                            'labelErrors': arqFile, 'msgsErrors': msgsErrors}
                linhas.pop(idx)
                idx2 = 0
                for arq in linFile:
                    if  arq[6: 7] <> '*':
                        linhas.insert(idx+idx2, arq.upper())
                        idx2 += 1
                break

    linhaf      = ''
    redefines   = ''
    posdic      = {}
    idxFiller   = 1
    idx         = 0
    posicao     = 1
    itemGrupo   = []
    nivel       = 0
    occurs      = 0
    niveloccurs = 0
    idl         = 0

    for li in linhas:
        if  li.find('.') < 0:
            linhaf += li.upper()
            continue
        linhaf += li.upper()
        linha   = linhaf.split()
        idl    += 1
        nivel   = int(linha[0])
        campo = linha[1].replace('.','')
        if  campo == 'FILLER':
            cpo        = '%s_%s' % (campo, '{:>02}'.format(idxFiller))
            idxFiller += 1
        else:
            cpo = campo
        itemGrupo.append([nivel, cpo])
        cpox  = ''
        for idx in xrange(idl-1, 0, -1):
            if  itemGrupo[idx][0] < nivel:
                cpox = itemGrupo[idx][1]
                break
        if  linhaf.find('REDEFINES ') > -1 and linhaf.find('PIC ') < 0:
            redefines   = linha[3].replace('.','')
            posdic[cpo] = posicao = posdic[redefines]
            db(db.booksCampos.insert(book=rowbook.id, nome=cpo, \
                nivel=nivel, natureza='', posicao=posdic[cpo], \
                    picture='', tamanho='', inteiro=0, decimais=0, \
                        tipo='', bytes=0, redefines=redefines, \
                            itemGrupo=cpox, occurs=occurs, \
                                usuarioConfirmacao=user, \
                                    dataConfirmacao=datetime.datetime.\
                                        today()))
            linhaf = ''
            continue
        if  linhaf.find('REDEFINES ') > -1 and \
            linhaf.find('PIC ') > -1:
            picture = linha[5]
            picts   = picture.replace('.','')
            if  len(linha) > 6:
                if  len(linha) == 7:
                    picture += (' ' + linha[6])
                else:
                    for idx in xrange(6, len(linha)-1):
                        if  linha[idx].upper() <> 'VALUE':
                            picture += (' ' + linha[idx])
            picture  = picture.replace('S','')
            pict     = ''
            inteiro  = 0
            decimais = 0
            tam      = ''
            dec      = ''
            idx      = 0
            while picture[idx:idx+1] <> '(' and \
                  picture[idx:idx+1] <> ' ' and \
                  picture[idx:idx+1] <> '.':
                  pict += picture[idx:idx+1]
                  idx  += 1
            idx += 1
            while picture[idx:idx+1] == ' ':
                  idx += 1
            while picture[idx:idx+1] <> ')' and \
                  picture[idx:idx+1] <> ' ' and \
                  picture[idx:idx+1] <> '.':
                  tam += picture[idx:idx+1]
                  idx += 1
            idx += 1
            while picture[idx:idx+1] == ' ':
                  idx += 1
            if  picture[idx:idx+1] == 'V':
                dec  = 'V'
                idx += 1
                while picture[idx:idx+1] == '9' or \
                      picture[idx:idx+1] == '(' or \
                      picture[idx:idx+1] == ' ' or \
                      picture[idx:idx+1] == '.':
                      idx += 1
                if  picture[idx:idx+1] <> 'U' and \
                    picture[idx:idx+1] <> '.':
                    while picture[idx:idx+1] <> ')' and \
                          picture[idx:idx+1] <> ' ' and \
                          picture[idx:idx+1] <> '.':
                          dec += picture[idx:idx+1]
                          idx += 1
            if  dec == 'V': dec = ''
            if  dec <> '' and (dec[1:] >= '0' and dec[1:] <= '9'):
                inteiro  = int(tam)
                decimais = int(dec[1:])
                tam      = str(int(tam) + int(dec[1:]))
            else:
                inteiro  = int(tam)
                decimais = 0
            tam    += dec
            tipo    = ''
            idxtipo = picture.find(' COMP')
            if  idxtipo > -1:
                idxtipo += 1
                while picture[idxtipo:idxtipo+1] <> ' ' and \
                      picture[idxtipo:idxtipo+1] <> '.':
                      tipo    += picture[idxtipo:idxtipo+1]
                      idxtipo += 1
            redefines   = linha[3].replace('.','')
            posdic[cpo] = posicao = posdic[redefines] + 1
            db(db.booksCampos.insert(book=rowbook.id, nome=cpo, \
                nivel=nivel, natureza=pict, posicao=posdic[cpo], \
                    picture=picts, tamanho=tam, inteiro=inteiro, \
                        decimais=decimais if decimais else 0, \
                            tipo=tipo, bytes=0, redefines=redefines, \
                                itemGrupo=cpox, occurs=occurs, \
                                    usuarioConfirmacao=user, \
                                        dataConfirmacao=datetime.\
                                            datetime.today()))
            linhaf = ''
            continue
        if  linhaf.find('OCCURS ') > -1:
            if  len(linha) == 4:
                occurs  = int(linha[3].replace('.',''))
            elif len(linha) == 5:
                occurs  = int(linha[3].replace('.',''))
            else:
                occurs  = int(linha[5].replace('.',''))
            niveloccurs = nivel
            posdic[cpo] = posicao
            db(db.booksCampos.insert(book=rowbook.id, nome=cpo, \
                nivel=nivel, natureza='', posicao=posdic[cpo], \
                    picture='', tamanho='', inteiro=0, decimais=0, \
                        tipo='', bytes=0, redefines='', \
                            itemGrupo=cpox, occurs=occurs, \
                                usuarioConfirmacao=user, \
                                    dataConfirmacao=datetime.datetime.\
                                        today()))
            linhaf = ''
            continue
        if  linhaf.find('PIC ') < 0:
            posdic[cpo] = posicao
            db(db.booksCampos.insert(book=rowbook.id, nome=cpo, \
                nivel=nivel, natureza='', posicao=posdic[cpo], \
                    picture='', tamanho='', inteiro=0, decimais=0, \
                        tipo='', bytes=0, redefines='', \
                            itemGrupo=cpox, occurs=occurs, \
                                usuarioConfirmacao=user, \
                                    dataConfirmacao=datetime.datetime.\
                                        today()))
            linhaf = ''
            continue
        if  occurs:
            if  nivel <= niveloccurs:
                occurs      = 0
                niveloccurs = 0
        redefines = ''
        linhaf    = ''
        picture   = linha[3]
        picts     = picture.replace('.','')
        if  len(linha) > 4:
            if  len(linha) == 5:
                picture += (' ' + linha[4])
            else:
                for idx in xrange(4, len(linha)-1):
                    if  linha[idx].upper() <> 'VALUE':
                        picture += (' ' + linha[idx])
        picture  = picture.replace('S','')
        pict     = ''
        inteiro  = 0
        decimais = 0
        tam      = ''
        dec      = ''
        idx      = 0
        while picture[idx:idx+1] <> '(' and \
              picture[idx:idx+1] <> ' ' and \
              picture[idx:idx+1] <> '.':
              pict += picture[idx:idx+1]
              idx  += 1
        idx += 1
        while picture[idx:idx+1] == ' ':
              idx += 1
        while picture[idx:idx+1] <> ')' and \
              picture[idx:idx+1] <> ' ' and \
              picture[idx:idx+1] <> '.':
              tam += picture[idx:idx+1]
              idx += 1
        idx += 1
        while picture[idx:idx+1] == ' ':
              idx += 1
        qt9 = 0
        if  picture[idx:idx+1] == 'V':
            dec  = 'V'
            idx += 1
            qt9  = 0
            while picture[idx:idx+1] == '9' or \
                  picture[idx:idx+1] == '(' or \
                  picture[idx:idx+1] == ' ' or \
                  picture[idx:idx+1] == '.':
                  if  picture[idx:idx+1] == '9':
                      qt9 += 1
                  idx += 1
            if  picture[idx:idx+1] <> 'U' and \
                picture[idx:idx+1] <> '.':
                while picture[idx:idx+1] <> ')' and \
                      picture[idx:idx+1] <> ' ' and \
                      picture[idx:idx+1] <> ''  and \
                      picture[idx:idx+1] <> '.':
                      dec += picture[idx:idx+1]
                      idx += 1
        if  dec == 'V': dec = ''
        if  dec <> '' and (dec[1:] >= '0' and dec[1:] <= '9'):
            inteiro  = int(tam)
            decimais = int(dec[1:])
            tam      = str(int(tam) + int(dec[1:]))
        else:
            inteiro  = int(tam)
            decimais = qt9
        tam    += dec
        tipo    = ''
        idxtipo = picture.find(' COMP')
        if  idxtipo > -1:
            idxtipo += 1
            while picture[idxtipo:idxtipo+1] <> ' ' and \
                  picture[idxtipo:idxtipo+1] <> '.':
                  tipo    += picture[idxtipo:idxtipo+1]
                  idxtipo += 1
        if  redefines:
            posdic[cpo] = posicao = posdic[redefines] + 1
        else:
            posdic[cpo] = posicao
        nbytes = 0
        if  not redefines:
            if  pict == '9':
                if  tipo.find('COMP-3') > -1:
                    nbytes   = (((inteiro + decimais) / 2) + 1)
                    posicao += nbytes
                elif  tipo.find('COMP') > -1:
                    if  inteiro < 5:
                        posicao += 2
                        nbytes   = 2
                    elif  inteiro < 10:
                          posicao += 4
                          nbytes   = 4
                    else:
                        posicao += 8
                        nbytes   = 8
                else:
                    nbytes   = inteiro + decimais
                    posicao += nbytes
            else:
                nbytes   = inteiro
                posicao += nbytes
        db(db.booksCampos.insert(book=rowbook.id, nome=cpo, \
            nivel=nivel, natureza=pict, posicao=posdic[cpo], \
                picture=picts, tamanho=tam, inteiro=inteiro, \
                    decimais=decimais if decimais else 0, tipo=tipo, \
                        bytes=nbytes, redefines=redefines, \
                            itemGrupo=cpox, occurs=occurs, \
                                usuarioConfirmacao=user, \
                                    dataConfirmacao=datetime.datetime.\
                                        today()))

    return {'retorno': True, 'flash': flash, 'labelErrors': labelErrors, \
                             'msgsErrors': msgsErrors}

def imgtb(argv1, argv2, argv3):

    try:

        with open(argv3, 'w') as f1:

            with open(argv1)  as f2:

                for line in f2:
                    for tb in argv2:
                        line = line.replace(tb[0], tb[1])
                    f1.write(line)

    except:
        return traceback.format_exc()

def gerarimgtb(db, idimgtb, folder, user):

    parms               = db(db.parametros.id==1).select().first()
    regimgtb            = db(db.imgtbs.id==idimgtb).select().first()
    aplicacao           = db(db.aplicacoes.id==regimgtb.codigoAplicacao).\
                                                           select().first()
    nomeaplicacao       = aplicacao.aplicacao
    sistema             = nomeaplicacao + ' - ' + aplicacao.descricao
    author              = aplicacao.analista
    regempresa          = db(db.empresa.id==aplicacao.empresa).select().\
                                                                    first()
    regentidade         = db(db.entidades.id==regimgtb.codigoEntidade).\
                                                           select().first()

    regcolunasEntidades = ColunasEntidades.ColunasEntidades(db).\
                          selectColunasEntidadesResolvidasByCodigoEntidade(
                                                    regimgtb.codigoEntidade)[1]

    templates = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'Template'
                            , 'IMGTB') + os.sep

    gerimgtb      = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'IMGTB') + os.sep

    gercpy       = os.path.join( '\\\\'
                               , '127.0.0.1'
                               , 'c$'
                               , parms.raiz
                               , regempresa.nome
                               , nomeaplicacao
                               , 'GERADOS'
                               , 'CPY') + os.sep

    try:
        os.makedirs(gerimgtb)
    except:
        pass

    try:
        os.makedirs(gercpy)
    except:
        pass

    descrs = '* '
    idx    = 0

    for regto in regcolunasEntidades:
        if  idx < 1:
            descrs += '{:<28}'.format(regimgtb.bookName + '-' + \
                            regto.colunas.columnName.replace('_','-')) + \
                                ' = ' + \
                      '{:<31}'.format(utl.txtAbrev(r'%s' % \
                            regto.colunas.attributeName, 31).upper()) + ' *'
        else:
            descrs += '\n' + '      * ' + '{:<28}'.\
                            format(regimgtb.bookName + '-' + \
                regto.colunas.columnName.replace('_','-')) + \
                        ' = ' + '{:<31}'.format(utl.txtAbrev(r'%s' % \
                        regto.colunas.attributeName, 31).upper()) + ' *'
        idx += 1

    imagems = ''

    for regto in regcolunasEntidades:
        if  not regto.colunasEntidades.ehNotNull:
            texcoluna = regimgtb.bookName + '-' + regto.colunas.columnName.\
                        replace('_','-')
            if (len(texcoluna) + 5) > 30:
                if  texcoluna[24:25] == '-':
                    texcoluna = texcoluna[0:24] + '-NULL'
                else:
                    texcoluna = texcoluna[0:25] + '-NULL'
            else:
                texcoluna = texcoluna + '-NULL'
            tamcoluna = len(texcoluna)
            if  tamcoluna > 28:
                imagems += ('\n' + utl.repeat(' ', 14) if imagems else '')  + \
                                '10 ' + texcoluna
                imagems += '\n'  + utl.repeat(' ', 45)  + \
                                ' PIC  X(0001).'
            else:
                imagems += ('\n' + utl.repeat(' ', 14) if imagems else '')  + \
                                '10 ' + \
                                '{:<28}'.format(texcoluna) + \
                                ' PIC  X(0001).'
        if  regto.datatypes.picture_cobol == '9':
            picture = 'S9(' + '{:>04}'.format(regto.colunas.tamanhoColuna -
                                              regto.colunas.decimais) + ')'
            if  regto.colunas.decimais == 0:
                picture += ' COMP-3.'
            else:
                picture += 'V9(' + '{:>02}'.format(regto.colunas.decimais) + \
                                   ')' + ' COMP-3.'
        else:
            picture = ' X(' + '{:>04}'.format(regto.colunas.tamanhoColuna) + ').'
        if  regto.datatypes.datatype == '-9'  or \
            regto.datatypes.datatype == '-15' or \
            regto.datatypes.datatype == '12':
            texcolunal = regimgtb.bookName + '-' + \
                            regto.colunas.columnName.replace('_','-')
            if (len(texcolunal) + 4) > 30:
                if  texcolunal[25:26] == '-':
                    texcolunal = texcolunal[0:25] + '-LEN'
                else:
                    texcolunal = texcolunal[0:26] + '-LEN'
            else:
                texcolunal = texcolunal + '-LEN'
            texcolunat = regimgtb.bookName + '-' + regto.colunas.columnName.\
                         replace('_','-')
            if (len(texcolunat) + 5) > 30:
                if  texcolunat[24:25] == '-':
                    texcolunat = texcolunat[0:24] + '-TEXT'
                else:
                    texcolunat = texcolunat[0:25] + '-TEXT'
            else:
                texcolunat = texcolunat + '-TEXT'
            tamcoluna = len(texcolunat)
            imagems  += '\n' + utl.repeat(' ', 14) + '10 ' + \
                            regimgtb.bookName + '-' + \
                            regto.colunas.columnName.replace('_','-') + '.'
            if  tamcoluna > 25:
                imagems += ('\n' + utl.repeat(' ', 17) if imagems else '') + \
                                ' 15 '  + texcolunal
                imagems += '\n'         + utl.repeat(' ', 45)   + \
                                ' PIC S9(0004) COMP.'
                imagems += '\n'         + utl.repeat(' ', 17)   + \
                                ' 15 '  + texcolunat
                imagems += '\n'         + utl.repeat(' ', 45)   + \
                                ' PIC ' + picture
            else:
                imagems += ('\n' + utl.repeat(' ', 17) if imagems else '') + \
                                ' 15 '  + \
                                '{:<25}'.format(texcolunal) + \
                                ' PIC S9(0004) COMP.'
                imagems += '\n'         + utl.repeat(' ', 17)   + \
                                ' 15 '  + \
                                '{:<25}'.format(texcolunat) + \
                                ' PIC ' + picture
        else:
            texcoluna = regimgtb.bookName + '-' + \
                                      regto.colunas.columnName.replace('_','-')
            tamcoluna = len(texcoluna)
            if  tamcoluna > 28:
                imagems += ('\n' + utl.repeat(' ', 14) if imagems else '') + \
                                '10 '  + texcoluna
                imagems += '\n'  + utl.repeat(' ', 45)  + \
                                ' PIC ' + picture
            else:
                imagems += ('\n' + utl.repeat(' ', 14) if imagems else '') + \
                                '10 '  + \
                                '{:<28}'.format(texcoluna) + \
                                ' PIC ' + picture

    now = date.today().strftime('%d/%m/%Y')

    db(db.imgtbs.id==idimgtb).update(usuarioGeracao=user, \
                                         dataGeracao=datetime.datetime.today())

    txt = '%s%s.cpy' % (gercpy, regimgtb.bookName)

    erros = gerarcpy(txt, imagems)

    if  erros:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento Imagem Tabela'
        msgsErrors  = {}
        idx         = 0
        for erro in erros.split('\n'):
            if  len(erro) > 1:
                idx += 1
                msgsErrors[idx] = erro
        return {'retorno': False, 'flash': flash, \
                'labelErrors': labelErrors, 'msgsErrors': msgsErrors}

    db.booksTxt.insert(codigoAplicacao=regimgtb.codigoAplicacao, \
                       nome=regimgtb.bookName, \
                       arquivo=txt, \
                       nomeExtenso=txt, status=2, \
                       mensagem='Pendente de Processamento.', \
                       usuarioConfirmacao=user,
                       dataConfirmacao=datetime.datetime.today())

    flash       = 'Imagem da Tabela gerado com sucesso.'
    labelErrors = 'Resultado da geracao da Imagem da Tabela'
    msgsErrors  = {}
    idbook      = db((db.booksTxt.nomeExtenso==txt) &
                     (db.booksTxt.status==2)).select().first()

    if  idbook:
        imp = booksImport([idbook.id], db, folder, \
                                                regimgtb.codigoAplicacao, user)
        if  imp['retorno']:
            msgsErrors[0] = 'Book %s - Done.' % regimgtb.bookName
        length = lreclBook(db, 'booksCampos', 'book', imp['id'])
        tpl = '%sIMAGEM_TABELA.txt' % templates
        tb  = [['@BOOKSNAME',      regimgtb.bookName],
               ['@BOOKNAME',       '{:<49}'.format(regimgtb.bookName)],
               ['@TABLENAME',      '{:<32}'.format('(%s) %s' % \
                       (regentidade.nomeExterno, regentidade.nomeFisico))],
               ['@MES',            '{:<02}'.format(now[3:5])],
               ['@ANO',            '{:<44}'.format(now[6:])],
               ['@EMPRESA',        '{:<49}'.format(regempresa.descricao.\
                                                                 upper())],
               ['@AUTHOR',         '{:<49}'.format(author.upper())],
               ['@SISTEMA',        '{:<49}'.format(utl.\
                                        remover_acentos(sistema).upper())],
               ['@LENGTH',         '{:>04}'.format(length)],
               ['@CAMPO_DESCRICAO', descrs],
               ['@IMAGEMS',         imagems]]
        txt = '%s%s.cpy' % (gerimgtb, regimgtb.bookName)
        erros = imgtb(tpl, tb, txt)
        if  erros:
            flash       = 'Falha na Execução'
            labelErrors = 'Resultado do processamento Imagem Tabela'
            msgsErrors  = {}
            idx         = 0
            for erro in erros.split('\n'):
                if  len(erro) > 1:
                    idx += 1
                    msgsErrors[idx] = erro
            return {'retorno': False, 'flash': flash, \
                                      'labelErrors': labelErrors, \
                                      'msgsErrors': msgsErrors}
    else:
        msgsErrors[0] = 'Book %s - Done.'               % regimgtb.bookName
        msgsErrors[1] = \
          'Book %s - Erro na importacao para booksTxt.' % regimgtb.bookName

    return {'retorno': True, 'flash': flash, \
                             'labelErrors': labelErrors, \
                             'msgsErrors':  msgsErrors}

def gerarcpy(txt, lines):

    try:

        with open(txt, 'w') as f1:

            idx = 0

            for line in lines.split('\n'):
                idx += 1
                f1.write(('\n' if idx > 1 else '') + line)

    except:
        return traceback.format_exc()

def hpu(argv1, argv2, argv3, job=False, step=''):

    li = ''

    try:
        if  job:
            with open(argv1)  as f2:
                for line in f2:
                    for tb in argv2:
                        line = line.replace(tb[0], tb[1])
                    li += line
            return {'erros': '', 'linhas': li}
        else:
            with open(argv3, 'w') as f1:
                with open(argv1)  as f2:
                    for line in f2:
                        for tb in argv2:
                            line = line.replace(tb[0], tb[1])
                        f1.write(line)
                        li += line
            return {'erros': '', 'linhas': li}
    except:
        return {'erros': traceback.format_exc(), 'linhas': ''}

def gerarhpu(db, idhpu, user, job=False, step=''):

    parms  = db(db.parametros.id==1).select().first()
    reghpu = db(db.hpus.id==idhpu).select().first()

    if  not reghpu:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento HPU'
        if  step:
            msgsErrors  = {1: '%s do HPU nao definido.' % step}
        else:
            msgsErrors  = {1: 'HPU nao definido.'}
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': ''}

    aplicacao           = db(db.aplicacoes.id==reghpu.codigoAplicacao).\
                                                               select().first()
    nomeaplicacao       = aplicacao.aplicacao
    regempresa          = db(db.empresa.id==aplicacao.empresa).select().first()
    regentidade         = db(db.entidades.id==reghpu.codigoEntidade).\
                                                               select().first()

    templates = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'Template'
                            , 'JCL') + os.sep
    gerhpu    = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.raiz
                            , regempresa.nome
                            , nomeaplicacao
                            , 'GERADOS'
                            , 'HPU') + os.sep
    try:
        os.makedirs(gerhpu)
    except:
        pass

    regsysin = db(db.sysin.hpus==idhpu).select().first()

    sysin    = ''
    sqx      = '' if not regsysin.sql else regsysin.sql.replace('\r', '')

    if  regsysin:
        if  not regsysin.nome1:
            sysin += '//SYSIN    DD *'
            sysin += '\nUNLOAD TABLESPACE @TABLEHEADER.@TABLESPACE'
            sysin += '\nDB2 NO'
            sysin += '\nQUIESCE YES'
            sysin += '\n@SELECT'
            sysin += '\nOUTDDN (SYSREC01)'
            sysin += '\nFORMAT DSNTIAUL'
            sysin += '\nLOADDDN SYSPUNCH'
        else:
            if  regsysin.nome1 == '*':
                sysin += 'DSN=%s,' % (regsysin.nome1 + '.' + \
                                      regsysin.nome2 + '.' + \
                                      regsysin.nome3)
            else:
                nome2 = (reghpu.jobRotine + 'S' + '{:>02}'.\
                                                format(step.split('STEP')[1]))\
                                                    if step else regsysin.nome2
                sysin += 'DSN=AD.C87.%s.%s%s,' % (regsysin.nome1.upper(), \
                                                                       nome2, \
                                               ('.' + regsysin.nome3.upper()) \
                                                     if regsysin.nome3 else '')
            sysin += '\n//       DISP=SHR'
    else:
        sysin += '//SYSIN    DD *'
        sysin += '\nUNLOAD TABLESPACE @TABLEHEADER.@TABLESPACE'
        sysin += '\nDB2 NO'
        sysin += '\nQUIESCE YES'
        sysin += '\n@SELECT'
        sysin += '\nOUTDDN (SYSREC01)'
        sysin += '\nFORMAT DSNTIAUL'
        sysin += '\nLOADDDN SYSPUNCH'

    stp   = regsysin.nome2 if not step \
                           else ('S' + '{:>02}'.format(step.split('STEP')[1]))

    rot   = reghpu.jobRotine + (stp if stp else ('S' +
                             '{:>02}'.format(reghpu.jobStep.split('STEP')[1])))

    tb    = [['@JOBNAME',     reghpu.jobName.upper()],
             ['@ROTINA',      rot],
             ['@APPLID',      nomeaplicacao[0:5].upper()],
             ['@USER',        reghpu.jobUser.upper()],
             ['@STEP',        step if step           else reghpu.jobStep \
                                   if reghpu.jobStep else 'STEP1'],
             ['@SYSIN',       sysin],
             ['@SELECT',      sqx],
             ['@TABLEUID',    regentidade.nomeExterno[0:4]+'A000'],
             ['@TABLEHEADER', regentidade.nomeExterno[0:4]+'D000'],
             ['@TABLESPACE',  regentidade.nomeExterno.replace('B','S')],
             ['@TABLENAME',   regentidade.nomeExterno],
             ['@TABLE',       regentidade.nomeFisico]]

    txt = '%s%s.jcl' % (gerhpu, reghpu.jobName)

    if  job:
        tpl = '%sJOB_HPU_SYSIN_CARTAO.txt' % templates
    else:
        tpl = '%sHPU_SYSIN_CARTAO.txt'     % templates

    ghpu = hpu(tpl, tb, txt, job, step)

    if  ghpu['erros']:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento HPU%s' % \
                                               (' - %s' % step) if step else ''
        msgsErrors  = {}
        idx         = 0
        for erro in ghpu['erros'].split('\n'):
            if  len(erro) > 1:
                idx += 1
                msgsErrors[idx] = erro
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': ghpu['linhas']}

    db(db.hpus.id==idhpu).update(usuarioGeracao=user, \
                                         dataGeracao=datetime.datetime.today())

    flash         = 'HPU gerado com sucesso.'
    labelErrors   = 'Resultado da geracao do HPU'
    msgsErrors    = {}
    msgsErrors[0] = 'JOB %s - Done.' % reghpu.jobName

    return {'retorno': True, 'flash': flash, \
                             'labelErrors': labelErrors, \
                              'msgsErrors': msgsErrors, \
                                  'linhas': ghpu['linhas']}

def progckrs(argv1, argv2, argv3, job=False, step=''):

    li = ''

    try:
        if  job:
            with open(argv1)  as f2:
                for line in f2:
                    for tb in argv2:
                        line = line.replace(tb[0], tb[1])
                    li += line
            return {'erros': '', 'linhas': li}
        else:
            with open(argv3, 'w') as f1:
                with open(argv1)  as f2:
                    for line in f2:
                        for tb in argv2:
                            line = line.replace(tb[0], tb[1])
                        f1.write(line)
                        li += line
            return {'erros': '', 'linhas': li}
    except:
        return {'erros': traceback.format_exc(), 'linhas': ''}

def gerarckrs(db, idprog, user, job=False, step=''):

    parms   = db(db.parametros.id==1).select().first()
    regprog = db(db.progckrs.id==idprog).select().first()

    if  not regprog:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento Programa (CKRS)'
        if  step:
            msgsErrors  = {1: '%s do Programa nao definido.' % step}
        else:
            msgsErrors  = {1: 'Programa nao definido.'}
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': ''}

    aplicacao           = db(db.aplicacoes.id==regprog.codigoAplicacao).\
                                select().first()
    nomeaplicacao       = aplicacao.aplicacao
    regempresa          = db(db.empresa.id==aplicacao.empresa).select().first()

    # Comentarios
    regprogckrs2        = db(db.progckrs2.progckrs==idprog).select()
    if  not regprogckrs2:
        flash   = 'Comentarios nao definidos%s' % \
                                               (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    # Entradas
    regprogckrs3        = db(db.progckrs3.progckrs==idprog).select()
    if  not regprogckrs3:
        flash   = 'Entradas nao definidas%s' % (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    # Saidas
    regprogckrs4        = db(db.progckrs4.progckrs==idprog).select()
    if  not regprogckrs4:
        flash   = 'Saidas nao definidas%s'  % (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    templates = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'Template'
                            , 'JCL') + os.sep
    gerprog   = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.raiz
                            , regempresa.nome
                            , nomeaplicacao
                            , 'GERADOS'
                            , 'PROGCKRS') + os.sep

    try:
        os.makedirs(gerprog)
    except:
        pass

    comentario = ''
    entrada    = ''
    saida      = ''

    for regsort2 in regprogckrs2:
        comentario += regsort2.comentario.replace('\n','').upper()

    for regsort3 in regprogckrs3:
        if  regsort3.nome2 == '*':
            entrada += '%s//%s DD DSN=%s,' % ('\n//*\n' if entrada else '', \
                                                      regsort3.nome1.upper(), \
                                                      regsort3.nome2 + '.'  + \
                                                      regsort3.nome3 + '.'  + \
                                                      regsort3.nome4)
        else:
            if  regsort3.nome2:
                nome2 = regsort3.nome2
            else:
                nome2 = (regprog.jobRotine + 'S' + '{:>02}'.\
                                                format(step.split('STEP')[1]))\
                                                    if step else regsort3.nome2
            entrada += '%s//%s DD DSN=AD.C87.%s.%s%s,' % ('\n//*\n' \
                                  if entrada else '', regsort3.nome1.upper(), \
                                               nome2, regsort3.nome3.upper(), \
                                               ('.' + regsort3.nome4.upper()) \
                                                     if regsort3.nome4 else '')
        entrada += '\n//       DISP=SHR'

    for regsort4 in regprogckrs4:
        lrecl       = lreclBook(db, db.booksCampos, 'book', \
                            regsort4.book)
        nome2       = (regprog.jobRotine + 'S' + '{:>02}'.\
                                                format(step.split('STEP')[1]))\
                                                    if step else regsort4.nome2
        saida      += '%s//%s DD DSN=AD.C87.%s.%s%s,' % ('\n//*\n' \
                                    if saida else '', regsort4.nome1.upper(), \
                                               nome2, regsort4.nome3.upper(), \
                                               ('.' + regsort4.nome4.upper()) \
                                                     if regsort4.nome4 else '')
        saida      += '\n//       DISP=(,CATLG,DELETE),'
        saida      += '\n//       UNIT=(DISCO,04),'
        saida      += '\n//       SPACE=(TRK,(005000,1000),RLSE),'
        saida      += '\n//       DCB=(AD.A,LRECL=%s,RECFM=FB)' % \
                                                         '{:>04}'.format(lrecl)

    if  not step:
        stp = 'S' + '{:>02}'.format(regprog.jobStep.split('STEP')[1])
    else:
        stp = 'S' + '{:>02}'.format(step.split('STEP')[1])

    rot   = regprog.jobRotine + stp

    comentario = utl.remover_acentos(comentario)

    tb    = [['@JOBNAME',    regprog.jobName.upper()],
             ['@ROTINA',     rot],
             ['@APPLID',     regprog.jobRotine[0:5].upper()],
             ['@USER',       regprog.jobUser.upper()],
             ['@STEP',        step if step            else regprog.jobStep \
                                   if regprog.jobStep else 'STEP1'],
             ['@PROGRAMA',   regprog.jobPrograma.upper()],
             ['@COMENTARIO', utl.stringList(comentario, 61, \
                             '//* ***    ')],
             ['@ENTRADA',    entrada],
             ['@SAIDA',      saida]]

    txt = '%s%s.jcl' % (gerprog, regprog.jobName)

    if  job:
        tpl = '%sJOB_PROGCKRS.txt' % templates
    else:
        tpl = '%sPROGCKRS.txt'     % templates

    gckrs = progckrs(tpl, tb, txt, job)

    if  gckrs['erros']:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento Programa (CKRS)%s' % \
                                               (' - %s' % step) if step else ''
        msgsErrors  = {}
        idx         = 0
        for erro in gckrs['erros'].split('\n'):
            if  len(erro) > 1:
                idx += 1
                msgsErrors[idx] = erro
        return {'retorno': False, 'flash': flash, \
                          'labelErrors': labelErrors, \
                           'msgsErrors': msgsErrors, \
                               'linhas': gckrs['linhas']}

    db(db.progckrs.id==idprog).update(usuarioGeracao=user, \
                                         dataGeracao=datetime.datetime.today())

    flash         = 'Programa (CKRS) gerado com sucesso.'
    labelErrors   = 'Resultado da geracao do JCL'
    msgsErrors    = {}
    msgsErrors[0] = 'JCL %s - Done.' % regprog.jobName

    return {'retorno': True, 'flash': flash, \
                             'labelErrors': labelErrors, \
                              'msgsErrors': msgsErrors, \
                                  'linhas': gckrs['linhas']}

def prognens(argv1, argv2, argv3, job=False, step=''):

    li = ''

    try:
        if  job:
            with open(argv1)  as f2:
                for line in f2:
                    for tb in argv2:
                        line = line.replace(tb[0], tb[1])
                    li += line
            return {'erros': '', 'linhas': li}
        else:
            with open(argv3, 'w') as f1:
                with open(argv1)  as f2:
                    for line in f2:
                        for tb in argv2:
                            line = line.replace(tb[0], tb[1])
                        f1.write(line)
                        li += line
            return {'erros': '', 'linhas': li}
    except:
        return {'erros': traceback.format_exc(), 'linhas': ''}

def gerarnens(db, idprog, user, job=False, step=''):

    parms   = db(db.parametros.id==1).select().first()
    regprog = db(db.prognens.id==idprog).select().first()

    if  not regprog:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento Programa'
        if  step:
            msgsErrors  = {1: '%s do Programa nao definido.' % step}
        else:
            msgsErrors  = {1: 'Programa nao definido.'}
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': ''}

    aplicacao           = db(db.aplicacoes.id==regprog.codigoAplicacao).\
                                select().first()
    nomeaplicacao       = aplicacao.aplicacao
    regempresa          = db(db.empresa.id==aplicacao.empresa).select().first()

    # Comentarios
    regprognens2        = db(db.prognens2.prognens==idprog).select()
    if  not regprognens2:
        flash   = 'Comentarios nao definidos%s' % \
                                               (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    # Entradas
    regprognens3        = db(db.prognens3.prognens==idprog).select()
    if  not regprognens3:
        flash   = 'Entradas nao definidas%s' % \
                                               (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    # Saidas
    regprognens4        = db(db.prognens4.prognens==idprog).select()
    if  not regprognens4:
        flash   = 'Saidas nao definidas%s' % (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    templates = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'Template'
                            , 'JCL') + os.sep
    gerprog   = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.raiz
                            , regempresa.nome
                            , nomeaplicacao
                            , 'GERADOS'
                            , 'PROGNENS') + os.sep

    try:
        os.makedirs(gerprog)
    except:
        pass

    comentario = ''
    entrada    = ''
    saida      = ''

    for regsort2 in regprognens2:
        comentario += regsort2.comentario.replace('\n','').upper()

    for regsort3 in regprognens3:
        if  regsort3.nome2 == '*':
            entrada    += '%s//%s DD DSN=%s,' % \
                                               ('\n//*\n' if entrada else '', \
                                                      regsort3.nome1.upper(), \
                                                      regsort3.nome2 + '.'  + \
                                                      regsort3.nome3 + '.'  + \
                                                      regsort3.nome4)
        else:
            if  regsort3.nome2:
                nome2 = regsort3.nome2
            else:
                nome2 = (regprog.jobRotine + 'S' + '{:>02}'.\
                                                format(step.split('STEP')[1]))\
                                                    if step else regsort3.nome2
            entrada    += '%s//%s DD DSN=AD.C87.%s.%s%s,' % ('\n//*\n' \
                                  if entrada else '', regsort3.nome1.upper(), \
                                               nome2, regsort3.nome3.upper(), \
                                               ('.' + regsort3.nome4.upper()) \
                                                     if regsort3.nome4 else '')
        entrada    += '\n//       DISP=SHR'

    for regsort4 in regprognens4:
        lrecl       = lreclBook(db, db.booksCampos, 'book', regsort4.book)
        nome2       = (regprog.jobRotine + 'S' + '{:>02}'.\
                                                format(step.split('STEP')[1]))\
                                                    if step else regsort4.nome2
        saida      += '%s//%s DD DSN=AD.C87.%s.%s.%s%s,' % ('\n//*\n' \
                                    if saida else '', regsort4.nome1.upper(), \
                                               nome2, regsort4.nome3.upper(), \
                                                      regsort4.nome4.upper(), \
                                               ('.' + regsort4.nome5.upper()) \
                                                     if regsort4.nome5 else '')
        saida      += '\n//       DISP=(,CATLG,DELETE),'
        saida      += '\n//       UNIT=(DISCO,04),'
        saida      += '\n//       SPACE=(TRK,(005000,1000),RLSE),'
        saida      += '\n//       DCB=(AD.A,LRECL=%s,RECFM=FB)' % \
                                                         '{:>04}'.format(lrecl)

    if  not step:
        stp = 'S' + '{:>02}'.format(regprog.jobStep.split('STEP')[1])
    else:
        stp = 'S' + '{:>02}'.format(step.split('STEP')[1])

    rot = regprog.jobRotine + stp

    comentario = utl.remover_acentos(comentario)

    tb    = [['@JOBNAME',    regprog.jobName.upper()],
             ['@ROTINA',     rot],
             ['@APPLID',     regprog.jobRotine[0:5].upper()],
             ['@USER',       regprog.jobUser.upper()],
             ['@STEP',        step if step            else regprog.jobStep \
                                   if regprog.jobStep else 'STEP1'],
             ['@PROGRAMA',   regprog.jobPrograma.upper()],
             ['@COMENTARIO', utl.stringList(comentario, 61, \
                             '//* ***    ')],
             ['@ENTRADA',    entrada],
             ['@SAIDA',      saida]]

    txt   = '%s%s.jcl' % (gerprog, regprog.jobName)

    if  job:
        tpl = '%sJOB_PROGNENS.txt' % templates
    else:
        tpl = '%sPROGNENS.txt'     % templates

    gnens = prognens(tpl, tb, txt, job, step)

    if  gnens['erros']:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento Programa%s' % \
                                               (' - %s' % step) if step else ''
        msgsErrors  = {}
        idx         = 0
        for erro in gnens['erros'].split('\n'):
            if  len(erro) > 1:
                idx += 1
                msgsErrors[idx] = erro
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': gnens['linhas']}

    db(db.prognens.id==idprog).update(usuarioGeracao=user, \
                                         dataGeracao=datetime.datetime.today())

    flash         = 'Programa gerado com sucesso.'
    labelErrors   = 'Resultado da geracao do JCL'
    msgsErrors    = {}
    msgsErrors[0] = 'JCL %s - Done.' % regprog.jobName

    return {'retorno': True, 'flash': flash, \
                             'labelErrors': labelErrors, \
                              'msgsErrors': msgsErrors, \
                                  'linhas': gnens['linhas']}

def sort1s(argv1, argv2, argv3, job=False, step=''):

    li = ''

    try:
        if  job:
            with open(argv1)  as f2:
                for line in f2:
                    for tb in argv2:
                        line = line.replace(tb[0], tb[1])
                    li += line
            return {'erros': '', 'linhas': li}
        else:
            with open(argv3, 'w') as f1:
                with open(argv1)  as f2:
                    for line in f2:
                        for tb in argv2:
                            line = line.replace(tb[0], tb[1])
                        f1.write(line)
                        li += line
            return {'erros': '', 'linhas': li}
    except:
        return {'erros': traceback.format_exc(), 'linhas': ''}

def gerarsort1s(db, idsrt, user, job=False, step=''):

    parms  = db(db.parametros.id==1).select().first()
    regsrt = db(db.sort1s.id==idsrt).select().first()

    if  not regsrt:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento SORT1S'
        if  step:
            msgsErrors  = {1: '%s do Sort nao definido.' % step}
        else:
            msgsErrors  = {1: 'Sort nao definido.'}
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': ''}

    aplicacao           = db(db.aplicacoes.id==regsrt.codigoAplicacao).\
                                select().first()
    nomeaplicacao       = aplicacao.aplicacao
    regempresa          = db(db.empresa.id==aplicacao.empresa).\
                                select().first()
    regentidade         = db(db.entidades.id==regsrt.codigoEntidade).\
                                select().first()
    regsort2s           = db(db.sort2s.codigoSort1s==idsrt).select()

    if  not regsort2s:
        flash   = 'Fields nao selecionados%s' % \
                                               (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    regsort3s           = db(db.sort3s.codigoSort1s==idsrt).select()

    templates = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'Template'
                            , 'JCL') + os.sep
    gersrt    = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.raiz
                            , regempresa.nome
                            , nomeaplicacao
                            , 'GERADOS'
                            , 'SORT1S') + os.sep
    try:
        os.makedirs(gersrt)
    except:
        pass

    classificacao = ''
    fields        = ''
    formato       = ''
    iguais        = True
    slant         = ''
    include       = ''

    lreclc        = lrecl(db, regsrt.codigoEntidade)

    idx           = 0

    for regsort2 in regsort2s:
        regcampo = db(db.colunas.id==regsort2.campo).select().first()
        sl       = startLength(db, regsrt.codigoEntidade, regsort2.campo)
        if  sl[1] <> slant and slant and iguais:
            iguais = False
        else:
            slant  = sl[1]
        if  idx < 1:
            fields        += '%s,%s' % (sl[0], 'A' \
                    if regsort2.ordem=='ASCENDENTE' else 'D')
            classificacao += regcampo.columnName
        else:
            fields        += ','  + '%s,%s' % (sl[0], 'A' \
                    if regsort2.ordem=='ASCENDENTE' else 'D')
            classificacao += ', ' + regcampo.columnName
        idx += 1

    if  iguais:
        fields  = fields.replace(',%s' % slant, '') + ')'
        formato = ',FORMAT=%s' % slant
    else:
        fields += ')' if fields else ''

    idxin = 0

    for regsort3 in regsort3s:
        regcampo = db(db.colunas.id==regsort3.campo).select().first()
        sl       = startLength(db, regsrt.codigoEntidade, regsort3.campo)
        if  regsort3.tipo == 'INCLUDE':
            if  not idxin:
                include += '%s,%s,%s' % (sl[0], regsort3.operacao,
                                                regsort3.valor)
            else:
                include += '%s,%s,%s' % (sl[0], regsort3.operacao,
                                                regsort3.valor)
            idxin += 1

    if  include:
        include    = 'OUTFIL INCLUDE=' + \
                        utl.stringList('(%s),FNAMES=SORTOUT' % \
                            include, 56, '                 ')

    if  not step:
        stp = 'S' + '{:>02}'.format(regsrt.jobStep.split('STEP')[1])
    else:
        stp = 'S' + '{:>02}'.format(step.split('STEP')[1])

    rot = regsrt.jobRotine[0:5] + stp

    tb  = [['@JOBNAME',       regsrt.jobName.upper()],
           ['@ROTINA',        rot],
           ['@APPLID',        nomeaplicacao[0:5]],
           ['@USER',          regsrt.jobUser],
           ['@STEP',          step if step           else regsrt.jobStep \
                                   if regsrt.jobStep else 'STEP1'],
           ['@ARQNAME',       regsrt.jobArqName],
           ['@CLASSIFICACAO', utl.stringList(classificacao, 61, \
                                                               '//* ***    ')],
           ['@TABLESPACE',    regentidade.nomeExterno[0:4]+'S000'],
           ['@TABLENAME',     regentidade.nomeExterno],
           ['@TABLE',         regentidade.nomeFisico],
           ['@FIELDS',        utl.stringList(fields + formato, 59, \
                                                            '              ')],
           ['@INCLUDE',       ('\n ' if include else '') + include],
           ['@LRECL',         '{:>04}'.format(lreclc)]]

    txt = '%s%s.jcl' % (gersrt, regsrt.jobName)

    if  job:
        tpl = '%sJOB_SORT1S.txt' % templates
    else:
        tpl = '%sSORT1S.txt'     % templates

    gs1s = sort1s(tpl, tb, txt, job, step)

    if  gs1s['erros']:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento SORT1S%s' % \
                                               (' - %s' % step) if step else ''
        msgsErrors  = {}
        idx         = 0
        for erro in gs1s['erros'].split('\n'):
            if  len(erro) > 1:
                idx += 1
                msgsErrors[idx] = erro
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': gs1s['linhas']}

    db(db.sort1s.id==idsrt).update(usuarioGeracao=user, \
                                         dataGeracao=datetime.datetime.today())

    flash         = 'SORT1S gerado com sucesso.'
    labelErrors   = 'Resultado da geracao do SORT'
    msgsErrors    = {}
    msgsErrors[0] = 'JOB %s - Done.' % regsrt.jobName

    return {'retorno': True, 'flash': flash, \
                             'labelErrors': labelErrors, \
                              'msgsErrors': msgsErrors, \
                                  'linhas': gs1s['linhas']}

def sortnens(argv1, argv2, argv3, job=False, step=''):

    li = ''

    try:
        if  job:
            with open(argv1)  as f2:
                for line in f2:
                    for tb in argv2:
                        line = line.replace(tb[0], tb[1])
                    li += line
            return {'erros': '', 'linhas': li}
        else:
            with open(argv3, 'w') as f1:
                with open(argv1)  as f2:
                    for line in f2:
                        for tb in argv2:
                            line = line.replace(tb[0], tb[1])
                        f1.write(line)
                        li += line
            return {'erros': '', 'linhas': li}
    except:
        return {'erros': traceback.format_exc(), 'linhas': ''}

def gerarsortnens(db, idsrt, user, job=False, step=''):

    parms  = db(db.parametros.id==1).select().first()
    regsrt = db(db.sortnens.id==idsrt).select().first()

    if  not regsrt:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento SORTNENS'
        if  step:
            msgsErrors  = {1: '%s do Sort nao definido.' % step}
        else:
            msgsErrors  = {1: 'Sort nao definido.'}
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': ''}

    aplicacao           = db(db.aplicacoes.id==regsrt.codigoAplicacao).\
                                                               select().first()
    nomeaplicacao       = aplicacao.aplicacao
    regempresa          = db(db.empresa.id==aplicacao.empresa).select().first()
    regsortnens2        = db(db.sortnens2.sortnens==idsrt).select() # Fields

    if  not regsortnens2:
        flash   = 'Fields nao definidos%s' % (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    regsortnens3        = db(db.sortnens3.sortnens==idsrt).select() # Sortin

    if  not regsortnens3:
        flash   = 'Sortin nao definido%s' % (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    regsortnens4        = db(db.sortnens4.sortnens==idsrt).select() # Sortout

    if  not regsortnens4:
        flash   = 'Sortout nao definido%s' % (' - %s' % step) if step else ''
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': '', 'msgsErrors': {}}

    qtdSortout = db(db.sortnens4.sortnens==idsrt).count()

    if  qtdSortout > 1:
        temInclude = True
        sortout    = ''
        for regto in regsortnens4:
            reginclude  = db(db.sortnens5.sortnens4==regto.id).select()
            if  not reginclude:
                sortout    = regto.nome1 + ' - ' + regto.nome2
                temInclude = False
                break
        if  not temInclude:
            flash  = 'Include nao definido para o Sortout %s%s' % (sortout , \
                                              (' - %s' % step) if step else '')
            return {'retorno': False, 'flash': flash, \
                                      'labelErrors': '', 'msgsErrors': {}}


    templates = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'Template'
                            , 'JCL') + os.sep
    gersrt    = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.raiz
                            , regempresa.nome
                            , nomeaplicacao
                            , 'GERADOS'
                            , 'SORTNENS') + os.sep

    try:
        os.makedirs(gersrt)
    except:
        pass

    classificacao = ''
    sortin        = ''
    sysout        = ''
    fields        = ''
    formato       = ''
    iguais        = True
    slant         = ''
    include       = ''
    incl          = ''
    lrecl         = lreclBook(db, db.booksCampos, 'book', regsrt.book)
    idx           = 0

    for regsort2 in regsortnens2:
        regcampo  = db(db.booksCampos.id==regsort2.campo).select().first()
        sl        = startLengthBook(db, db.booksCampos, 'book', \
                                        regsrt.book, regsort2.campo)
        if  sl[1] <> slant and slant and iguais:
            iguais = False
        else:
            slant  = sl[1]
        if  idx < 1:
            fields        += '%s,%s' % (sl[0], 'A' \
                    if regsort2.ordem=='ASCENDENTE' else 'D')
            classificacao += regcampo.nome
        else:
            fields        += ','  + '%s,%s' % (sl[0], 'A' \
                    if regsort2.ordem=='ASCENDENTE' else 'D')
            classificacao += ', ' + regcampo.nome
        idx += 1

    if  iguais:
        fields  = fields.replace(',%s' % slant, '') + ')'
        formato = ',FORMAT=%s' % slant
    else:
        fields += ')' if fields else ''

    idxin = 0

    for regsort3 in regsortnens3:
        if  regsort3.nome1 == '*':
            nome1 = (regsort3.nome1 + '.' + regsort3.nome2 + '.' + \
                                            regsort3.nome3)
        else:
            if  regsort3.nome1:
                nome1 = regsort3.nome1
            else:
                nome1 = (regsrt.jobRotine + 'S' + '{:>02}'.
                                                   format(step.split('STEP')[1]
                                 if step else regsrt.jobStep.split('STEP')[1]))
        if  not idxin:
            if  regsort3.nome1 == '*':
                sortin += '//SORTIN DD DSN=%s,' % nome1
            else:
                sortin += '//SORTIN DD DSN=AD.C87.%s.%s.%s%s,' % \
                                      (nome1, regsort3.nome2, regsort3.nome3, \
                                                       ('.' + regsort3.nome4) \
                                                     if regsort3.nome4 else '')
        else:
            if  regsort3.nome1 == '*':
                sortin += '\n//       DD DSN=%s,' % nome1
            else:
                sortin += '\n//       DD DSN=AD.C87.%s.%s.%s%s,' % \
                                      (nome1, regsort3.nome2, regsort3.nome3, \
                                                       ('.' + regsort3.nome4) \
                                                     if regsort3.nome4 else '')
        sortin += '\n//       DISP=SHR'
        idxin  += 1

    if  len(regsortnens4) == 1:
        nome1 = (regsrt.jobRotine + 'S' + '{:>02}'.format(step.split('STEP')[1]
                                 if step else regsrt.jobStep.split('STEP')[1]))
        sysout     += '//SORTOUT DD DSN=AD.C87.%s.SORT.%s%s,' % \
                                               (nome1, regsortnens4[0].nome1, \
                                                ('.' + regsortnens4[0].nome2) \
                                              if regsortnens4[0].nome2 else '')
        sysout     += '\n//       DISP=(,CATLG,DELETE),'
        sysout     += '\n//       UNIT=(DISCO,04),'
        sysout     += '\n//       SPACE=(TRK,(005000,1000),RLSE),'
        sysout     += '\n//       DCB=(AD.A,LRECL=@LRECL,RECFM=FB)'
    else:
        idxout = 1
        nome1  = (regsrt.jobRotine + 'S' + '{:>02}'.
                                                   format(step.split('STEP')[1]
                                 if step else regsrt.jobStep.split('STEP')[1]))
        for regsort4 in regsortnens4:
            sysout += '%s//SYSOUT%s DD DSN=AD.C87.%s.SORT.%s%s,' % \
                                                ('\n//*\n' if sysout else '', \
                                                     '{:>02}'.format(idxout), \
                                                       nome1, regsort4.nome1, \
                                                       ('.' + regsort4.nome2) \
                                                     if regsort4.nome2 else '')
            sysout += '\n//       DISP=(,CATLG,DELETE),'
            sysout += '\n//       UNIT=(DISCO,04),'
            sysout += '\n//       SPACE=(TRK,(005000,1000),RLSE),'
            sysout += '\n//       DCB=(AD.A,LRECL=@LRECL,RECFM=FB)'
            idxout += 1

    bn     = ''
    idxout = 1

    for regsort4 in regsortnens4:
        regsort5s = db(db.sortnens5.sortnens4==regsort4.id).select()
        if  not regsort5s:
            continue
        incl   = ''
        for regsort5 in regsort5s:
            regcampo  = db(db.booksCampos.id==regsort5.campo).select().first()
            sl        = startLengthBook(db, db.booksCampos, 'book', \
                            regsrt.book, regsort5.campo)
            if  regsort5.tipo == 'INCLUDE':
                incl += '%s%s,%s,%s' % (',' if incl else '', sl[0], \
                            regsort5.operacao, regsort5.valor)
        include      += ('%sOUTFIL INCLUDE=' % bn) + \
                            utl.stringList('(%s),FNAMES=%s%s' % \
                            (incl, 'SYSOUT' if qtdSortout > 1 else 'SORTOUT', \
                            '{:>02}'.format(idxout) \
                            if qtdSortout > 1 else ''), \
                            56, '                 ')
        idxout       += 1
        bn            = '\n '

    if  not step:
        stp = 'S' + '{:>02}'.format(regsrt.jobStep.split('STEP')[1])
    else:
        stp = 'S' + '{:>02}'.format(step.split('STEP')[1])

    rot   = regsrt.jobRotine + stp

    arqname = utl.remover_acentos(utl.stringList(\
                                             'CLASSIFICA O ARQUIVO %s POR:' % \
                                 regsrt.jobArqName, 61, '//* ***    ')).upper()

    classificacao = utl.remover_acentos(classificacao).upper()

    tb    = [['@JOBNAME',       regsrt.jobName.upper()],
             ['@ROTINA',        rot],
             ['@APPLID',        nomeaplicacao[0:5]],
             ['@USER',          regsrt.jobUser],
             ['@STEP',          step if step           else regsrt.jobStep \
                                     if regsrt.jobStep else 'STEP1'],
             ['@ARQNAME',       arqname],
             ['@CLASSIFICACAO', utl.stringList(classificacao, 61, \
                                         '//* ***    ')],
             ['@SORTIN',        sortin],
             ['@SYSOUT',        sysout],
             ['@FIELDS',        utl.stringList(fields + \
                                         formato, 59, '              ')],
             ['@INCLUDE',       ('\n ' if include else '') + include],
             ['@LRECL',         '{:>04}'.format(lrecl)]]

    txt = '%s%s.jcl' % (gersrt, regsrt.jobName)

    if  job:
        tpl = '%sJOB_SORTNENS.txt' % templates
    else:
        tpl = '%sSORTNENS.txt'     % templates

    gsns = sortnens(tpl, tb, txt, job, step)

    if  gsns['erros']:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento SORTNENS%s' % \
                                               (' - %s' % step) if step else ''
        msgsErrors  = {}
        idx         = 0
        for erro in gsns['erros'].split('\n'):
            if  len(erro) > 1:
                idx += 1
                msgsErrors[idx] = erro
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors, \
                                       'linhas': gsns['linhas']}

    db(db.sortnens.id==idsrt).update(usuarioGeracao=user, \
                                     dataGeracao=datetime.datetime.today())

    flash         = 'SORTNENS gerado com sucesso.'
    labelErrors   = 'Resultado da geracao do SORT'
    msgsErrors    = {}
    msgsErrors[0] = 'JOB %s - Done.' % regsrt.jobName

    return {'retorno': True, 'flash': flash, \
                             'labelErrors': labelErrors, \
                              'msgsErrors': msgsErrors, \
                                  'linhas': gsns['linhas']}

def job(argv1, argv2, argv3):

    try:

        with open(argv3, 'w') as f1:

            with open(argv1)  as f2:

                for line in f2:
                    for tb in argv2:
                        line = line.replace(tb[0], tb[1])
                    f1.write(line)

    except:
        return traceback.format_exc()

def gerarJob(db, idjob, user):

    parms         = db(db.parametros.id==1).select().first()
    regjob        = db(db.jobs.id==idjob).select().first()
    regsteps      = db(db.jobsteps.job==idjob).select(orderby='sequencia')
    aplicacao     = db(db.aplicacoes.id==regjob.codigoAplicacao).\
                                                               select().first()
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select().first()

    if  not regsteps:
        flash = 'Steps nao definidos'
        return {'retorno': False, 'flash': flash, 'labelErrors': '', \
                                  'msgsErrors': {}}

    templates = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'Template'
                            , 'JCL') + os.sep
    gerjob    = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.raiz
                            , regempresa.nome
                            , nomeaplicacao
                            , 'GERADOS'
                            , 'JOBS') + os.sep

    try:
        os.makedirs(gerjob)
    except:
        pass

    jobs = ''

    for regstep in regsteps:
        if  regstep.objeto == 'HPU':
            obj = gerarhpu(db, regstep.idObjeto, user, job=True, \
                                                             step=regstep.step)
            if  not obj['retorno']:
                return {'retorno': False, 'flash': obj['flash'], \
                                          'labelErrors': obj['labelErrors'], \
                                           'msgsErrors': obj['msgsErrors']}

            jobs += obj['linhas']
            continue
        if  regstep.objeto == 'Programa':
            obj = gerarnens(db, regstep.idObjeto, user, job=True, \
                                                             step=regstep.step)
            if  not obj['retorno']:
                return {'retorno': False, 'flash': obj['flash'], \
                                          'labelErrors': obj['labelErrors'], \
                                           'msgsErrors': obj['msgsErrors']}

            jobs += obj['linhas']
            continue
        if  regstep.objeto == 'Programa (CKRS)':
            obj = gerarckrs(db, regstep.idObjeto, user, job=True, \
                                                             step=regstep.step)
            if  not obj['retorno']:
                return {'retorno': False, 'flash': obj['flash'], \
                                          'labelErrors': obj['labelErrors'], \
                                           'msgsErrors': obj['msgsErrors']}

            jobs += obj['linhas']
            continue
        if  regstep.objeto == 'Sort Tabela':
            obj = gerarsort1s(db, regstep.idObjeto, user, job=True, \
                                                             step=regstep.step)
            if  not obj['retorno']:
                return {'retorno': False, 'flash': obj['flash'], \
                                          'labelErrors': obj['labelErrors'], \
                                           'msgsErrors': obj['msgsErrors']}

            jobs += obj['linhas']
            continue
        if  regstep.objeto == 'Sort Arquivo':
            obj = gerarsortnens(db, regstep.idObjeto, user, job=True, \
                                                             step=regstep.step)
            if  not obj['retorno']:
                return {'retorno': False, 'flash': obj['flash'], \
                                          'labelErrors': obj['labelErrors'], \
                                           'msgsErrors': obj['msgsErrors']}

            jobs += obj['linhas']
            continue

    tb    = [['@JOBNAME', regjob.name], \
             ['@ROTINA',  regjob.rotine], \
             ['@APPLID',  regjob.rotine[0:4]], \
             ['@USER',    regjob.usuario],
             ['@STEPS',   jobs]]

    txt   = '%s%s.jcl'  % (gerjob, regjob.name)
    tpl   = '%sJOB.txt' % templates

    erros = job(tpl, tb, txt)

    if  erros:
        flash       = 'Falha na Execução'
        labelErrors = 'Resultado do processamento JOB'
        msgsErrors  = {}
        idx         = 0
        for erro in erros.split('\n'):
            if  len(erro) > 1:
                idx += 1
                msgsErrors[idx] = erro
        return {'retorno': False, 'flash': flash, \
                                  'labelErrors': labelErrors, \
                                   'msgsErrors': msgsErrors}

    db(db.jobs.id==idjob).update(usuarioGeracao=user, \
                                         dataGeracao=datetime.datetime.today())

    flash         = 'JOB gerado com sucesso.'
    labelErrors   = 'Resultado da geracao do JOB'
    msgsErrors    = {}
    msgsErrors[0] = 'JOB %s - Done.' % regjob.name

    return {'retorno': True, 'flash': flash, \
                             'labelErrors': labelErrors, \
                              'msgsErrors': msgsErrors}

def referback(db, idaplicacao, idstep, idcontroller, idobjeto):
    regstp = db(db.jobsteps.id==idstep).select().first()
    if  regstp.objeto == 'HPU':
        nome1 = 'nome1'
        nome2 = 'nome2'
        nome3 = 'nome3'
    elif  regstp.objeto == 'Programa':
        nome1 = 'nome2'
        nome2 = 'nome3'
        nome3 = 'nome4'
    elif  regstp.objeto == 'Programa (CKRS)':
        nome1 = 'nome2'
        nome2 = 'nome3'
        nome3 = 'nome4'
    elif  regstp.objeto == 'Sort Tabela':
        nome1 = 'nome2'
        nome2 = 'nome3'
        nome3 = 'nome4'
    else:
        nome1 = 'nome1'
        nome2 = 'nome2'
        nome3 = 'nome3'
    regsteps = db(db.jobsteps).select(orderby='job,step,sequencia')
    items    = ''
    rotina   = ''
    job      = 0
    step     = ''
    ocor     = 0
    qtde     = len(regsteps)
    for regstep in regsteps:
        ocor  += 1
        regjob = db(db.jobs.id==regstep.job).select().first()
        if  regjob.codigoAplicacao <> idaplicacao:
            continue
        if  regstep.job == int(session.idjob or 0) and (regstep.step == session.get('step', '') or regstep.sequencia > int(session.sequencia or 0)):
            continue
        if  regjob.rotine <> rotina:
            items += ('</ul></ul></ul><ul>' if items else '<ul>') + '<li>Rotina: %s</li>' % regjob.rotine
            rotina = regjob.rotine
            items += '<ul><li>Job: %s</li>' % regjob.name
            job    = regstep.job
            items += '<ul><li>%s - %s %s</li>' % (regstep.step, regstep.objeto, regstep.dsObjeto)
            step   = regstep.step
        else:
            if  regstep.job <> job:
                items += ('</ul><ul>' if items else '<ul>') + '<li>Job: %s</li>' % regjob.name
                job    = regstep.job
                items += '<ul><li>%s - %s %s</li>' % (regstep.step, regstep.objeto, regstep.dsObjeto)
                step   = regstep.step
            else:
                if  regstep.step <> step:
                    items += '%s<ul><li>%s - %s %s</li>' % ('<ul>' if ocor==qtde else '', regstep.step, regstep.objeto, regstep.dsObjeto)
                    step   = regstep.step
        if  regstep.objeto == 'HPU':
            reghpu = db(db.hpus.id==regstep.idObjeto).select().first()
            if  not reghpu:
                items += '<ul><li>Nenhuma saida definida</li></ul>'
            else:
                regent = db(db.tabelas.id==reghpu.codigoEntidade).select().first()
                items += '<ul>'
                dsname = 'SYSREC01 - AD.C87.%s.%s' % (regjob.rotine + 'S%s.HPU.SYSREC01' % regstep.sequencia, regent.nome)
                if  regstep.job == int(session.idjob or 0):
                    vlr1 = '*'
                    vlr2 = step
                    vlr3 = 'SYSREC01'
                    vlr4 = ''
                else:
                    vlr1 = regjob.rotine + 'S%s' % '{:>02}'.format(regstep.sequencia)
                    vlr2 = 'SYSREC01'
                    vlr3 = regent.nome
                    vlr4 = ''
                items += '<li>' + str(A(dsname, _style=XML('cursor: pointer'),
                           _onclick=XML("jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome1, vlr1) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome2, vlr2) +
                           "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome3, vlr3) +
                             ("jQuery('#%s_nome4').attr('value','%s');" %
                                                     (idcontroller, vlr4)
                           if  regstp.objeto == 'Sort Arquivo' else '') +
                           "jQuery('#referback_%s').text('');" % idobjeto)))
            items += '</li>'
            items += '</ul>'
        if  regstep.objeto == 'Programa':
            regnens  = db(db.prognens.id==regstep.idObjeto).select().first()
            if  not regnens:
                items += '<ul><li>Nenhuma saida definida</li></ul>'
            else:
                idx       = 0
                regnens4s = db(db.prognens4.prognens==regnens.id).select()
                for regnens4 in regnens4s:
                    idx   += 1
                    items += '<ul>'
                    dsname = '%s - AD.C87.%s%s%s%s' % \
                          (regnens4.nome1, regjob.rotine + 'S%s' % '{:>02}'.format(regstep.sequencia),
                          ('.' + regnens4.nome3) if regnens4.nome3 else '',
                          ('.' + regnens4.nome4) if regnens4.nome4 else '',
                          ('.' + regnens4.nome5) if regnens4.nome5 else '')
                    if  regstep.job == int(session.idjob or 0):
                        vlr1 = '*'
                        vlr2 = step
                        vlr3 = regnens4.nome1
                        vlr4 = ''
                    else:
                        vlr1 = regjob.rotine + 'S%s' % '{:>02}'.format(regstep.sequencia)
                        vlr2 = (regnens4.nome3) if regnens4.nome3 else ''
                        vlr3 = (regnens4.nome4) if regnens4.nome4 else ''
                        vlr4 = (regnens4.nome5) if regnens4.nome5 else ''
                    items += '<li>' + str(A(dsname, _style=XML('cursor: pointer'),\
                    _onclick=XML("jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome1, vlr1) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome2, vlr2) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome3, vlr3) +
                             ("jQuery('#%s_nome4').attr('value','%s');" %
                                                     (idcontroller, vlr4)
                           if  regstp.objeto == 'Sort Arquivo' else '') +
                          "jQuery('#referback_%s').text('');" % idobjeto)))
                    items += '</li>'
                    items += '</ul>'
                if  not idx:
                    items += '<ul><li>Nenhuma Saida definida</li></ul>'
        if  regstep.objeto == 'Programa (CKRS)':
            regckrs  = db(db.progckrs.id==regstep.idObjeto).select().first()
            if  not regckrs:
                items += '<ul><li>Nenhuma saida definida</li></ul>'
            else:
                idx       = 0
                regckrs4s = db(db.progckrs4.progckrs==regckrs.id).select()
                for regckrs4 in regckrs4s:
                    idx   += 1
                    items += '<ul>'
                    dsname = '%s - AD.C87.%s%s%s%s' % \
                          (regnens4.nome1, regjob.rotine + 'S%s' % '{:>02}'.format(regstep.sequencia),
                          ('.' + regckrs4.nome3) if regckrs4.nome3 else '',
                          ('.' + regckrs4.nome4) if regckrs4.nome4 else '',
                          ('.' + regckrs4.nome5) if regckrs4.nome5 else '')
                    if  regstep.job == int(session.idjob or 0):
                        vlr1 = '*'
                        vlr2 = step
                        vlr3 = regckrs4.nome1
                        vlr4 = ''
                    else:
                        vlr1 = regjob.rotine + 'S%s' % '{:>02}'.format(regstep.sequencia)
                        vlr2 = (regckrs4.nome3) if regckrs4.nome3 else ''
                        vlr3 = (regckrs4.nome4) if regckrs4.nome4 else ''
                        vlr4 = (regckrs4.nome5) if regckrs4.nome5 else ''
                    items += '<li>' + str(A(dsname, _style=XML('cursor: pointer'),
                    _onclick=XML("jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome1, vlr1) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome2, vlr2) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome3, vlr3) +
                             ("jQuery('#%s_nome4').attr('value','%s');" %
                                                     (idcontroller, vlr4)
                           if  regstp.objeto == 'Sort Arquivo' else '') +
                          "jQuery('#referback_%s').text('');" % idobjeto)))
                    items += '</li>'
                    items += '</ul>'
                if  not idx:
                    items += '<ul><li>Nenhuma Saida definida</li>'
        if  regstep.objeto == 'Sort Tabela':
            reg1s  = db(db.sort1s.id==regstep.idObjeto).select().first()
            if  not reg1s:
                items += '<ul><li>Nenhuma saida definida</li></ul>'
            else:
                regent = db(db.tabelas.id==reg1s.codigoEntidade).select().first()
                items += '<ul>'
                dsname = 'SORTOUT - AD.C87.%s%s%s' % (regjob.rotine + 'S%s.SORT' % '{:>02}'.format(regstep.sequencia), '.' + regent.nome, '.' + reg1s.jobArqName)
                if  regstep.job == int(session.idjob or 0):
                    vlr1 = '*'
                    vlr2 = step
                    vlr3 = 'SORTOUT'
                    vlr4 = ''
                else:
                    vlr1 = regjob.rotine
                    vlr2 = 'S%s.SORT' % '{:>02}'.format(regstep.sequencia)
                    vlr3 = regent.nome
                    vlr4 = reg1s.jobArqName
                items += '<li>' + str(A(dsname, _style=XML('cursor: pointer'),
                    _onclick=XML("jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome1, vlr1) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome2, vlr2) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome3, vlr3) +
                             ("jQuery('#%s_nome4').attr('value','%s');" %
                                                     (idcontroller, vlr4)
                           if  regstp.objeto == 'Sort Arquivo' else '') +
                          "jQuery('#referback_%s').text('');" % idobjeto)))
            items += '</li>'
            items += '</ul>'
        if  regstep.objeto == 'Sort Arquivo':
            regnens  = db(db.sortnens.id==regstep.idObjeto).select().first()
            if  not regnens:
                items += '<ul><li>Nenhuma saida definida</li></ul>'
            else:
                regnens4s = db(db.sortnens4.sortnens==regnens.id).select()
                idx       = 0
                for regnens4 in regnens4s:
                    idx   += 1
                    items += '<ul>'
                    origem = 'SYSOUT%s' % '{:>02}'.format(idx)
                    dsname = 'SYSOUT%s - AD.C87.%s%s%s' % ('{:>02}'.format(idx), regjob.rotine + 'S%s.SORT' % '{:>02}'.format(regstep.sequencia), '.' + regnens4.nome1, ('.' + regnens4.nome2) if regnens4.nome2 else '')
                    if  regstep.job == int(session.idjob or 0):
                        vlr1 = '*'
                        vlr2 = step
                        vlr3 = origem
                        vlr4 = ''
                    else:
                        vlr1 = regjob.rotine + 'S%s' % '{:>02}'.format(regstep.sequencia)
                        vlr2 = 'SORT'
                        vlr3 = regnens4.nome1
                        vlr4 = (regnens4.nome2) if regnens4.nome2 else ''
                    items += '<li>' + str(A(dsname, _style=XML('cursor: pointer'),
                    _onclick=XML("jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome1, vlr1) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome2, vlr2) +
                                 "jQuery('#%s_%s').attr('value','%s');" %
                                            (idcontroller, nome3, vlr3) +
                             ("jQuery('#%s_nome4').attr('value','%s');" %
                                                     (idcontroller, vlr4)
                           if  regstp.objeto == 'Sort Arquivo' else '') +
                          "jQuery('#referback_%s').text('');" % idobjeto)))
                    items += '</li>'
                    items += '</ul>'
                if  not idx:
                    items += '<ul><li>Nenhuma Saida definida</li></ul>'
        items += '</ul>'
    return XML(items)

# vim: ft=python
