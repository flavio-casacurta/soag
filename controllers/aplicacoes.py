# coding: utf8

from gluon.contrib.pyfpdf import FPDF
from MensagensPadrao      import MensagensPadrao

import os, datetime

@auth.requires_login()
def index():
    idaplicacao = request.args(0)
    if  idaplicacao:
        session.aplicacao_id = idaplicacao
    form = SQLFORM(aplicacoes, idaplicacao, deletable=True,
               hidden=dict() if auth.user and \
                   auth.has_membership(1, auth.user.id, 'Administrador')
                       else dict(empresa=auth.user.empresa))
    delecaoLogica       = request.vars.delecaoLogica       or None
    colunaDelecaoLogica = request.vars.colunaDelecaoLogica or 0
    session.flash       = None
    if  delecaoLogica:
        if  colunaDelecaoLogica == '0':
            session.flash             = 'Coluna de Delecao Logica Invalida'
    if  not session.flash:
        form.vars.colunaDelecaoLogica = colunaDelecaoLogica
        form.vars.usuarioConfirmacao  = auth.user.id
        form.vars.dataConfirmacao     = datetime.datetime.today()
        if  form.accepts(request.vars, session):
            if  request.vars.has_key('delete_this_record') and \
                    request.vars.delete_this_record == 'on':
                session.flash = 'Aplicacao Excluida'
                redirect(URL('index'))
            else:
                if  idaplicacao:
                    session.flash = 'Aplicacao Alterada'
                    redirect(URL('index', args=(idaplicacao)))
                else:
                    idempresa   = form.vars.empresa
                    idaplicacao = form.vars.id
                    raiz  = db(db[parametros].id==1).select()[0].raiz
                    empr  = (db(db[empresa].id==idempresa).select()[0]
                                                        .nome.replace(' ', '_'))
                    try:
                        aplic = db(db[aplicacoes].id==\
                            idaplicacao).select()[0].aplicacao
                    except:
                        aplic = request.vars.aplicacao

                    listDir = [ ('DATAWORK'  , '')
                              , ('DCLGEN'    , '')
                              , ('DEFINICOES', '')
                              , ('GERADOS'   , 'CPY')
                              , ('GERADOS'   , 'HPU')
                              , ('GERADOS'   , 'IMGTB')
                              , ('GERADOS'   , 'LOG')
                              , ('GERADOS'   , 'PGM')
                              , ('SQL'       , '')
                              , ('UTL'       , '')]

                    for l in listDir:
                        a, b = l
                        try:
                            os.makedirs(os.path.join( '\\\\'
                                                    , '127.0.0.1'
                                                    , 'c$'
                                                    , raiz
                                                    , empr
                                                    , aplic
                                                    , a
                                                    , b))
                        except:
                            pass

                    mensagensPadrao = MensagensPadrao(db, cAppl=idaplicacao)
                    mensagensPadrao.criaMensagensPadrao()
                    db.checkList.insert(codigoAplicacao    = idaplicacao
                                       ,aplicacao          = False
                                       ,entidades          = False
                                       ,colunas            = False
                                       ,regrasColunas      = False
                                       ,origemColunas      = False
                                       ,colunasEntidades   = False
                                       ,mensagensEntidades = False
                                       ,programas          = False)
                    db.colunas.insert(codigoAplicacao = idaplicacao
                                     ,columnName      = 'NREG_QTDE'
                                     ,codigoDatatype  = 12
                                     ,tamanhoColuna   = 2
                                     ,decimais        = 0
                                     ,attributeName   = 'QUANTIDADE DE REGISTROS'
                                     ,label           = 'QUANTIDADE DE REGISTROS'
                                     ,descricao       = 'QUANTIDADE DE REGISTROS DEVOLVIDOS')
                    db.menu.insert(codigoAplicacao=idaplicacao
                                  ,parent=''
                                  ,descricao='Menu Principal'
                                  ,url='')
                    response.flash = 'Aplicacao Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  auth.user and auth.has_membership(1, auth.user.id, 'Administrador'):
        query = db[aplicacoes].id > 0
    else:
        if  auth.user:
            query = db[aplicacoes].empresa == auth.user.empresa
        else:
            query = db[aplicacoes].empresa == 0
    return dict(listdetail.index(['Aplicações'],
                'aplicacoes', aplicacoes,
                query,
                form, fields=['id','aplicacao','descricao'],
                noDetail=[] if auth.user and auth.has_membership(1, \
                                auth.user.id, 'Administrador') else ['empresa'],
                scroll=['5%','25%','70%'],
                width_label='35%',
                width_field='65%',
                search=['aplicacao','descricao'],
                optionDelete=True if (auth.user) and (auth.has_membership(1, \
                    auth.user.id, 'Administrador') or
                    auth.has_membership(2, auth.user.id, 'Super-Usuario')) \
                    else False,
                buttonClear=True if (auth.user) and (auth.has_membership(1, \
                    auth.user.id, 'Administrador') or
                    auth.has_membership(2, auth.user.id, 'Super-Usuario')) \
                    else False,
                buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('aplicacoes', aplicacoes)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('aplicacoes', aplicacoes)
    redirect(URL('index'))

@auth.requires_login()
def search():
    if  auth.user and auth.has_membership(1, auth.user.id, 'Administrador'):
        query = ''
    else:
        if  auth.user:
            query = 'empresa==%d' % auth.user.empresa
        else:
            query = 'empresa==0'
    return listdetail.search('aplicacoes', aplicacoes, query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Aplicações"
    heading = "First Paragraph"
    text = 'bla ' * 100
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times','B',15)
    pdf.cell(w=210,h=9,txt=title,border=0,ln=1,align='C',fill=0)
    pdf.set_font('Times','B',15)
    pdf.cell(w=0,h=6,txt=heading,border=0,ln=1,align='L',fill=0)
    pdf.set_font('Times','',12)
    pdf.multi_cell(w=0,h=5,txt=text)
    response.headers['Content-Type']='application/pdf'
    return pdf.output(name='report.pdf',dest='S')

@auth.requires_login()
def download():
    return response.download(request, db)
