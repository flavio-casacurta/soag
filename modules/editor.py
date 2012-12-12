# -*- coding: utf-8 -*-

import utilities as utl

class Editor():

    arquivo    = ''
    lines      = []
    line       = 0
    column     = 0
    erros      = []
    nomeFisico = ''

    def __init__(self, arquivo, nome='', dclgen=False, dmlgen=False):

        self.arquivo    = ''
        self.lines      = []
        self.line       = 0
        self.column     = 0
        self.erros      = []
        self.line       = 0
        self.nomeFisico = ''

        try:
            self.arquivo = arquivo
            arqs         = open(arquivo).readlines()
            line         = ''
            nivel10      = False
            pk           = False
            for arq in arqs:
                line += arq
                if  dclgen:
                    if  not self.nomeFisico and arq.find('DB2PRD.') > -1:
                        self.nomeFisico = arq[arq.find('DB2PRD.')+7: \
                                              arq.find(')')]
                        line = ''
                        continue
                    if  not nivel10 and arq.find('10 ') > -1:
                        nivel10 = True
                    if  arq[6:7] == ' ':
                        if  nivel10:
                            if  arq.find('.') > -1:
                                self.lines.append(line.replace('\r\n','').\
                                                       replace('\n','').\
                                                       replace('\r',''))
                                line = ''
                            else:
                                line = ''
                        else:
                            self.lines.append(line.replace('\r\n','').\
                                                   replace('\n','').\
                                                   replace('\r',''))
                            line = ''
                    else:
                        line = ''
                elif dmlgen:
                    if  arq.find('PRIMARY KEY ') > -1:
                        if  arq.find(')') > -1:
                            self.lines.append(line.replace('\r\n','').\
                                                   replace('\n','').\
                                                   replace('\r',''))
                            line = ''
                            pk   = True
                        else:
                            continue
                    if  not pk:
                        if  arq.find(')') > -1:
                            pk = True
                        else:
                            self.lines.append(line.replace('\r\n','').\
                                                   replace('\n','').\
                                                   replace('\r',''))
                            line = ''
                    else:
                        self.lines.append(line.replace('\r\n','').\
                                               replace('\n','').\
                                               replace('\r',''))
                        line = ''

                else:
                    self.lines.append(line.replace('\r\n','').\
                                           replace('\n','').\
                                           replace('\r',''))
                    line = ''
        except:
            self.arquivo = nome
            for arq in arquivo:
                self.lines.append(arq)

    def active(self):

        return True if self.lines else False

    def getErros(self):

        return self.erros

    def getNomeFisico(self):

        return self.nomeFisico

    def getFile(self):

        return self.lines

    def getLine(self, line='.'):

        if  line <> '.':
            try:
                return self.lines[line]
            except:
                return ''
        else:
            try:
                return self.lines[self.line]
            except:
                return ''

    def setLine(self, texto, line='.'):

        if  line <> '.':
            try:
                self.lines[line] = texto
            except:
                return False
        else:
            try:
                self.lines[self.line] = texto
            except:
                return False

        return self.setPosColumn(0)

    def addLine(self, line='.', qtde=0):

        if  qtde:
            for qtd in qtde:
                if  line:
                    if  line <> '.':
                        try:
                            self.lines.insert(line+1, '')
                            line += 1
                        except:
                            return False
                    else:
                        self.lines.insert(self.line+1, '')
                else:
                    self.lines.insert(self.line+1, '')
                self.line += 1
        else:
            if  line:
                if  line <> '.':
                    try:
                        self.lines.insert(line+1, '')
                        line += 1
                    except:
                        return False
                else:
                    self.lines.insert(self.line+1, '')
            else:
                self.lines.insert(self.line+1, '')
            self.line += 1

        return self.setPosColumn(0)

    def delLine(self, line='.'):

        if  line:
            if  line <> '.':
                try:
                    self.lines.pop(line)
                except:
                    return False
            else:
                self.lines.pop(self.line)
        else:
            self.lines.pop(self.line)

        if  self.line > self.getLines():
            self.line = self.getLines()

        return self.setPosColumn(0)

    def getLines(self):

        return len(self.lines) - 1

    def getPosLine(self):

        return self.line

    def setPosLine(self, line):

        self.line = line

        return self.setPosColumn(0)

    def getPosColumn(self):

        return self.column

    def setPosColumn(self, coluna):

        self.column = coluna

        return True

    def find(self, palavra):

        li = 0
        fp = False

        for arq in self.lines:
            ok = arq.find(palavra)
            if  ok > -1:
                self.line   = li
                cols = arq.split()
                idx  = 0
                for col in cols:
                    if  col == palavra:
                        self.column = idx
                        break
                    idx += 1
                fp = True
                break
            li += 1

        return li if fp else -1

    def getPalavra(self):

        col   = self.getPosColumn()
        linha = self.getLine().split()

        try:
            return linha[col]
        except:
            return ''

    def getPalavras(self):

        ret  = ''
        wrds = self.getLine().split()

        if  self.getPosColumn() < (len(wrds) - 1):
            for idx in xrange(self.getPosColumn(), len(wrds)-1):
                ret += (' ' if ret else '') + wrds[idx]
        else:
            ret = wrds[self.getPosColumn()]

        return ret

    def nextPalavra(self):

        return self.nextColumn()

    def prevPalavra(self):

        return self.prevColumn()

    def firstColumn(self):

        linha  = self.line
        linhas = self.getLines()

        if  linha < 0 or linha > linhas:
            return -1

        return self.setPosColumn(0)

    def lastColumn(self):

        return self.setPosColumn(len(self.getLine().split()) - 1)

    def nextColumn(self):

        col  = self.getPosColumn()
        cols = len(self.getLine().split()) - 1

        if (col + 1) > cols:
            self.nextLine()
            return self.firstColumn()

        return self.setPosColumn(col + 1)

    def prevColumn(self):

        col = self.getPosColumn()

        if (col - 1) < 0:
            self.prevLine()
            return self.lastColumn()

        return self.setPosColumn(col - 1)

    def nextLine(self, qtde=0):

        pos = self.line

        if  qtde:
            for idx in xrange(pos + 1, pos + qtde + 1):
                self.setPosLine(idx)
        else:
            self.setPosLine(pos + 1)

        return self.setPosColumn(0)

    def prevLine(self, qtde=0):

        pos = self.line

        if  qtde:
            for idx in xrange(pos - 1, pos - qtde - 1, -1):
                self.setPosLine(idx)
        else:
            self.setPosLine(pos - 1)

        return self.setPosColumn(0)

    def replace(self, de, para):

        for idx in xrange(0, self.getLines()):
            self.setLine(idx, self.getLine(idx).replace(de, para))

        return True

    def save(self):

        try:

            with open(self.arquivo, 'w') as f1:

                for line in self.lines:
                    f1.write(line + '\n')

            return True

        except:

            return False

    def saveAs(self, nome):

        try:

            self.arquivo = nome

            with open(nome, 'w') as f1:

                for line in self.lines:
                    f1.write(line + '\n')

            return True

        except:

            return False

    def formata(self, tb, limite=False):

        for idx in xrange(0, self.getLines()+1):
            linha = self.getLine(idx)
            for y in tb:
                if  linha[6: 7] == '*':
                    if  limite:
                        al = utl.alinhaPalavras(y[0], y[1], limite)
                    else:
                        al = utl.alinhaPalavras(y[0], y[1])
                    linha = linha.replace(al[0], al[1])
                    self.setLine(linha, idx)
                else:
                    linha = linha.replace(y[0], y[1])
                    self.setLine(linha, idx)

        return True
