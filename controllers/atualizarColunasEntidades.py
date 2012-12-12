# coding: utf8

import utilities        as     utl
from   ColunasEntidades import *

@auth.requires_login()
def index():
   if  request.vars:
       idaplicacao = int(request.vars.aplicacao_id or 0)
   else:
       idaplicacao = int(session.aplicacao_id      or 0)
   if  session.aplicacao_id <> idaplicacao:
       session.aplicacao_id  = idaplicacao
       redirect(URL('index'))
   else:
       aplicacao = str(utl.Select(db,
                                  name='aplicacao_id',
                                  table='aplicacoes',
                                  fields=['id','descricao'],
                                  filtro='' if (auth.user) and \
                                               (auth.has_membership(1, \
                                                auth.user.id, \
                                                'Administrador')) \
                                            else db['aplicacoes'].\
                                                 empresa==auth.user.\
                                                 empresa,
                                  value=idaplicacao))
   return dict({'mensagens': session.atualizarColunasEntidades or [], \
                   'aplicacao': aplicacao})

@auth.requires_login()
def clear():
   session.atualizarColunasEntidades = []
   redirect(URL('index'))

@auth.requires_login()
def aplicar():
   iAce = ColunasEntidades(db, cAppl=session.aplicacao_id)
   rAce = iAce.updateColunasEntidadesBycAppl()
   pgm  = []
   for line in rAce[1].split('\n'):
       if  line:
           pgm.append(line)
   session.atualizarColunasEntidades = pgm
   redirect(URL('index'))
