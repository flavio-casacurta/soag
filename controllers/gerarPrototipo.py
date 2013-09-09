# coding: utf8

from Aplicacao import Aplicacao
from CreateAplicacao import app_create
from CreateLoads import CreateLoads
from CreateLayout import CreateLayout
from CreateDB import CreateDB

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
    return dict({'mensagens': session.gerarMsgPrototipo or [], \
                 'aplicacao': aplicacao})

@auth.requires_login()
def clear():
    session.gerarMsgPrototipo = []
    redirect(URL('index'))

@auth.requires_login()
def aplicar():

    appCreate = app_create(db, Aplicacao(db, session.aplicacao_id).getApplId(), request, force=True, info=True)
    if  not appCreate[0]:
        session.gerarMsgPrototipo = [appCreate[1]]
        redirect(URL('index'))

    createLoads = CreateLoads(db, cAppl=session.aplicacao_id, info=True).createLoads()
    if  not createLoads[0]:
        session.gerarMsgPrototipo = [createLoads[1]]
        redirect(URL('index'))

    createLayout = CreateLayout(db, cAppl=session.aplicacao_id, info=True).createLayout()
    if  not createLayout[0]:
        session.gerarMsgPrototipo = [createLayout[1]]
        redirect(URL('index'))

    createDB = CreateDB(db, cAppl=session.aplicacao_id, createDataBase=True, info=True).createDB()
    if  not createDB[0]:
        session.gerarMsgPrototipo = [createDB[1]]
        redirect(URL('index'))

    db(db.checkListPrototipo.codigoAplicacao==session.aplicacao_id).update(aplicacao   = True
                                                                          ,menus       = False
                                                                          ,controllers = False
                                                                          ,users       = False
                                                                          ,mensagens   = False)
    session.gerarMsgPrototipo = ['Aplicação Criada com Sucesso']
    redirect(URL('index'))
