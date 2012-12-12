# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import sys
import Aplicacao
import ColunasEntidades

class Entidades:

    def __init__(self, db, cAppl=0, iderwin=0, model=None):
        self.db               = db
        self.cAppl            = cAppl
        self.iderwin          = iderwin
        self.model            = model
        self.aplicacao        = Aplicacao.Aplicacao(self.db, self.cAppl)
        self.applId           = self.aplicacao.getApplId()
        self.delecaoLogica    = self.aplicacao.getDelecaoLogica()
        self.colDelLog        = ''
        if self.delecaoLogica:
           self.colDelLog     = self.aplicacao.getColunaDelecaoLogica()
        self.entidades        = self.db.entidades

    def insertEntidades(self):
        lidos     = 0
        gravados  = 0
        #numTabIni = 500
        dicEnts   = {}
        generate  = lambda ent: ent['Do_Not_Generate']==False

        for lisEnts in filter(generate, self.model.getEntidades('')):
            lidos += 1
            nomeFisico       = lisEnts['User_Formatted_Physical_Name']
            nomeAmigavel     = lisEnts['User_Formatted_Name']
            descricao        = lisEnts['Definition']
            if  not descricao:
                descricao    = lisEnts['Comment']
            regto = self.db((self.db.erwinents.erwin == self.iderwin) &
                   (self.db.erwinents.entidade == nomeFisico)).select().first()
            if  not regto:
                print 'Desprezando: %s' % nomeFisico
                continue
            nomeExterno = regto.nomeExterno2
            dicEnts[nomeExterno] = {'nomeFisico':nomeFisico
                                   ,'nomeAmigavel':nomeAmigavel
                                   ,'descricao':descricao}

        for k in dicEnts:

#  Trata nomeAmigavel
            nomeAmigavel  = dicEnts[k]['nomeAmigavel']
            nNomeAmigavel = ''
            strt = 0
            for chr in xrange(1,len(nomeAmigavel)):
                if  nomeAmigavel[chr].isupper():
                    nNomeAmigavel = nNomeAmigavel + nomeAmigavel[strt:chr] + ' '
                    strt  = chr
            nNomeAmigavel = nNomeAmigavel + nomeAmigavel[strt:chr+1]
            dicEnts[k]['nomeAmigavel'] = nNomeAmigavel

#  Trata descrição

            if  dicEnts[k]['descricao']:
                dicEnts[k]['descricao'] = ' '.join(dicEnts[k]['descricao'].split())
#                dicEnts[k]['descricao'] = utl.nUni2Uni(' '.join(dicEnts[k]['descricao'].split()))
            else:
                dicEnts[k]['descricao'] = dicEnts[k]['nomeAmigavel']

        for k in sorted(dicEnts.keys()):
            try:
                self.entidades.insert(codigoAplicacao = int(self.cAppl)
                                     ,nomeExterno     = k
                                     ,nomeFisico      = dicEnts[k]['nomeFisico']
                                     ,nomeAmigavel    = dicEnts[k]['nomeAmigavel']
                                     ,descricao       = dicEnts[k]['descricao']
                                     )
                gravados = gravados +1
            except:
                return [0, "Ocorreu um erro no Insert da Tabela Entidades.", sys.exc_info()[1]]
        self.db.commit()
        return [1,'Entidades >>>'
               + '\n' + ' Lidos    = ' + str(lidos)
               + '\n' + ' Gravados = ' + str(gravados)
               + '\n']

