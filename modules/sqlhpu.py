# -*- coding: utf-8 -*-

import editor, utilities as utl

class Sql():

    sql = {'Nome'      : '', \
           'NomeFisico': '', \
           'Campos'    : [], \
           'Pks'       : [], \
           'Dates'     : [], \
           'Times'     : [], \
           'TimeStamps': [], \
           'VarChars'  : [], \
           'Nulls'     : [], \
           'Sinais'    : [], \
           'Length'    : 0, \
           'LenPks'    : 0, \
           'Filtros'   : []}
           
    dcl        = None
    dml        = None
    props      = None
    sinalCobol = 'off'
    
    def __init__(self, db=None, props=None, dirdcl='', dirdml='', \
                                nome='', model=None, sinalCobol='off'):

        self.sql = {'Nome'      : nome, \
                    'NomeFisico': '', \
                    'Campos'    : [], \
                    'Pks'       : [], \
                    'Dates'     : [], \
                    'Times'     : [], \
                    'TimeStamps': [], \
                    'VarChars'  : [], \
                    'Nulls'     : [], \
                    'Sinais'    : [], \
                    'Length'    : 0, \
                    'LenPks'    : 0, \
                    'Filtros'   : []}
                    
        self.dcl        = None
        self.dml        = None
        self.props      = props
        self.sinalCobol = sinalCobol
               
        if   (not  db and nome and props and dirdcl and dirdml and not model):
            self.dclgen(dirdcl + '/' + nome + '.cpy')
            self.dmlgen(dirdml + '/' + nome + '.sql')
        elif (not db and nome and not props and dirdcl and
                                                dirdml and not model):
            self.dclgen(dirdcl)
            self.dmlgenFile(dirdml)
        elif (not db and nome and not props and dirdcl and not
                                                dirdml and not model):
            self.dclgen(dirdcl)
        elif (db and nome and not props and not dirdcl and
                                                dirdml and not model):
            self.dmlgenFile(dirdml, db=db, tabela=nome)
        elif (db and nome and not props and not dirdcl and not
                                                dirdml and not model):
            if self.dclgenTable(db, nome):
               self.dmlgenTable(db, nome)
        if   (not  db and not nome and not props and not dirdcl and not 
                                                         dirdml and model):
            self.erwin(model)

    def dclgen(self, arquivo):

        self.dcl = editor.Editor(arquivo, dclgen=True)

        if  self.dcl.active():
            self.sql['NomeFisico'] = self.dcl.getNomeFisico()
            self.sql['Length'] = 0
            li = self.dcl.find('10 ')
            if  li > -1:
                while self.dcl.getPalavra() == '10':
                      self.dcl.nextPalavra()
                      cpo = self.dcl.getPalavra()
                      self.dcl.nextPalavra()
                      self.dcl.nextPalavra()
                      varchar = 'N'
                      if  self.dcl.getPalavra() == '49':
                          varchar = 'S'
                          self.dcl.nextLine()
                          self.dcl.firstColumn()
                          self.dcl.nextPalavra()
                          if  self.dcl.getLine().find('49') < 0:
                              self.dcl.nextLine()
                              self.dcl.firstColumn()
                              self.dcl.nextPalavra()
                          self.dcl.nextPalavra()
                          self.dcl.nextPalavra()
                          self.dcl.nextPalavra()
                      if  self.dcl.getPalavra()[0:1] == 'S':
                          sinal = 'S'
                      else:
                          sinal = ''
                      picture = self.getPicture(self.dcl.getLine()).\
                                                               replace('S', '')
                      if  picture[0:1] == '9':
                          value = 'ZEROS'
                      else:
                          value = 'SPACES'
                      self.sql['Campos'].append({'Nome': cpo,\
                             'Atributo':\
                               {'Picture':\
                                 {'Sinal'  : sinal,\
                                  'Tipo'   : self.getPictureTipo(picture),\
                                  'Inteiro': self.getPictureInteiro(picture),\
                                  'Decimal': self.getPictureDecimal(picture)},\
                                  'Value'  : value,\
                                  'VarChar': varchar}})
                      self.sql['Length'] += \
                                (int(self.getPictureInteiro(picture)) + \
                                 int(self.getPictureDecimal(picture)) + \
                                (1 if self.getPictureTipo(picture)=='9' and \
                                      self.sinalCobol=='on' else 0))
                      self.dcl.nextLine()
            li = self.dcl.find('DECLARE DB2PRD.')
            if  li > -1:
                self.dcl.nextLine()
                while self.dcl.getLine().find('END-EXEC.') < 0:
                      cpo = self.dcl.getPalavra()
                      if  cpo == '(':
                          self.dcl.nextPalavra()
                          cpo = self.dcl.getPalavra()
                      if  self.dcl.getLine().find('NOT NULL') < 0:
                          self.sql['Nulls'].append(cpo.replace('_', '-'))
                      if  self.dcl.getLine().find(' DATE') > -1:
                          self.sql['Dates'].append(cpo.replace('_', '-'))
                      if  self.dcl.getLine().find(' TIME') > -1:
                          self.sql['Times'].append(cpo.replace('_', '-'))
                      if  self.dcl.getLine().find(' TIMESTAMP') > -1:
                          self.sql['TimeStamps'].append(cpo.replace('_', '-'))
                      if  self.dcl.getLine().find(' VARCHAR') > -1:
                          self.sql['VarChars'].append(cpo.replace('_', '-'))
                      self.dcl.nextLine()

    def dmlgen(self, arquivo):        

        self.dml = editor.Editor(arquivo, dmlgen=True)

        if  self.dml.active():
            li = self.dml.find('PRIMARY KEY ')
            if  li > -1:
                Pks = self.getPrimaryKey(self.dml.getLine())
                self.sql['LenPks'] = 0
                for pk in Pks:
                    cpo = pk.replace('_', '-')
                    lnt = self.getCampoAtributo(cpo, 'Length') or 0
                    self.sql['Pks'].append(cpo)
                    self.sql['LenPks'] += (lnt + \
                      (1 if self.getCampoAtributo(cpo, 'Tipo')=='9' and \
                            self.sinalCobol=='on' else 0))
            else:
                camposc = self.props.getFieldsc()
                self.sql['LenPks'] = 0
                for campoc in camposc:
                    regra = self.props.getFieldscAtributo(campoc['nome'], \
                                                                   'validacao')
                    if  regra.find('PK') > -1:
                        cpo = campoc['nome'].replace('_', '-')
                        lnt = self.getCampoAtributo(cpo, 'Length') or 0
                        self.sql['Pks'].append(cpo)
                        self.sql['LenPks'] += (lnt + \
                          (1 if (self.getCampoAtributo(cpo, 'Tipo')=='9' and \
                                 self.sinalCobol=='on') else 0))
        else:
            camposc = self.props.getFieldsc()
            self.sql['LenPks'] = 0
            for campoc in camposc:
                regra = self.props.getFieldscAtributo(campoc['nome'], \
                                                                   'validacao')
                if  regra.find('PK') > -1:
                    cpo = campoc['nome'].replace('_', '-')
                    lnt = self.getCampoAtributo(cpo, 'Length') or 0
                    self.sql['Pks'].append(cpo)
                    self.sql['LenPks'] += lnt + \
                          (1 if self.getCampoAtributo(cpo, 'Tipo')=='9' and \
                                self.sinalCobol=='on' else 0)
        self.sql['Filtros'] = self.props.getFiltros()

    def dclgenTable(self, db, nome):

        tb = db(db.tabelas.nome==nome).select().first()
        
        if  tb:
            self.sql['NomeFisico'] = tb.descricao
            self.sql['Length']     = 0
            campos = db(db.campos.tabela==tb.id).select()
            for campo in campos:
                  cpo = campo.nome.replace('_', '-')
                  varchar = 'N'
                  if  campo.isVarchar == 'Sim':
                      varchar = 'S'
                  picture = campo.natureza
                  if  picture[0:1] == '9':
                      sinal = 'S'
                      value = 'ZEROS'
                  else:
                      value = 'SPACES'
                      sinal = ''
                  self.sql['Campos'].append({'Nome': cpo,\
                         'Atributo':\
                           {'Picture':\
                             {'Sinal'  : sinal,\
                              'Tipo'   : self.getPictureTipo(picture),\
                              'Inteiro': self.getPictureInteiro(picture),\
                              'Decimal': self.getPictureDecimal(picture)},\
                              'Value'  : value,\
                              'VarChar': varchar}})
                  self.sql['Length'] += \
                             (int(self.getPictureInteiro(picture)) + \
                              int(self.getPictureDecimal(picture)) + \
                            (1 if self.getPictureTipo(picture)=='9' and \
                                  self.sinalCobol=='on' else 0))
                  if  campo.nulo == 'Sim':
                      self.sql['Nulls'].append(cpo)
                  if  campo.isDate == 'Sim':
                      self.sql['Dates'].append(cpo)
                  if  campo.isTime == 'Sim':
                      self.sql['Times'].append(cpo)
                  if  campo.isTimestamp == 'Sim':
                      self.sql['TimeStamps'].append(cpo)
                  if  campo.isVarchar == 'Sim':
                      self.sql['VarChars'].append(cpo)
                  if  campo.pk == 'Sim':
                      self.sql['Pks'].append(cpo)
                      self.sql['LenPks'] += \
                                  self.getCampoAtributo(cpo, 'Length') + \
                            (1 if self.getCampoAtributo(cpo, 'Tipo')=='9' and \
                                  self.sinalCobol=='on' else 0)
            return True if campos else False

        return False

    def dmlgenTable(self, db, nome):        

        Pks = []

        tb  = db(db[nome].nome==nome).select().first()
        
        if  tb:
            campos = db(db.campos.tabela==tb.id).select()
            for campo in campos:
                if  campo.pk == 'Sim':
                    Pks.append(campo.nome)

        self.sql['LenPks'] = 0
        
        for pk in Pks:
            cpo = pk.replace('_', '-')
            self.sql['Pks'].append(cpo)
            self.sql['LenPks'] += self.getCampoAtributo(cpo, 'Length') + \
                            (1 if self.getCampoAtributo(cpo, 'Tipo')=='9' and \
                                  self.sinalCobol=='on' else 0)

    def dmlgenFile(self, arquivo, db=None, tabela=None):        

        if  db and tabela:
            if  self.dclgenTable(db, tabela):
                self.dml = editor.Editor(arquivo, dmlgen=True)
                if  self.dml.active():
                    li = self.dml.find('PRIMARY KEY ')
                    if  li > -1:
                        Pks = self.getPrimaryKey(self.dml.getLine())
                        self.sql['LenPks'] = 0
                        for pk in Pks:
                            cpo = pk.replace('_', '-')
                            self.sql['Pks'].append(cpo)
                            self.sql['LenPks'] += \
                                  self.getCampoAtributo(cpo, 'Length') + \
                            (1 if self.getCampoAtributo(cpo, 'Tipo')=='9' \
                              and self.sinalCobol=='on' else 0)

    def dataType(self, datatype):
        
        isVarChar = True if datatype.startswith('VAR') else False
        tamanho   = ''

        if (datatype.startswith('CHARACTER')  or
            datatype.startswith('VARCHAR')    or
            datatype.startswith('DATE')       or
            datatype.startswith('TIME')       or
            datatype.startswith('TIMESTAMP')):
            picture  = 'X'
            tipo     = ''
        else:
            picture  = 'S9'
            if  datatype.startswith('SMALLINT'):
                tipo     = ' COMP'
                tamanho  = '4'
            elif datatype.startswith('INTEGER'):
                tipo    = ' COMP'
                tamanho = '9'
            else:
                tipo    = ' COMP-3'

        if  tamanho:
            picture += ('(%s)%s' % (tamanho, tipo))
        else:
            dt1 = datatype.split('(')
            if  len(dt1) > 1:
                picture += '('
                dt2 = dt1[1].split(')')
                dt3 = dt2[0].split(',')
                if  len(dt3) > 1:
                    picture += str(int(dt3[0].strip())-int(dt3[1].strip()))
                    picture += 'V9('
                    picture += dt3[1]
                    picture += ')'
                else:
                    picture += dt2[0]
                picture += (')%s' % tipo)

        isDate      = True if datatype.startswith('DATE')      else False
        isTime      = True if datatype.startswith('TIME')      else False
        isTimeStamp = True if datatype.startswith('TIMESTAMP') else False
        
        return {'isVarChar': isVarChar, 'picture': picture, 'isDate': isDate,
                'isTime': isTime, 'isTimeStamp': isTimeStamp}

    def erwin(self, model):
        
        if not model: return False

        cpo      = model['nomeFisico'].replace('_', '-')
        dataType = self.dataType(model['dataType'])
        null     = model['null']
        picture  = dataType['picture']
        tipo     = self.getPictureTipo(picture)

        if  tipo == '9':
            value = 'ZEROS'
            sinal = 'S'
        else:
            value = 'SPACES'
            sinal = ''

        self.sql['Campos'].append({'Nome': cpo,
                 'Atributo':
                 {'Picture':
                   {'Sinal'  : sinal,
                    'Tipo'   : tipo,
                    'Inteiro': self.getPictureInteiro(picture),
                    'Decimal': self.getPictureDecimal(picture)},
                    'Value'  : value,
                    'VarChar': 'S' if dataType['isVarChar'] else 'N'}})

        self.sql['Length'] += \
                   (int(self.getPictureInteiro(picture)) +
                    int(self.getPictureDecimal(picture)) +
                   (1 if tipo == '9' and self.sinalCobol=='on' else 0))

        if  null:
            self.sql['Nulls'].append(cpo)

        if  dataType['isDate']:
            self.sql['Dates'].append(cpo)

        if  dataType['isTime']:
            self.sql['Times'].append(cpo)

        if  dataType['isTimeStamp']:
            self.sql['TimeStamps'].append(cpo)

        if  dataType['isVarChar']:
            self.sql['VarChars'].append(cpo)

        if  model['pk']:
            self.sql['Pks'].append(cpo)
            self.sql['LenPks'] += \
                       self.getCampoAtributo(cpo, 'Length') + \
                       (1 if tipo == '9' and self.sinalCobol=='on' else 0)

        return True

    def getSql(self):
        
        return self.sql
        
    def getPrimaryKey(self, linha):
        
        pks = []
        cpo = ''
        col = linha.find('KEY ') + 4
        
        while linha[col: col+1] <> '(' and col <= len(linha):
              col += 1
              
        col += 1

        while linha[col: col+1] <> ')' and col <= len(linha):
              if  linha[col: col+1] == ' ':
                  col += 1
                  continue
              if  linha[col: col+1] == ',':
                  pks.append(cpo)
                  cpo  = ''
                  col += 1
                  continue
              cpo += linha[col: col+1]
              col += 1

        if  cpo:        
            pks.append(cpo)

        return pks
    
    def getNome(self):
        
        return self.sql['Nome']
    
    def getNomeFisico(self):
        
        return self.sql['NomeFisico']
    
    def getLength(self):
        
        return self.sql['Length']
    
    def getLenPks(self):
        
        return self.sql['LenPks']
    
    def getCampo(self, campo):

        ret = {}

        for x in self.sql['Campos']:
            if  x['Nome'] == campo:
                ret = x['Atributo']
                break

        return ret
    
    def getCampos(self, cobol=False):
        
        ret = []
      
        for x in self.sql['Campos']:
            ret.append(x['Nome'] if not cobol else x['Nome'].replace('_', '-'))

        return ret
    
    def getCampoAtributo(self, campo, atributo, a1=None):
        
        ret = ''
      
        for x in self.sql['Campos']:
            if  x['Nome'] == campo:
                if  atributo == 'Picture':
                    pict = x['Atributo']['Picture']
                    ret  = '+(' if (pict['Tipo'] == '9' and \
                                   self.sinalCobol=='on') else '' + \
                                   pict['Tipo'] + '('
                    if  not a1:
                        ret += '{:>03}'.format(pict['Inteiro'])
                        ret += ')'
                        if  pict['Decimal'] <> '0':
                            ret += 'V9(' + \
                                  '{:>02}'.format(pict['Decimal']) + ')'
                    else:
                        ret = pict[a1]
                else:
                    if  atributo == 'PictureSinal':
                        pict = x['Atributo']['Picture']
                        ret  = '+(' if (pict['Tipo'] == '9' and \
                                       self.sinalCobol=='on') else '' + \
                                       pict['Tipo'] + '('
                        if  not a1:
                            ret += '{:>03}'.format(pict['Inteiro'])
                            ret += ')'
                            if  pict['Decimal'] <> '0':
                                ret += \
                          'V9(' + '{:>02}'.format(pict['Decimal']) + ')'
                        else:
                            ret = pict[1]
                    else:
                        if  atributo == 'Tamanho':
                            pict = x['Atributo']['Picture']
                            ret  = pict['Inteiro']
                            if  pict['Decimal'] <> '0':
                                ret  = str(int(ret) + int(pict['Decimal']))
                                ret += 'V' + pict['Decimal']
                        else:
                            if  atributo == 'Length':
                                pict = x['Atributo']['Picture']
                                ret  = int(pict['Inteiro']) + \
                                       int(pict['Decimal'])
                            else:
                                if  atributo == 'Tipo':
                                    pict = x['Atributo']['Picture']
                                    ret  = pict['Tipo']
                                else:
                                    if  atributo == 'Inteiro':
                                        pict = x['Atributo']['Picture']
                                        ret  = int(pict['Inteiro'])
                                    else:
                                        if  atributo == 'Decimal':
                                            pict = x['Atributo']['Picture']
                                            ret  = int(pict['Decimal'])
                                        else:
                                            if  atributo == 'Sinal':
                                                pict = x['Atributo']\
                                                                  ['Picture']
                                                ret  = 'S9-'
                                                ret += '{:>03}'.\
                                                      format(pict['Inteiro'])
                                                if  pict['Decimal'] <> '0':
                                                    ret += '-V' + \
                                                 ('9' * int(pict['Decimal']))
                                            else:
                                                ret = x['Atributo'][atributo]

        return ret
    
    def getPks(self):
        
        return self.sql['Pks']
    
    def getNulls(self):
        
        return self.sql['Nulls']
    
    def isPk(self, cpo):
        
        ret = 0
      
        for x in self.sql['Pks']:
            if  x == cpo:
                ret = 1
                break

        return ret
    
    def isDate(self, cpo):
        
        ret = 0
        
        for x in self.sql['Dates']:
            if  x == cpo:
                ret = 1
                break

        return ret
    
    def isTime(self, cpo):
        
        ret = 0

        for x in self.sql['Times']:
            if  x == cpo:
                ret = 1
                break

        return ret
    
    def isTimeStamp(self, cpo):

        ret = 0

        for x in self.sql['TimeStamps']:
            if  x == cpo:
                ret = 1
                break

        return ret
    
    def isVarChar(self, cpo):
        
        ret = 0

        for x in self.sql['VarChars']:
            if  x == cpo:
                ret = 1
                break

        return ret
    
    def isNumeric(self, cpo):
        
        return True if self.getCampoAtributo(cpo, 'Tipo') == '9' else False
    
    def isString(self, cpo):
        
        return False if self.getCampoAtributo(cpo, 'Tipo') == '9' else True
    
    def isNull(self, cpo):
        
        ret = False
      
        for x in self.sql['Nulls']:
            if  x == cpo:
                ret = True
                break

        return ret
    
    def isSinal(self, cpo):
        
        ret = False
      
        for x in self.sql['Sinais']:
            if  x[0] == cpo:
                ret = True
                break

        return ret
    
    def getSinal(self, cpo):
        
        ret = ''
      
        for x in self.sql['Sinais']:
            if  x[0] == cpo:
                ret = x[1]
                break

        return ret
    
    def getNotPks(self):
        
        campos = self.getCampos()
        pks    = self.getPks()
        ret    = []
        
        for campo in campos:
            epk = False
            for pk in pks:
                if  campo == pk:
                    epk = True
                    break
            if  not epk:
                ret.append(campo)
                
        return ret
    
    def getCamposCobol(self):
        
        ret = []
        
        for x in self.sql['Campos']:
            ret.append('       01  ' + utl.limita('WRK-' + x['Nome'], 30))
            ret.append((' ' * 38) + ' PIC ' + \
                utl.pad(self.getCampoAtributo(x['Nome'], 'Picture'), 10) + \
                ' VALUE ' + self.getCampoAtributo(x['Nome'], 'Value') + '.')

        return ret
    
    def getCamposBook(self, spaces, prefix, num, book, \
                            plus, pluss, length, a1=None):
        
        ret = []
        
        for x in self.sql['Campos']:
            if  len(utl.limita(book + '-' + prefix + '-' + \
                                                    x['Nome'], 30)) < length:
                if  a1 and not self.isPk(x['Nome']):
                    ret.append((' ' * spaces) + ' ' + num + ' ' + \
                        utl.pad(utl.limita(book + '-' + prefix + '-' + \
                                x['Nome'], 30), length - 1 + pluss)  + \
                        ' PIC ' + \
                        self.getCampoAtributo(x['Nome'], 'Picture') + '.')
                else:
                    if  a1:
                        ret.append((' ' * spaces) + ' ' + num + ' '       + \
                            utl.pad(utl.limita(book + '-' + prefix + '-'  + \
                                        x['Nome'], 30), length - 1 + \
                                        pluss) + ' PIC ' + \
                                        self.getCampoAtributo(x['Nome'], \
                                        'Picture') + '.')
            else:
                if  a1 and not self.isPk(x['Nome']):
                    ret.append((' ' * spaces) + ' ' + num + ' ' + \
                        utl.limita(book + '-' + prefix + '-' + \
                            x['Nome'], 30))
                    ret.append((' ' * 25 + spaces + plus) + ' PIC ' + \
                        self.getCampoAtributo(x['Nome'], 'Picture') + '.')
                else:
                    if  a1:
                        ret.append((' ' * spaces) + ' ' + num + ' ' + \
                            utl.limita(book + '-' + prefix + '-' + \
                                x['Nome'], 30))
                        ret.append((' ' * 25 + spaces + plus) + ' PIC ' + \
                           self.getCampoAtributo(x['Nome'], 'Picture') + '.')

        return ret
    
    def getPksBook(self, spaces, prefix, num, book, plus, length):
        
        ret = []
        
        for x in self.sql['Pks']:
            if  len(utl.limita(book + '-' + prefix + '-' + x, 30)) < length:
                ret.append((' ' * spaces) + ' ' + num + ' ' + \
                    utl.pad(utl.limita(book + '-' + prefix + '-' + x, 30), \
                    length - 1) + ' PIC ' + self.getCampoAtributo(x, \
                    'Picture') + '.')
            else:
                ret.append((' ' * spaces) + ' ' + num + ' ' + \
                    utl.limita(book + '-' + prefix + '-' + x, 30))
                ret.append((' ' * 43 + plus) + ' PIC ' + \
                    self.getCampoAtributo(x, 'Picture') + '.')

        return ret
    
    def getCamposCobolSinal(self):
        
        ret = []
        
        for x in self.sql['Campos']:
            if  self.isNumeric(x['Nome']):
                cpo  = utl.limita('WRK-AUX-' + \
                           self.getCampoAtributo(x['Nome'], 'Sinal'), 30)
                cpor = utl.limita('WRK-AUX-' + \
                           self.getCampoAtributo(x['Nome'], 'Sinal').\
                                replace('S', ''), 30)
                ha = False
                for y in self.sql['Sinais']:
                    if  y[1] == ('WRK-AUX-' + \
                                  self.getCampoAtributo(x['Nome'], 'Sinal')):
                        ha = True
                        break
                if  not ha:
                    ret.append((' ' * 7) + '01  ' + utl.pad(cpo, 27) + \
                        ' PIC ' + utl.pad(self.getCampoAtributo(x['Nome'], \
                                         'PictureSinal'), 15) + ' VALUE ' + \
                        self.getCampoAtributo(x['Nome'], 'Value') + '.')
                    ret.append((' ' * 7) + \
                        '01  FILLER                    ' + \
                            '  REDEFINES ' + cpo + '.')
                    ret.append((' ' * 7) + \
                        '    05 FILLER                 ' + \
                            '  PIC  X(001).')
                    ret.append((' ' * 7) + '    05 ' + utl.pad(cpor, 24) + \
                        ' PIC ' + utl.pad(self.getCampoAtributo(x['Nome'], \
                        'Picture') + '.', 15).replace('+', ' '))
                    ret.append('')
                self.sql['Sinais'].append([x['Nome'], cpo])

        return ret
    
    def getPksCobol(self):
        
        ret = []
        
        for x in self.sql['Pks']:
            ret.append('       01  ' + utl.limita('WRK-' + x + '-INI', 30))
            ret.append((' ' * 38) + ' PIC ' + \
                utl.pad(self.getCampoAtributo(x, 'Picture'), 15) + \
                ' VALUE ' + self.getCampoAtributo(x, 'Value') + '.')
            ret.append('       01  ' + utl.limita('WRK-' + x + '-FIM', 30))
            ret.append((' ' * 38) + ' PIC ' + \
                utl.pad(self.getCampoAtributo(x, 'Picture'), 15) + \
                ' VALUE ' + self.getCampoAtributo(x, 'Value') + '.')

        return ret
    
    def getChavesCobol(self):
        
        ret = []
        
        for x in self.sql['Pks']:
            cpo = (' ' * 11) + '05 ' + utl.limita('WRK-CH-' + x, 30)
            if  len(utl.pad(cpo, 38) + ' PIC ' + \
                utl.pad(self.getCampoAtributo(x, 'Picture'), 15) + \
                ' VALUE ' + self.getCampoAtributo(x, 'Value') + '.') < 72:
                ret.append(utl.pad(cpo, 38) + ' PIC ' + \
                    utl.pad(self.getCampoAtributo(x, 'Picture'), 15) + \
                    ' VALUE ' + self.getCampoAtributo(x, 'Value') + '.')
            else:
                ret.append(cpo)
                ret.append((' ' * 38) + ' PIC ' + \
                    utl.pad(self.getCampoAtributo(x, 'Picture'), 15) + \
                    ' VALUE ' + self.getCampoAtributo(x, 'Value') + '.')

        return ret
    
    def getNullsCobol(self, a1=None):
        
        ret = []
        
        for x in self.sql['Nulls']:
            if  a1:
                for campoc in a1:
                    if  campoc['nome'] == x:
                        if  not self.isPk(x):
                            if  not ret:
                                ret = ['       01  WRK-VAR-NULL.']
                            cpo = utl.limita('WRK-' + x + '-NULL', 30)
                            if  len(utl.pad('           05 ' + cpo, 38) + \
                                ' PIC S9(004) COMP    VALUE ZEROS.') < 72:
                                ret.append(utl.pad('           05 ' + \
                                    cpo, 38) + \
                                    ' PIC S9(004) COMP    VALUE ZEROS.')
                            else:
                                ret.append('           05 ' + cpo)
                                ret.append(\
                                         '                              ' + \
                                         '         PIC S9(004) COMP    V' + \
                                         'ALUE ZEROS.')
                            break
            else:
                if  not self.isPk(x):
                    if  not ret:
                        ret = ['       01  WRK-VAR-NULL.']
                    cpo = utl.limita('WRK-' + x + '-NULL', 30)
                    if  len(utl.pad('           05 ' + cpo, 38) + \
                            ' PIC S9(004) COMP    VALUE ZEROS.') < 72:
                        ret.append(utl.pad('           05 ' + cpo, 38) + \
                            ' PIC S9(004) COMP    VALUE ZEROS.')
                    else:
                        ret.append('           05 ' + cpo)
                        ret.append(\
                                 '                                      ' + \
                                 '  PIC S9(004) COMP    VALUE ZEROS.')

        return ret
    
    def getNullsVarCharCobol(self, a1=None):
        
        ret = []
        
        for x in self.sql['Nulls']:
            if  a1:
                for campoc in a1:
                    if  campoc['nome'] == x:
                        if  not self.isPk(x) and self.isVarChar(x):
                            if  not ret:
                                ret = ['       01  WRK-VAR-NULL.']
                            cpo = utl.limita('WRK-' + x + '-NULL', 30)
                            if  len(utl.pad('           05 ' + cpo, 38) + \
                                   ' PIC S9(004) COMP    VALUE ZEROS.') < 72:
                                ret.append(utl.pad('           05 ' + \
                                         cpo, 38) + \
                                         ' PIC S9(004) COMP    VALUE ZEROS.')
                            else:
                                ret.append('           05 ' + cpo)
                                ret.append(\
                                         '                              ' + \
                                         '         PIC S9(004) COMP    V' + \
                                         'ALUE ZEROS.')
                            break
            else:
                if  not self.isPk(x) and self.isVarChar(x):
                    if  not ret:
                        ret = ['       01  WRK-VAR-NULL.']
                    cpo = utl.limita('WRK-' + x + '-NULL', 30)
                    if  len(utl.pad('           05 ' + cpo, 38) + \
                            ' PIC S9(004) COMP    VALUE ZEROS.') < 72:
                        ret.append(utl.pad('           05 ' + cpo, 38) + \
                            ' PIC S9(004) COMP    VALUE ZEROS.')
                    else:
                        ret.append('           05 ' + cpo)
                        ret.append(\
                                 '                                      ' + \
                                 ' PIC S9(004) COMP    VALUE ZEROS.')
        
        return ret
    
    def getSqlUpdate(self, camposct):
        
        ret    = []
        ret.append('           EXEC SQL')
        ret.append('                UPDATE DB2PRD.' + self.getNomeFisico())
        pks    = self.getPks()
        npks   = self.getNotPks()
        pv     = False
        for npk in npks:
            setc = False
            for campoc in camposct:
                if  campoc['nome'] == npk       and \
                   (npk.find('CUSUAR-INCL') < 0 and \
                    npk.find('CUSUAR_INCL') < 0 and \
                    npk.find('HINCL-REG')   < 0 and \
                    npk.find('HINCL_REG')   < 0):
                    setc = True
                    break
            if  setc:
                if  not pv:
                    if  self.isTimeStamp(campoc['nome']):
                        ret.append('                SET ' + \
                            utl.pad('         ' + \
                                    npk.replace('-', '_'), 30) + \
                            ' = CURRENT TIMESTAMP')
                    else:
                        if  self.isDate(campoc['nome']):
                            ret.append('                SET ' + \
                                utl.pad('         ' + \
                                        npk.replace('-', '_'), 30) + \
                                ' = CURRENT DATE')
                        else:
                            ret.append('                SET ' + \
                                utl.pad('         ' + \
                                        npk.replace('-', '_'), 30) + ' =')
                            ret.append('                   :' + \
                                self.getNome() + '.' + npk)
                            if  self.isNull(npk):
                                ret.append('                        :' + \
                                    utl.limita('WRK-' + npk + '-NULL', 30))
                    pv = True
                else:
                    if  self.isTimeStamp(campoc['nome']):
                        ret.append('                  , ' + \
                            utl.pad('         ' + \
                                    npk.replace('-', '_'), 30) + \
                            ' = CURRENT TIMESTAMP')
                    else:
                        if  self.isDate(campoc['nome']):
                            ret.append('                  , ' + \
                                utl.pad('         ' + \
                                        npk.replace('-', '_'), 30) + \
                                ' = CURRENT DATE')
                        else:
                            ret.append('                  , ' + \
                                utl.pad('         ' + \
                                        npk.replace('-', '_'), 30) + ' =')
                            ret.append('                   :' + \
                                self.getNome() + '.' + npk)
                            if  self.isNull(npk):
                                if  npk.find('CUSUAR-INCL') < 0:
                                    ret.append(\
                                              '                        :' + \
                                      utl.limita('WRK-' + npk + '-NULL', 30))

        if  len(self.sql['Filtros']) > 0:
            for filtro in self.sql['Filtros']:
                ret.append(utl.lPad(filtro['arg1'], 21) + (' ' * 8) + \
                    utl.pad(filtro['arg2'], 22) + filtro['arg3'])
                ret.append('                   :' + self.getNome() + '.' + \
                    filtro['arg4'] + ' ' + filtro['arg5'] + ' ' + \
                    filtro['arg6'])
        else:
            pv = False
            for pk in pks:
                setc = False
                for campoc in camposct:
                    if  campoc['nome'] == pk:
                        setc = True
                        break
                if  setc:
                    if  not pv:
                        ret.append(utl.lPad('WHERE', 21) + (' ' * 8) + \
                                   utl.pad(pk.replace('-', '_'), 22) + '=')
                        ret.append('                   :' + \
                                                   self.getNome() + '.' + pk)
                        pv  = True
                    else:
                        ret.append(utl.lPad('AND', 21) + (' ' * 8)   + \
                                   utl.pad(pk.replace('-', '_'), 22) + '=')
                        ret.append('                   :' + \
                                                   self.getNome() + '.' + pk)

        ret.append('           END-EXEC.')

        return ret
    
    def getSqlInsert(self, campos, despr):
        
        ret  = []
        ret.append('           EXEC SQL INSERT INTO DB2PRD.' + \
                   self.getNomeFisico())
        pks  = self.getPks()
        npks = self.getNotPks()
        pv   = False

        for pk in pks:
            if  not pv:
                ret.append('                         ( ' + \
                           pk.replace('-', '_'))
                pv  = True
            else:
                ret.append('                         , ' + \
                           pk.replace('-', '_'))

        for npk in npks:
            setc = False
            for campoc in campos:
                if  campoc['nome'] == npk:
                    fora = False
                    for despr in despr:
                        if  npk == despr:
                            fora = True
                            break
                    if  not fora:
                        setc = True
                        break
            if  setc:
                ret.append('                         , ' + \
                           npk.replace('-', '_'))

        pv = False

        for pk in pks:
            if  not pv:
                ret.append('                ) VALUES ( :' + \
                           self.getNome() + '.' + pk)
                pv  = True
            else:
                ret.append('                         , :' + \
                           self.getNome() + '.' + pk)

        for npk in npks:
            setc = False
            nul  = 'N'
            for campoc in campos:
                if  campoc['nome'] == npk:
                    fora = False
                    for despr in despr:
                        if  npk == despr:
                            fora = True
                            break
                    if  not fora:
                        setc = True
                        if (campoc['nome'].find('HMANUT-')      > -1) or \
                           (campoc['nome'].find('CUSUAR-MANUT') > -1):
                            nul = 'S'
                        break
            if  setc:
                if  nul == 'S':
                    ret.append('                         , NULL')
                else:
                    if  self.isTimeStamp(campoc['nome']):
                        ret.append('                         , CURRENT T' + \
                                   'IMESTAMP')
                    else:
                        if  self.isDate(campoc['nome']):
                            ret.append('                         , CURRE' + \
                                       'NT DATE')
                        else:
                            ret.append('                         , :' + \
                                       self.getNome() + '.' + npk)
                            if  self.isNull(npk):
                                if  npk.find('CUSUAR-MANUT') < 0:
                                    ret.append('                        ' + \
                                               '       :' + \
                                               utl.limita('WRK-' + \
                                                          npk + '-NULL', 30))

        ret.append('                )')
        ret.append('           END-EXEC.')

        return ret
    
    def getTableSelect(self, db, table=0, where=False):
        
        ret = ''
        tab = db(db.entidades.id==table).select().first()
        
        if  not tab:
            return ret
            
        campos = db(db.colunasEntidades.codigoEntidade==tab.id).select()
        
        pv = False

        for campo in campos:
            col = db(db.colunas.id==campo.codigoColuna).select().first()
            if  col:
                if  not pv:
                    ret += 'SELECT %s\n' % col.columnName.replace('-', '_')
                    pv   = True
                else:
                    ret += '     , %s\n' % col.columnName.replace('-', '_')
        
        ret += 'FROM   DB2PRD.%s'    % tab.nomeFisico

        return ret
    
    def getSqlSelect(self):
        
        ret    = []
        campos = self.getCampos()
        pks    = self.getPks()
        pv     = False

        for campo in campos:
            if  not pv:
                ret.append('           EXEC SQL SELECT ' + \
                           campo.replace('-', '_'))
                pv = True
            else:
                ret.append('                         , ' + \
                           campo.replace('-', '_'))

        pv = False

        for campo in campos:
            if  not pv:
                ret.append('                      INTO :' + \
                           self.getNome() + '.' + campo)
                if  self.isNull(campo):
                    ret.append('                                :' + \
                               utl.limita('WRK-' + campo + '-NULL', 30))
                pv = True
            else:
                ret.append('                         , :' + \
                           self.getNome() + '.' + campo)
                if  self.isNull(campo):
                    ret.append('                                :' + \
                               utl.limita('WRK-' + campo + '-NULL', 30))

        if  not ret:
            pv = False
            for pk in pks:
                if  not pv:
                    ret.append('           EXEC SQL SELECT ' + \
                               pk.replace('-', '_'))
                    pv = True
                else:
                    ret.append('                         , ' + \
                               pk.replace('-', '_'))
            pv = False
            for pk in pks:
                if  not pv:
                    ret.append('                      INTO :' + \
                               self.getNome() + '.' + pk)
                    pv = True
                else:
                    ret.append('                         , :' + \
                               self.getNome() + '.' + pk)

        ret.append('                      FROM  DB2PRD.' + \
                   self.getNomeFisico())

        if  len(self.sql['Filtros']) > 0:
            for filtro in self.sql['Filtros']:
                ret.append(utl.lPad(filtro['arg1'], 26) + (' ' * 11) + \
                           utl.pad(filtro['arg2'], 22) + filtro['arg3'])
                ret.append((' ' * 27) + ':' + self.getNome() + '.' + \
                           filtro['arg4'] + ' ' + filtro['arg5'] + ' ' + \
                           filtro['arg6'])
        else:
            pv = False
            for pk in pks:
                if  not pv:
                    ret.append(utl.lPad('WHERE', 21) + (' ' * 8) + \
                               utl.pad(pk.replace('-', '_'), 22) + '=')
                    ret.append('                         :' + \
                               self.getNome() + '.' + pk)
                    pv = True
                else:
                    ret.append(utl.lPad('AND', 21) + (' ' * 8) + \
                               utl.pad(pk.replace('-', '_'), 22) + '=')
                    ret.append('                         :' + \
                               self.getNome() + '.' + pk)

        ret.append('           END-EXEC.')

        return ret
    
    def getSqlUnicidade(self, book, unicos, ia):
        
        ret = []
        pks = self.getPks()
        
        if  ia == 'a':
            for pk in pks:
                ret.append('           MOVE ' + book + '-' + pk)
                ret.append((' ' * 38) + ' TO ' + pk)
                ret.append((' ' * 38) + ' OF ' + self.getNome() + '.')

        for unico in unicos:
            ret.append('           MOVE ' + book + '-' + unico)
            ret.append((' ' * 38) + ' TO ' + unico)
            ret.append((' ' * 38) + ' OF ' + self.getNome() + '.')

        ret.append('')
        ret.append('           EXEC SQL SELECT COUNT(*)')
        ret.append('                      INTO :WRK-COUNT')
        ret.append('                      FROM  DB2PRD.' + \
                   self.getNomeFisico())

        pv = False

        if  ia == 'a':
            for pk in pks:
                if  not pv:
                    ret.append('                     WHERE           ' + \
                               pk.replace('-', '_'))
                    ret.append('                        <> :' + \
                               self.getNome() + '.' + pk)
                    pv = True
                else:
                    ret.append('                       AND           ' + \
                               pk.replace('-', '_'))
                    ret.append('                        <> :' + \
                               self.getNome() + '.' + pk)

        for unico in unicos:
            if  ia == 'a':
                ret.append('                       AND           ' + \
                           unico.replace('-', '_'))
                ret.append('                         = :' + \
                           self.getNome() + '.' + unico)
            else:
                if  not pv:
                    ret.append('                     WHERE           ' + \
                               unico.replace('-', '_'))
                    ret.append('                         = :' + \
                               self.getNome() + '.' + unico)
                    pv = True
                else:
                    ret.append('                       AND           ' + \
                               unico.replace('-', '_'))
                    ret.append('                         = :' + \
                               self.getNome() + '.' + unico)

        ret.append('           END-EXEC.')

        return ret
    
    def getSqlDeclareCursor(self, oper, campos):
        
        ret = []
        ret.append('           EXEC SQL')
        ret.append('                DECLARE CSR' + \
            ('01' if oper == '>=' else \
            ('02' if oper == '>'  else \
            ('01' if oper == 'P1' else \
            ('02' if oper == 'P2' else '03')))) + '-' + self.getNome() + \
            ' CURSOR FOR')
        pks = self.getPks()
        pv  = False

        for campoc in campos:
            if  campoc['nome'].find('-L ') > -1:
                campo = campoc['nome'][0, campoc['nome'].find('-L ')]
            else:
                campo = campoc['nome']
            if  not pv:
                if  self.isNull(campo):
                    if  self.getCampoAtributo(campo, 'Picture', \
                                                              'Tipo') == '9':
                        ret.append((' ' * 16) + 'SELECT' + (' ' * 7) + \
                                   ' VALUE(' + campo.replace('-', '_') + \
                                   ', 0)')
                    else:
                        if  self.isTimeStamp(campo):
                            if  len((' ' * 16) + 'SELECT' + (' ' * 7)   + \
                                    ' VALUE(' + campo.replace('-', '_') + \
                                    ", '0001-01-01-00.00.00.000000')") < 72:
                                ret.append((' ' * 16) + 'SELECT'   + \
                                           (' ' *  7) + ' VALUE('  + \
                                           campo.replace('-', '_') + \
                                           ", '0001-01-01-00.00.00.000000')")
                            else:
                                ret.append((' ' * 16) + 'SELECT'   + \
                                           (' ' * 7)  + ' VALUE('  + \
                                           campo.replace('-', '_') + ',')
                                ret.append((' ' * 29) + \
                                           "'0001-01-01-00.00.00.000000')")
                        else:
                            if  self.isDate(campo):
                                ret.append((' ' * 16) + 'SELECT'   + \
                                           (' ' * 7)  + ' VALUE('  + \
                                           campo.replace('-', '_') + \
                                           ", '0001-01-01')")
                            else:
                                if  self.isTime(campo):
                                    ret.append((' ' * 16) + 'SELECT'   + \
                                               (' ' * 7)  + ' VALUE('  + \
                                               campo.replace('-', '_') + \
                                               ", '00:00:00')")
                                else:
                                    if  self.isVarChar(campo):
                                        ret.append((' ' * 16) + 'SELECT' + \
                                                   (' ' * 14) + \
                                                   campo.replace('-', '_'))
                                    else:
                                        ret.append((' ' * 16) + 'SELECT'  + \
                                                   (' ' * 7)  + ' VALUE(' + \
                                                  campo.replace('-', '_') + \
                                                   ", ' ')")
                else:
                    ret.append((' ' * 16) + 'SELECT' + (' ' * 7) + \
                               campo.replace('-', '_'))
                pv = True
            else:
                if  self.isNull(campo):
                    if  self.getCampoAtributo(campo, 'Picture', 'Tipo') == '9':
                        ret.append((' ' * 20) + ' , VALUE(' + \
                                   campo.replace('-', '_') + ', 0)')
                    else:
                        if  self.isTimeStamp(campo):
                            if  len((' ' * 20) + ' , VALUE(' + \
                                campo.replace('-', '_') + \
                                ", '0001-01-01-00.00.00.000000')") < 72:
                                ret.append((' ' * 20) + ' , VALUE(' + \
                                           campo.replace('-', '_')  + \
                                           ", '0001-01-01-00.00.00.000000')")
                            else:
                                ret.append((' ' * 20) + ' , VALUE(' + \
                                           campo.replace('-', '_')  + ',')
                                ret.append((' ' * 29) + \
                                           "'0001-01-01-00.00.00.000000')")
                        else:
                            if  self.isDate(campo):
                                ret.append((' ' * 20) + ' , VALUE(' + \
                                           campo.replace('-', '_')  + \
                                           ", '0001-01-01')")
                            else:
                                if  self.isTime(campo):
                                    ret.append((' ' * 20) + ' , VALUE(' + \
                                               campo.replace('-', '_')  + \
                                               ", '00:00:00')")
                                else:
                                    if  self.isVarChar(campo):
                                        ret.append((' ' * 20) + \
                                                   ' ,       ' + \
                                                   campo.replace('-', '_'))
                                    else:
                                        ret.append((' ' * 20) + \
                                                   ' , VALUE(' + \
                                                 campo.replace('-', '_')  + \
                                                   ", ' ')")
                else:
                    ret.append((' ' * 20) + ' ,       ' + \
                               campo.replace('-', '_'))

        ret.append('                FROM DB2PRD.' + self.getNomeFisico())

        if  len(self.sql['Filtros']):
            for filtro in self.sql['Filtros']:
                if  oper == 'P1':
                    if  filtro['seq'] <> '1':
                        continue
                if  oper == 'P2':
                    if  filtro['seq'] <> '2':
                        continue
                ret.append(utl.lPad(filtro['arg1'], 21) + (' ' * 8) + \
                            utl.pad(filtro['arg2'], 22) + filtro['arg3'])
                ret.append('                   :' + self.getNome() + '.' + \
                           filtro['arg4'] + ' ' + filtro['arg5'] + ' ' + \
                           filtro['arg6'])
        else:
            pv = False
            for pk in pks:
                if  not pv:
                    if  oper == 'P1':
                        if  len(pks):
                            aux = '>='
                        else:
                            aux = '>'
                    else:
                        if  oper == 'P2':
                            if  len(pks):
                                aux = '<='
                            else:
                                aux = '<'
                        else:
                            aux = oper
                    ret.append('                WHERE       ('   + \
                               utl.pad(pk.replace('-', '_'), 30) + ' ' + aux)
                    ret.append((' ' * 19) + ':' + self.getNome() + '.' + \
                                                                    pk + ')')
                else:
                    if  oper == 'P1' or oper == 'P2':
                        for x in xrange(0, pv - 1):
                            ret.append('                  ' + \
                                      (' OR' if not x else 'AND') + \
                                      '       ' + ('('  if not x else ' ')  + \
                                      utl.pad(pks[x].replace('-', '_'), 30) + \
                                      ' =')
                            ret.append((' ' * 19) + ':' + self.getNome() + \
                                       '.' + pks[x])
                        ret.append('                  AND        ' + \
                                   utl.pad(pk.replace('-', '_'), 30) + ' ' + \
                                   ('>' if oper == 'P1' else '<'))
                        ret.append((' ' * 19) + ':' + self.getNome() + '.' + \
                                   pk + ')')
                    else:
                        ret.append('                  AND       (' + \
                                   utl.pad(pk.replace('-', '_'), 30) + ' ' + \
                                   ('>=' if oper == 'P1' else \
                                   ('<=' if oper == 'P2' else oper)))
                        ret.append((' ' * 19) + ':' + self.getNome() + '.' + \
                                   pk + ')')
                pv += 1

        pv = False

        for pk in pks:
            if  not pv:
                ret.append('                ORDER BY     '   + \
                           utl.pad(pk.replace('-', '_'), 30) + \
                           (' DESC'  \
                                   if oper == '<' or oper == 'P2' else ' ASC'))
                pv = True
            else:
                ret.append((' ' * 26) + ' , ' + \
                           utl.pad(pk.replace('-', '_'), 30) + \
                           (' DESC' \
                                   if oper == '<' or oper == 'P2' else ' ASC'))

        ret.append('                FETCH FIRST 51 ROWS ONLY')
        ret.append('           END-EXEC.')

        return ret
    
    def getSqlFetchCursor(self, campos):
        
        ret = []
        pv  = False

        for campoc in campos:
            if  campoc['nome'].find('-L ') > -1:
                campo = campoc['nome'][0: campoc['nome'].find('-L ')]
            else:
                campo = campoc['nome']
            if  not pv:
                ret.append((' ' * 19) + ':' + self.getNome() + '.' + campo)
                if  self.isNull(campo) and self.isVarChar(campo):
                    ret.append((' ' * 24) + ':WRK-' + campo + '-NULL')
                pv = True
            else:
                ret.append((' ' * 16) + ' , :' + self.getNome() + '.' + campo)
                if  self.isNull(campo) and self.isVarChar(campo):
                    ret.append((' ' * 16) + ' ,      :WRK-' + campo + '-NULL')

        return ret
    
    def getSqlDelete(self):
        
        ret = []
        
        ret.append('           EXEC SQL')
        ret.append('                DELETE FROM  DB2PRD.' + \
                   self.getNomeFisico())

        pks = self.getPks()

        if  len(self.sql['Filtros']):
            for filtro in self.sql['Filtros']:
                ret.append(utl.lPad(filtro['arg1'], 21) + (' ' * 8) + \
                            utl.pad(filtro['arg2'], 22) + filtro['arg3'])
                ret.append('                   :' + self.getNome() + '.' + \
                           filtro['arg4'] + ' ' + filtro['arg5'] + ' ' + \
                           filtro['arg6'])
        else:
            pv = False
            for pk in pks:
                if  not pv:
                    ret.append(utl.lPad('WHERE', 21) + (' ' * 8)  + \
                               utl.pad(pk.replace('-', '_'), 22) + '=')
                    ret.append('                   :' + self.getNome() + \
                               '.' + pk)
                    pv = True
                else:
                    ret.append(utl.lPad('AND', 21) + (' ' * 8)   + \
                               utl.pad(pk.replace('-', '_'), 22) + '=')
                    ret.append('                   :' + self.getNome() + \
                               '.' + pk)

        ret.append('           END-EXEC.')

        return ret
    
    def getSqlAutoPk(self, book, prop):
        
        ret1 = []
        ret2 = []
        pks  = self.getPks()
        pv   = 0
        pk0  = []
        pk1  = []
 
        for pk in pks:
            if  prop.getFieldscAtributo(pk, 'validacao').\
                                                           find('AUTO') > -1:
                if  not pv:
                    ret1.append('           EXEC SQL')
                    ret1.append('                SELECT VALUE(MAX(' + \
                                pk.replace('-', '_') + '), 0) + 1')
                    pv += 1
                else:
                    ret1.append('                     , VALUE(MAX(' + \
                                pk.replace('-', '_') + '), 0) + 1')
            if  prop.getFieldscAtributo(pk, 'natureza')  <> '' and \
                prop.getFieldscAtributo(pk, 'validacao') <> '' and \
                prop.getFieldscAtributo(pk, 'validacao').\
                                                       find('AUTO') < 0 and \
                prop.getFieldscAtributo(pk, 'validacao').\
                                                       find('PK')   < 0 and \
                not pk0:
                pk0.append(pk)
                continue
            if  pk0:
                pk1.append(pk)

        pv  = False
        pk0 = []
        pk1 = []

        for pk in pks:
            if  prop.getFieldscAtributo(pk, 'validacao').\
                                                           find('AUTO') > -1:
                if  not pv:
                    ret1.append('                  INTO :' + \
                                self.getNome() + '.' + pk)
                    pv += 1
                else:
                    ret1.append('                     , :' + \
                                self.getNome() + '.' + pk)
            if  prop.getFieldscAtributo(pk, 'natureza')  <> '' and \
                prop.getFieldscAtributo(pk, 'validacao') <> '' and \
                prop.getFieldscAtributo(pk, 'validacao').\
                                                       find('AUTO') < 0 and \
                prop.getFieldscAtributo(pk, 'validacao').\
                                                       find('PK')   < 0 and \
                not pk0:
                pk0.append(pk)
                continue
            if  pk0:
                pk1.append(pk)

        if  ret1:
            if  pk1:
                pv = False
                for rets in pk1:
                    if  not pv:
                        ret1.append('           EXEC SQL')
                        ret1.append('                SELECT VALUE(MAX(' + \
                                    rets.replace('-', '_') + '), 0) + 1')
                        pv += 1
                    else:
                        ret1.append('                     , VALUE(MAX(' + \
                                    rets.append('-', '_') + '), 0) + 1')
                pv = False
                for rets in pk1:
                    if  not pv:
                        ret1.append('                  INTO :' + \
                                    self.getNome() + '.' + rets)
                        pv += 1
                    else:
                        ret1.append('                     , :' + \
                                    self.getNome() + '.' + rets)

        if  ret1:
            ret1.append('                  FROM DB2PRD.' + \
                        self.getNomeFisico())
            if  pk0:
                pv = False
                for rets in pk0:
                    if  not pv:
                        ret1.append('                WHERE ' + \
                                    utl.lPad('       ' + \
                                    rets.replace('-', '_'), 30) + ' =')
                        ret1 .append('                   :' + \
                                     self.getNome() + '.' + rets)
                        pv += 1
                    else:
                        ret1.append('                  AND ' + \
                                    utl.lPad('       ' + \
                                    rets.replace('-', '_'), 30) + ' =')
                        ret1.append('                   :' + \
                                    self.getNome() + '.' + rets)
            ret1.append('           END-EXEC.')

        if  pk0:
            for rets in pk0:
                ret2.append('           MOVE ' + book + '-' + rets)
                ret2.append((' ' * 38) + ' TO ' + rets)
                ret2.append((' ' * 38) + ' OF ' + self.getNome() + '.')
                ret2.append('')

        ret3 = []
        
        for rets in ret2:
            ret3.append(rets)

        for rets in ret1:
            ret3.append(rets)

        return ret3
    
    def getPictureTipo(self, picture):

        idx = 0

        if  picture[idx: idx+1] == 'S':
            idx += 1

        if  picture[idx: idx+1] == '9' or picture[idx: idx+1] == 'Z':
            ret = '9'
        else:
            ret = 'X'

        return ret
    
    def getPictureInteiro(self, picture):

        ret = '0'
        idx =  0

        while picture[idx: idx+1] <> '('  and \
              picture[idx: idx+1] <> '.'  and \
              idx <= len(picture):
              idx += 1

        if  picture[idx: idx+1] == '.' or idx > len(picture):
            ret = '1'
        else:
            idx += 1
            pv   = False
            while picture[idx: idx+1] <> ')'  and \
                  picture[idx: idx+1] <> '.'  and \
                  idx <= len(picture):
                  if  not pv:
                      ret = picture[idx: idx+1]
                      pv  = True
                  else:
                      ret += picture[idx: idx+1]
                  idx += 1

        return ret
    
    def getPictureDecimal(self, picture):
        
        ret = '0'
        idx =  0

        while picture[idx: idx+1] <> '('  and \
              picture[idx: idx+1] <> '.'  and \
              idx <= len(picture):
              idx += 1

        if  picture[idx: idx+1] <> '.' and idx <= len(picture):
            idx += 1
            while picture[idx: idx+1] <> ')'  and \
                  picture[idx: idx+1] <> '.'  and \
                  idx <= len(picture):
                  idx += 1

            if  picture[idx: idx+1] <> '.' and idx <= len(picture):
                idx += 1
                while picture[idx: idx+1] <> '('  and \
                      picture[idx: idx+1] <> '.'  and \
                      idx <= len(picture):
                      idx += 1
                if  picture[idx: idx+1] <> '.' and idx <= len(picture):
                    idx += 1
                    pv   = False
                    while picture[idx: idx+1] <> ')'  and \
                          picture[idx: idx+1] <> '.'  and \
                          idx <= len(picture):
                          if  not pv:
                              ret = picture[idx: idx+1]
                              pv  = True
                          else:
                              ret += picture[idx: idx+1]
                          idx += 1

        return ret
    
    def getPicture(self, linha):

        word   = ''
        pos    = linha.find('PIC ')

        if  pos > -1:        
            coluna = pos + 4
            idx    = coluna
            while linha[idx: idx+1] <> ' '  and \
                  linha[idx: idx+1] <> '.'  and \
                  idx <= len(linha):
                  word += linha[idx: idx+1]
                  idx  += 1

        return word
