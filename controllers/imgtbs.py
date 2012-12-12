# coding: utf-8

from   gluon.contrib.pyfpdf import FPDF
import jobs
import utilities as utl

@auth.requires_login()
def index():
    idimgtb = request.args(0)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao            = int(session.aplicacao_id         or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    form = SQLFORM(imgtbs, idimgtb, deletable=True)
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Imagem Tabela Excluida'
            redirect(URL('index'))
        else:
            if  idimgtb:
                session.flash  = 'Imagem Tabela Alterada'
                redirect(URL('index', args=(idimgtb)))
            else:
                response.flash = 'Imagem Tabela Incluída'
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
        query = imgtbs.codigoAplicacao==0
    else:
        query = imgtbs.codigoAplicacao==idaplicacao
    buttons = [['Gerar imagem tabela', 'gerarimgtb']]
    popups  = []
    if  idimgtb and db(db.imgtbs.id==idimgtb).select()[0].dataGeracao:
        popups.append(['Download', 'imgtbsd'])
    return dict(listdetail.index(['Imagem Tabela',
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
                      'imgtbs', imgtbs,
                      query,
                      form, fields=['id', 'codigoEntidade', 'bookName'],
                      scroll=['5%','70%','25%'],
                      noDetail=['codigoAplicacao'],
                      search=['codigoEntidade', 'bookName'],
                      optionDelete=True,
                      buttonClear=True,
                      buttonSubmit=True,
                      buttons=buttons,
                      popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('imgtbs', imgtbs)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('imgtbs', imgtbs)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('imgtbs', imgtbs, query=query)

@auth.requires_login()
def gerarimgtb():
    idimgtb = request.args(0) or redirect(URL('index'))
    imgtb   = jobs.gerarimgtb(db, idimgtb, request.folder, auth.user.id)
    session.flash       = imgtb['flash']
    session.labelErrors = imgtb['labelErrors']
    session.msgsErrors  = imgtb['msgsErrors']
    redirect(URL('index', args=(idimgtb)))

@auth.requires_login()
def imgtbsd():
    idimgtb       = request.args(0) or redirect(URL('index'))
    parms         = db(db.parametros.id==1).select()[0]
    regimgtb      = db(db.imgtbs.id==idimgtb).select()[0]
    aplicacao     = db(db.aplicacoes.id==regimgtb.codigoAplicacao).select()[0]
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select()[0]
    gerimgtb      = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'IMGTB') + os.sep
    fileimgtb     = '%s.cpy' % regimgtb.bookName
    return listdetail.download(request, response, gerimgtb, fileimgtb)

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
