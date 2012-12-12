# coding: utf8

from   Programas import *
import utilities as utl

@auth.requires_login()
def index():
   if  request.vars:
       idaplicacao = int(request.vars.aplicacao_id or 0)
   else:
       idaplicacao = int(session.aplicacao_id or 0)
   if  session.aplicacao_id <> idaplicacao:
       session.aplicacao_id  = idaplicacao
       redirect(URL('index'))
   else:
       aplicacao = str(utl.Select(db,
                            name='aplicacao_id',
                            table='aplicacoes',
                            fields=['id','descricao'],
                            filtro='' if (auth.user) and \
                                         (auth.has_membership(1, auth.user.id, \
                                         'Administrador')) \
                                      else \
                                          db['aplicacoes'].empresa==\
                                              auth.user.empresa,
                            value=idaplicacao))
   return dict({'mensagens': session.nomearProgramas or [], \
                'aplicacao': aplicacao})

@auth.requires_login()
def clear():
   session.nomearProgramas = []
   redirect(URL('index'))

@auth.requires_login()
def aplicar():

   programas  = Programas(db, cAppl=session.aplicacao_id)
   nomearPgms = programas.nomearProgramas()

   pgm  = []
   for line in nomearPgms[1].split('\n'):
       if  line:
           pgm.append(line)
   session.nomearProgramas = pgm
   redirect(URL('index'))