#  Julgar de acordo com a coluna de deleção se gera serviço de deleção da entidade

    def updateEntidadesXprogramas(self):


        isTrue       = lambda value, lisDic, key: any([k for k in lisDic if k[key]==value])
        lidos        = 0
        gravados     = 0

        if  self.delecaoLogica:
            colEnt   = ColunasEntidades.ColunasEntidades(self.db, cAppl=self.cAppl)
        try:
            for query in self.db(self.entidades).select():
                lidos += 1
                if  not query.nomeExterno.startswith(self.applId):
                    lisPgm = [False for p in xrange(10)]
                else:
                    lisPgm = [True  for p in xrange(10)]
                    if  self.delecaoLogica:
                        ce = colEnt.selectColunasEntidadesByCodigoEntidade(query.id)
                        if  not ce[0]:
                            return [0, 'Ocorreu um erro no Update da Tabela Entidades,\
                                        no selectColunasEntidadesByCodigoEntidade']
                        if  isTrue(self.colDelLog, ce[1], 'codigoColuna'):
                            lisPgm[4] = False
                            lisPgm[5] = False
                try:
                    self.db((self.entidades.codigoAplicacao  == int(self.cAppl))
                          & (self.entidades.id               == query.id))         \
                              .update( coordenadorInclusao   =  lisPgm[0]
                                     , pgmInclusao           =  lisPgm[1]
                                     , coordenadorAlteracao  =  lisPgm[2]
                                     , pgmAlteracao          =  lisPgm[3]
                                     , coordenadorExclusao   =  lisPgm[4]
                                     , pgmExclusao           =  lisPgm[5]
                                     , coordenadorConsulta   =  lisPgm[6]
                                     , pgmConsulta           =  lisPgm[7]
                                     , coordenadorLista      =  lisPgm[8]
                                     , pgmLista              =  lisPgm[9]
                                     )
                    gravados = gravados +1
                except:
                    return [0, 'Ocorreu um erro no Update da Tabela Entidades.', sys.exc_info()[1]]
        except:
            return [0,'Ocorreu um erro no Select da Tabela Entidades.', sys.exc_info()[1]]

        self.db.commit()
        return [1,'Programas das Entidades >>>'
               + '\n' + 'lidos    = ' + str(lidos)
               + '\n' + 'Gravados = ' + str(gravados)
               + '\n']

    def selectEntidadesByEntidadeId(self, entidadeId):
        try:
            query=self.db(self.entidades.id == int(entidadeId)).select()
        except:
            return [0,'Ocorreu um erro no Select da Tabela Entidades.', sys.exc_info()[1]]
        if not query:
            return [0, 0]
        return [1, query]

    def selectEntidadesByNomeExterno(self, nomeExterno):
        try:
            query=self.db((self.entidades.codigoAplicacao == int(self.cAppl))
                        & (self.entidades.nomeExterno     == nomeExterno)).select()
        except:
            return [0, 'Ocorreu um erro no Select da Tabela Entidades.', sys.exc_info()[1]]
        if  not query:
            return [0, 0]
        return [1, query]

    def selectEntidadesByNomeFisico(self, nomeFisico):
        try:
            query=self.db((self.entidades.codigoAplicacao == int(self.cAppl))
                        & (self.entidades.nomeFisico      == nomeFisico)).select()
        except:
            return [0,' Ocorreu um erro no Select da Tabela Entidades.', sys.exc_info()[1]]
        if  not query:
            return [0, 0]
        return [1, query]

    def selectEntidadesProgramasBycodigoAplicacao(self):
        programasEntidade = []
        try:
            for query in self.db(self.entidades.codigoAplicacao == int(self.cAppl))   \
                         .select(self.entidades.ALL,orderby=self.entidades.nomeExterno):
                lista          = []
                codigoEntidade = int(query.id)
                programas      = [ query.pgmInclusao
                                 , query.pgmAlteracao
                                 , query.pgmExclusao
                                 , query.pgmConsulta
                                 , query.pgmLista        ]
                lista.append(codigoEntidade)
                lista.append(programas)
                programasEntidade.append(lista)
        except:
            return [0, 'Ocorreu um erro no Select da Tabela Entidades.', sys.exc_info()[1]]
        return [1, programasEntidade]

    def selectEntidadesBycodigoAplicacao(self):
        try:
            query = self.db(self.entidades.codigoAplicacao == int(self.cAppl))   \
                        .select(self.entidades.ALL,orderby=self.entidades.nomeExterno)
        except:
            return [0, 'Ocorreu um erro no Select da Tabela Entidades.', sys.exc_info()[1]]
        return [1, query]
