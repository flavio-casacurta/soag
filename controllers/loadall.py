# coding: utf8

import utilities as utl
import LoadDB

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
   return dict({'mensagens': session.msgloadall or [], 'aplicacao': aplicacao})

@auth.requires_login()
def clear():
   session.msgloadall = []
   redirect(URL('index'))

@auth.requires_login()
def aplicar():

   iLoad = LoadDB.LoadDB(db, cAppl=session.aplicacao_id)
   rLoad = iLoad.loadDB()

   msg  = []
   for lines in rLoad[1]:
       for line in lines.split('\n'):
           if  line:
               msg.append(line)
   session.msgloadall = msg
   redirect(URL('index'))
