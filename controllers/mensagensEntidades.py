# coding: utf8

from   Mensagens import *
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
                                  else db['aplicacoes'].empresa==\
                                       auth.user.empresa,
                        value=idaplicacao))
   return dict({'mensagens': session.msgEntidades or [], \
                'aplicacao': aplicacao})

@auth.requires_login()
def clear():
   session.msgEntidades = []
   redirect(URL('index'))

@auth.requires_login()
def aplicar():

   mensagens  = Mensagens(db, cAppl=session.aplicacao_id)
   criaMsg    = mensagens.criaMensagensEntidades()

   msg  = []
   for line in criaMsg[1].split('\n'):
       if  line:
           msg.append(line)
   session.msgEntidades = msg
   redirect(URL('index'))
