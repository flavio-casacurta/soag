# coding: utf8

from Aplicacao import Aplicacao
from CheckListPrototipo import CheckListPrototipo
from CreateDB import CreateDB
from CreateMenu import CreateMenu
from CreateController import CreateController
from DumpUsers import DumpUsers
from DumpMsg import DumpMsg

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
    return dict({'mensagens': session.acessarMsgPrototipo or [], \
                 'aplicacao': aplicacao})

@auth.requires_login()
def clear():
    session.acessarMsgPrototipo = []
    redirect(URL('index'))

@auth.requires_login()
def acessar():

    if  len(db(db.menu.codigoAplicacao==session.aplicacao_id).select()) < 2:
        session.acessarMsgPrototipo = ['Menus nao foram Criados']
        redirect(URL('index'))

    if  len(db(db.userAplicacao.codigoAplicacao==session.aplicacao_id).select()) < 1:
        session.acessarMsgPrototipo = ['Usuarios nao foram Criados']
        redirect(URL('index'))

    checkListPrototipo = CheckListPrototipo(db, cAppl=session.aplicacao_id)

    if  not checkListPrototipo.getAplicacao():
        session.acessarMsgPrototipo = ['Aplicação nao foi Criada']
        redirect(URL('index'))

    if  not checkListPrototipo.getModel():
        createDB = CreateDB(db, cAppl=session.aplicacao_id, info=True).createDB()
        if  not createDB[0]:
            session.acessarMsgPrototipo = [createDB[1]]
            redirect(URL('index'))

    if  not checkListPrototipo.getMenus():
        createMenu = CreateMenu(db, cAppl=session.aplicacao_id, info=True).createMenu()
        if  not createMenu[0]:
            session.acessarMsgPrototipo = [createMenu[1]]
            redirect(URL('index'))

    if  not checkListPrototipo.getControllers():
        createController = CreateController(db, cAppl=session.aplicacao_id, info=True).createController()
        if  not createController[0]:
            session.acessarMsgPrototipo = [createController[1]]
            redirect(URL('index'))

    if  not checkListPrototipo.getUsers():
        dumpUsers = DumpUsers(db, cAppl=session.aplicacao_id, info=True).dumpUsers()
        if  not dumpUsers[0]:
            session.acessarMsgPrototipo = [dumpUsers[1]]
            redirect(URL('index'))

    if  not checkListPrototipo.getMensagens():
        dumpMsg = DumpMsg(db, cAppl=session.aplicacao_id, info=True).dumpMsg()
        if  not dumpMsg[0]:
            session.acessarMsgPrototipo = [dumpMsg[1]]
            redirect(URL('index'))

    redirect('../../{}/default/index'.format(Aplicacao(db,session.aplicacao_id).getApplId()))
