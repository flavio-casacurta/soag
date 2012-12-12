# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idprograma = request.args(0)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao or 0)
        identidade             = int(request.vars.codigoEntidade  or 0)
    else:
        idaplicacao            = int(session.aplicacao_id         or 0)
        identidade             = int(session.entidade_id          or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    if  session.entidade_id   <> identidade:
        session.entidade_id    = identidade
        redirect(URL('index'))
    form = SQLFORM(programas, idprograma, deletable=True)
    if  request.vars:
        form.vars.codigoRegra    = int(request.vars.codigoRegra or 0)
        form.vars.nomePrograma   = request.vars.nomePrograma    or ''
        form.vars.bookInterface  = request.vars.bookInterface   or ''
        form.vars.bookControle   = request.vars.bookControle    or ''
    form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = \
        auth.user.id
    form.vars.dataConfirmacao    = request.vars.dataConfirmacao    = \
        datetime.datetime.today()
    session.flash                = None
    aplicacao                    = db(db[aplicacoes].id==idaplicacao).select()
    if  aplicacao:
        if  aplicacao[0].soag:
            programas.bookInterface.writable = False
            programas.bookControle.writable  = False
        else:
            programas.bookInterface.writable = True
            programas.bookControle.writable  = True
            if  request.vars:
                if  len(request.vars.nomePrograma) <> 8:
                    session.flash = 'Nome do Programa deve ser completo'
                if  not request.vars.bookInterface:
                    session.flash = 'Book de Interface deve ser informado'
                if  not request.vars.bookControle:
                    session.flash = 'Book de Controle deve ser informado'
        if  not session.flash:
            entidade=db(db[entidades].id==identidade).select()
            if  entidade:
                if  (request.vars.codigoRegra == '1' and not \
                     entidade[0].pgmInclusao)  or \
                    (request.vars.codigoRegra == '2' and not \
                     entidade[0].pgmAlteracao) or \
                    (request.vars.codigoRegra == '3' and not \
                     entidade[0].pgmExclusao)  or \
                    (request.vars.codigoRegra == '4' and not \
                     entidade[0].pgmConsulta)  or \
                    (request.vars.codigoRegra == '5' and not \
                     entidade[0].pgmLista):
                    session.flash = \
                        'Regra deve estar de acordo com o declarado na entidade'
        if  not session.flash and not idprograma:
            programa=db(db[programas].nomePrograma==request.vars.nomePrograma).\
                        select()
            if  programa:
                session.flash = 'Ja existe um programa com este nome'
    bookSaida = {'1':False, '2':False, '3':False, '4':True, '5':True}
    if  request.vars.codigoRegra:
        form.vars.bookSaida = request.vars.bookSaida = \
                                    bookSaida[request.vars.codigoRegra]
    if  not session.flash:
        if  form.accepts(request.vars, session):
            if  ('delete_this_record' in request.vars) and \
                        request.vars.delete_this_record == 'on':
                session.flash = 'Nome do Programa Excluido'
                redirect(URL('index'))
            else:
                if  idprograma:
                    session.flash = 'Nome do Programa Alterado'
                    redirect(URL('index', args=(idprograma)))
                else:
                    response.flash = 'Nome do Programa Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  not idaplicacao or not identidade:
        query = db[programas].codigoAplicacao==0
    else:
        query = db[programas].codigoAplicacao==idaplicacao
    return dict(listdetail.index(['Nomear Programa',
                    '<br />Aplicacao:',
                    str(utl.Select(db,
                            name='codigoAplicacao',
                            table='aplicacoes',
                            fields=['id','descricao'],
                            filtro='' if (auth.user) and \
                                         (auth.has_membership(1, auth.user.id,\
                                         'Administrador')) \
                                      else db['aplicacoes'].empresa==\
                                              auth.user.empresa,
                            value=session.aplicacao_id or 0)),
                    '<br />Entidade:',
                    str(utl.Select(db,
                            name='codigoEntidade',
                            table='entidades',
                            fields=['id','nomeFisico'],
                            masks=[[],['nomeExterno','nomeFisico']],
                            filtro=db['entidades'].codigoAplicacao==idaplicacao,
                            value=session.entidade_id or 0))],
                    'programas', programas,
                    query,
                    form, fields=['id', 'codigoRegra', 'nomePrograma'],
                    filtros=[['codigoEntidade', identidade]],
                    scroll=['5%','48%','47%'],
                    noDetail=['codigoAplicacao', 'codigoEntidade', 'bookSaida'],
                    search=['codigoRegra', 'nomePrograma'],
                    optionDelete=True,
                    buttonClear=True,
                    buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('programas', programas)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('programas', programas)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('programas', programas, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Nomear Programa"
    heading = "First Paragraph"
    text = 'xpto ' * 100
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
