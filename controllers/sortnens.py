# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import jobs
import utilities as utl

@auth.requires_login()
def index():
    idsrt = request.args(0)
    if  idsrt:
        regsortnens            = db(sortnens.id==idsrt).select().first()
        session.codigoSortnens = idsrt
        session.jobRotine      = regsortnens.jobRotine
        session.codigoBook     = regsortnens.book
    else:
        session.codigoSortnens = 0
        session.jobRotine      = ''
        session.codigoBook     = 0
    form = SQLFORM(sortnens, idsrt, deletable=True)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao            = int(session.aplicacao_id         or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    if  not idsrt and not request.vars.get('jobStep', ''):
        form.vars.jobStep      = request.vars.jobStep = 'STEP1'
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            db(db.sortnes5.sortnens4==idsrt).delete()
            db(db.sortnes4.sortnens==idsrt).delete()
            db(db.sortnes3.sortnens==idsrt).delete()
            db(db.sortnes2.sortnens==idsrt).delete()
            session.flash = 'SORT Excluido'
            redirect(URL('index'))
        else:
            if  idsrt:
                session.flash = 'SORT Alterado'
                redirect(URL('index', args=(idsrt)))
            else:
                session.flash = 'SORT Incluído'
                redirect(URL('index'))
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
        query = sortnens.codigoAplicacao==0
    else:
        query = sortnens.codigoAplicacao==idaplicacao
    buttons = [['Fields',     'sortnens2', '150', '390','450', '600'],
               ['Sortin',     'sortnens3',  '70', '370','570', '600'],
               ['Sortout',    'sortnens4', '120', '390','480', '600'],
               ['Gerar sort', 'gerarsort']]
    popups  = []
    if  idsrt and db(db.sortnens.id==idsrt).select()[0].dataGeracao:
        popups.append(['Download', 'sortnensd'])
    return dict(listdetail.index(['Sort Arquivo',
                    '<br/>Aplicacao:',
                    str(utl.Select(db,
                            name='codigoAplicacao',
                            table='aplicacoes',
                            fields=['id','descricao'],
                            value=session.aplicacao_id))],
                    'sortnens', sortnens,
                    query,
                    form, fields=['id', 'book', 'jobName', \
                                  'jobRotine', 'jobArqName'],
                    scroll=['5%','24%','24%','24%','23%'],
                    noDetail=['codigoAplicacao'],
                    search=['book', 'jobName', 'jobRotine', 'jobUser'],
                    optionDelete=True,
                    buttonClear=True,
                    buttonSubmit=True,
                    buttons=buttons,
                    popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('sortnens', sortnens)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sortnens', sortnens)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('sortnens', sortnens, query=query)

@auth.requires_login()
def gerarsort():
    idsrt = request.args(0) or redirect(URL('index'))
    jcl   = jobs.gerarsortnens(db, idsrt, auth.user.id)
    session.flash       = jcl['flash']
    session.labelErrors = jcl['labelErrors']
    session.msgsErrors  = jcl['msgsErrors']
    redirect(URL('index', args=(idsrt)))

@auth.requires_login()
def sortnensd():
    idsrt         = request.args(0) or redirect(URL('index'))
    parms         = db(db.parametros.id==1).select().first()
    regsrt        = db(db.sortnens.id==idsrt).select().first()
    aplicacao     = db(db.aplicacoes.id==regsrt.codigoAplicacao).\
                            select().first()
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select().first()
    gersrt        = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'SORTNENS') + os.sep
    filesrt       = '%s.jcl'                    % regsrt.jobName
    return listdetail.download(request, response, gersrt, filesrt)

@auth.requires_login()
def sortnens2():
    redirect('../sortnens2/index')

@auth.requires_login()
def sortnens3():
    redirect('../sortnens3/index')

@auth.requires_login()
def sortnens4():
    redirect('../sortnens4/index')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "SORT com uma saida"
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
