# coding: utf-8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl

@auth.requires_login()
def index():
    idmenu = request.args(0)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao            = int(session.aplicacao_id         or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    form = SQLFORM(menu, idmenu, deletable=True)
    if  form.vars.codigoAplicacao is None:
        form.vars.codigoAplicacao = request.vars.codigoAplicacao = idaplicacao
    if  form.vars.parent is None:
        form.vars.parent = request.vars.parent
    if  form.vars.url is None:
        form.vars.url = request.vars.url
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Menu Excluido'
            redirect(URL('index'))
        else:
            if  idmenu:
                session.flash  = 'Menu Alterado'
                redirect(URL('index', args=(idmenu)))
            else:
                response.flash = 'Menu Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    if  not idaplicacao:
        query = menu.codigoAplicacao==-1
    else:
        query = menu.codigoAplicacao==idaplicacao
    buttons = []
    popups  = []
    return dict(listdetail.index(['Menu',
                      '<br/>Aplicacao:',
                      str(utl.Select(db,
                                     name='codigoAplicacao',
                                     table='aplicacoes',
                                     fields=['id','descricao'],
                                     filtro='' \
                                     if (auth.user) and \
                                        (auth.has_membership(1, \
                                         auth.user.id, 'Administrador')) \
                                     else aplicacoes.empresa==\
                                          auth.user.empresa,
                                     value=session.aplicacao_id or 0))],
                      'menu', menu,
                      query,
                      form, fields=['id', 'parent', 'descricao', 'url'],
                      scroll=['5%','28%','28%','39%'],
                      noDetail=['codigoAplicacao'],
                      search=['parent', 'descricao', 'url'],
                      optionDelete=True,
                      buttonClear=True,
                      buttonSubmit=True,
                      buttons=buttons,
                      popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('menu', menu)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('menu', menu)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('menu', menu, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Imagem Tabela"
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


# vim: ft=python
