# -*- coding:utf-8
import os
from Entidades import Entidades
from ColunasEntidades import ColunasEntidades

class ComparaTables:

    def __init__(self, db, cAppl=0):
        self.db               = db
        self.cAppl            = cAppl
        self.entidades        = Entidades(self.db, cAppl=self.cAppl)
        self.colunasEntidades = ColunasEntidades(self.db, self.cAppl)


    def comparaTables(self):
        retEntidade = self.entidades.selectEntidadesBycodigoAplicacao()
        if  not retEntidade[0]:
            return [0,'Ocorreu um erro na chamada de selectEntidadesBycodigoAplicacao.', retEntidade[1]]
        entidades = retEntidade[1]

        dicCols = {}

        for entidade in entidades:
            lisCols = []
            retColunasEntidades = self.colunasEntidades.selectColunasEntidadesResolvidasByCodigoEntidade(entidade.id)
            if  not retColunasEntidades[0]:
                if  retColunasEntidades[1]:
                    return [0, retColunasEntidades[2]]
                else:
                    return [0, 'Nao existem colunas para esta Entidade']
            colunasEntidade = retColunasEntidades[1]
            for col in colunasEntidade:
                lisCols.append(col.colunas.columnName)
            dicCols[entidade.nomeFisico]=lisCols


        path = 'C:\IMSDCxCICS\Bradesco\SACL\SQL'
        dicSQL = {}

        for entidade in entidades:
            lisCols = []
            sql = '{}.sql'.format(entidade.nomeExterno)
            lines = open(os.path.join(path, sql)).readlines()
            for line in lines:
                if (line.startswith('(') or
                    line.split()[0] == 'CREATE'):
                    continue
                if  line.split()[0] == 'CONSTRAINT':
                    break
                lisCols.append(line.split()[0])
            dicSQL[entidade.nomeFisico]=lisCols

        lisInconf = []

        for k in dicCols.keys():
            if  dicCols[k] != dicSQL[k]:
                lisInconf.append(k)

        return [dicCols, dicSQL, lisInconf]
