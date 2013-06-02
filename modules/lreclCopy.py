
def lreclCopy(copy):

    linFile = copy.split('\n')

    regc = {}

    linhas = []

    for arq in linFile:

        if  arq != '' and arq[6: 7] != '*':

            linhas.append(arq.upper())

    while True:
        
        copy = False
        
        for li in linhas:
            
            if  li.find('COPY') > -1:
                
                copy = True
                
                break
            
        if  not copy: break
    
        idx = -1
        
        for li in linhas:
            
            idx += 1
            
            if  li.find('COPY') > -1:
                
                cols = li.split()
                
                book = cols[1].replace("'", '').replace('.', '')
                    
                msg = 'COPY {} deve ser expandido.'.format(book)
                
                return {'retorno': False, 'msg': msg, 'lrecl': 0}

    linhaf = ''
    redefines = ''
    posdic = {}
    idxFiller = 1
    idx = 0
    posicao = 1
    itemGrupo = []
    nivel = 0
    occurs = 0
    niveloccurs = 0
    idl = 0

    for li in linhas:
        
        if  li.find('.') < 0:
            
            linhaf += li.upper()
            
            continue
        
        linhaf += li.upper()
        
        linha = linhaf.split()
        
        idl += 1
        
        nivel = int(linha[0])
        
        campo = linha[1].replace('.', '')
        
        if  campo == 'FILLER':
            
            cpo = '%s_%s' % (campo, '{:>02}'.format(idxFiller))
            
            idxFiller += 1
            
        else:
            
            cpo = campo
            
        itemGrupo.append([nivel, cpo])
        
        cpox = ''
        
        for idx in xrange(idl - 1, 0, -1):
            
            if  itemGrupo[idx][0] < nivel:
                
                cpox = itemGrupo[idx][1]
                
                break
            
        if  linhaf.find('REDEFINES ') > -1 and linhaf.find('PIC ') < 0:
            
            redefines = linha[3].replace('.', '')
            
            posdic[cpo] = posicao = posdic[redefines]
            
            regc[cpo] = {}

            regc[cpo]['nivel': nivel]
            regc[cpo]['natureza': '']
            regc[cpo]['posicao': posdic[cpo]]
            regc[cpo]['picture': '']
            regc[cpo]['tamanho': 0]
            regc[cpo]['inteiro': 0]
            regc[cpo]['decimais': 0]
            regc[cpo]['tipo': '']
            regc[cpo]['bytes': 0]
            regc[cpo]['redefines': redefines]
            regc[cpo]['itemGrupo': cpox]
            regc[cpo]['occurs': occurs]
            
            linhaf = ''
            
            continue

        if  linhaf.find('REDEFINES ') > -1 and \
            linhaf.find('PIC ') > -1:
                
            picture = linha[5]
            picts = picture.replace('.', '')

            if  len(linha) > 6:

                if  len(linha) == 7:

                    picture += (' ' + linha[6])

                else:

                    for idx in xrange(6, len(linha) - 1):

                        if  linha[idx].upper() != 'VALUE':

                            picture += (' ' + linha[idx])

            picture = picture.replace('S', '')

            pict = ''
            inteiro = 0
            decimais = 0
            tam = ''
            dec = ''
            idx = 0

            while picture[idx:idx + 1] != '(' and \
                  picture[idx:idx + 1] != ' ' and \
                  picture[idx:idx + 1] != '.':

                pict += picture[idx:idx + 1]
                idx += 1

            idx += 1

            while picture[idx:idx + 1] == ' ':

                idx += 1

            while picture[idx:idx + 1] != ')' and \
                  picture[idx:idx + 1] != ' ' and \
                  picture[idx:idx + 1] != '.':
                tam += picture[idx:idx + 1]
                idx += 1

            idx += 1

            while picture[idx:idx + 1] == ' ':

                idx += 1

            if  picture[idx:idx + 1] == 'V':

                dec = 'V'
                idx += 1

                while picture[idx:idx + 1] == '9' or \
                      picture[idx:idx + 1] == '(' or \
                      picture[idx:idx + 1] == ' ' or \
                      picture[idx:idx + 1] == '.':

                    idx += 1

                if  picture[idx:idx + 1] != 'U' and \
                    picture[idx:idx + 1] != '.':

                    while picture[idx:idx + 1] != ')' and \
                          picture[idx:idx + 1] != ' ' and \
                          picture[idx:idx + 1] != '.':

                        dec += picture[idx:idx + 1]
                        idx += 1

            if  dec == 'V':

                dec = ''

            if  dec != '' and (dec[1:] >= '0' and dec[1:] <= '9'):

                inteiro = int(tam)
                decimais = int(dec[1:])
                tam = str(int(tam) + int(dec[1:]))

            else:

                inteiro = int(tam)
                decimais = 0

            tam += dec
            tipo = ''
            idxtipo = picture.find(' COMP')

            if  idxtipo > -1:

                idxtipo += 1

                while picture[idxtipo:idxtipo + 1] != ' ' and \
                      picture[idxtipo:idxtipo + 1] != '.':

                    tipo += picture[idxtipo:idxtipo + 1]

                    idxtipo += 1

            redefines = linha[3].replace('.', '')

            posdic[cpo] = posicao = posdic[redefines] + 1

            regc[cpo] = {}
            
            regc[cpo]['nivel'] = nivel
            regc[cpo]['natureza'] = pict
            regc[cpo]['posicao'] = posdic[cpo]
            regc[cpo]['picture'] = picts
            regc[cpo]['tamanho'] = tam
            regc[cpo]['inteiro'] = inteiro
            regc[cpo]['decimais'] = decimais if decimais else 0
            regc[cpo]['tipo'] = tipo
            regc[cpo]['bytes'] = 0
            regc[cpo]['redefines'] = redefines
            regc[cpo]['itemGrupo'] = cpox
            regc[cpo]['occurs'] = occurs

            linhaf = ''

            continue

        if  linhaf.find('OCCURS ') > -1:
            
            if  len(linha) == 4:
                
                occurs = int(linha[3].replace('.', ''))
                
            elif len(linha) == 5:
                
                occurs = int(linha[3].replace('.', ''))
                
            else:
                
                occurs = int(linha[5].replace('.', ''))
                
            niveloccurs = nivel
            
            posdic[cpo] = posicao
            
            regc[cpo] = {}
            
            regc[cpo]['nivel'] = nivel
            regc[cpo]['natureza'] = ''
            regc[cpo]['posicao'] = posdic[cpo]
            regc[cpo]['picture'] = ''
            regc[cpo]['tamanho'] = 0
            regc[cpo]['inteiro'] = 0
            regc[cpo]['decimais'] = 0
            regc[cpo]['tipo'] = ''
            regc[cpo]['bytes'] = 0
            regc[cpo]['redefines'] = ''
            regc[cpo]['itemGrupo'] = cpox
            regc[cpo]['occurs'] = occurs

            linhaf = ''

            continue

        if  linhaf.find('PIC ') < 0:
            
            posdic[cpo] = posicao
            

            regc[cpo] = {}

            regc[cpo]['nivel'] = nivel
            regc[cpo]['natureza'] = ''
            regc[cpo]['posicao'] = posdic[cpo]
            regc[cpo]['picture'] = ''
            regc[cpo]['tamanho'] = 0
            regc[cpo]['inteiro'] = 0
            regc[cpo]['decimais'] = 0
            regc[cpo]['tipo'] = ''
            regc[cpo]['bytes'] = 0
            regc[cpo]['redefines'] = ''
            regc[cpo]['itemGrupo'] = cpox
            regc[cpo]['occurs'] = occurs

            linhaf = ''

            continue

        if  occurs:
            
            if  nivel <= niveloccurs:
                
                occurs = 0
                
                niveloccurs = 0
                
        redefines = ''
        
        linhaf = ''
        
        picture = linha[3]
        
        picts = picture.replace('.', '')
        
        if  len(linha) > 4:
            
            if  len(linha) == 5:
                
                picture += (' ' + linha[4])
                
            else:
                
                for idx in xrange(4, len(linha) - 1):
                    
                    if  linha[idx].upper() != 'VALUE':
                        
                        picture += (' ' + linha[idx])
                        
        picture = picture.replace('S', '')
        
        pict = ''
        inteiro = 0
        decimais = 0
        tam = ''
        dec = ''
        idx = 0
        
        while picture[idx:idx + 1] != '(' and \
              picture[idx:idx + 1] != ' ' and \
              picture[idx:idx + 1] != '.':
                  
            pict += picture[idx:idx + 1]
            idx += 1
            
        idx += 1
        
        while picture[idx:idx + 1] == ' ':
            
            idx += 1
            
        while picture[idx:idx + 1] != ')' and \
              picture[idx:idx + 1] != ' ' and \
              picture[idx:idx + 1] != '.':
                  
            tam += picture[idx:idx + 1]
            idx += 1
            
        idx += 1
        
        while picture[idx:idx + 1] == ' ':
            
            idx += 1
            
        qt9 = 0
        
        if  picture[idx:idx + 1] == 'V':
            
            dec = 'V'
            idx += 1
            qt9 = 0
            
            while picture[idx:idx + 1] == '9' or \
                  picture[idx:idx + 1] == '(' or \
                  picture[idx:idx + 1] == ' ' or \
                  picture[idx:idx + 1] == '.':
                      
                if  picture[idx:idx + 1] == '9':
                    
                    qt9 += 1
                    
                idx += 1
                
            if  picture[idx:idx + 1] != 'U' and \
                picture[idx:idx + 1] != '.':
                    
                while picture[idx:idx + 1] != ')' and \
                      picture[idx:idx + 1] != ' ' and \
                      picture[idx:idx + 1] != '' and \
                      picture[idx:idx + 1] != '.':
                          
                    dec += picture[idx:idx + 1]
                    idx += 1
                    
        if  dec == 'V':
            
            dec = ''
            
        if  dec != '' and (dec[1:] >= '0' and dec[1:] <= '9'):
            
            inteiro = int(tam)
            decimais = int(dec[1:])
            
            tam = str(int(tam) + int(dec[1:]))
            
        else:
            
            inteiro = int(tam)
            decimais = qt9
            
        tam += dec
        tipo = ''
        idxtipo = picture.find(' COMP')
        
        if  idxtipo > -1:
            
            idxtipo += 1
            
            while picture[idxtipo:idxtipo + 1] != ' ' and \
                  picture[idxtipo:idxtipo + 1] != '.':
                      
                tipo += picture[idxtipo:idxtipo + 1]
                idxtipo += 1
                
        if  redefines:
            
            posdic[cpo] = posicao = posdic[redefines] + 1
            
        else:
            
            posdic[cpo] = posicao
            
        nbytes = 0
        
        if  not redefines:
            
            if  pict == '9':
                
                if  tipo.find('COMP-3') > -1:
                    
                    nbytes = (((inteiro + decimais) / 2) + 1)
                    
                    posicao += nbytes
                    
                elif tipo.find('COMP') > -1:
                    
                    if  inteiro < 5:
                        
                        posicao += 2
                        nbytes = 2
                        
                    elif inteiro < 10:
                        
                        posicao += 4
                        nbytes = 4
                        
                    else:
                        
                        posicao += 8
                        nbytes = 8
                        
                else:
                    
                    nbytes = inteiro + decimais
                    posicao += nbytes
                    
            else:
                
                nbytes = inteiro
                posicao += nbytes
                
        regc[cpo] = {}
        
        regc[cpo]['nivel'] = nivel
        regc[cpo]['natureza'] = pict
        regc[cpo]['posicao'] = posdic[cpo]
        regc[cpo]['picture'] = picts
        regc[cpo]['tamanho'] = tam
        regc[cpo]['inteiro'] = inteiro
        regc[cpo]['decimais'] = decimais if decimais else 0
        regc[cpo]['tipo'] = tipo
        regc[cpo]['bytes'] = nbytes
        regc[cpo]['redefines'] = redefines
        regc[cpo]['itemGrupo'] = cpox
        regc[cpo]['occurs'] = occurs

    length = 0
    
    nivel = 0

    for k in regc:

        if  regc[k]['redefines']:
            nivel = regc[k]['nivel']
            continue

        if  nivel and regc[k]['nivel'] > nivel:
            continue

        nivel = 0
        
        try:
            bytes = int(regc[k]['bytes'])
            
        except:
            bytes = 0
        
        try:
            occurs = int(regc[k]['occurs'])
            
        except:
            occurs = 1

        length += (bytes * (occurs if occurs else 1))

    msg = 'calculo ok.'

    return {'retorno': True, 'msg': msg, 'lrecl': length}
