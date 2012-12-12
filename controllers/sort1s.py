# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import jobs
import utilities as utl

@auth.requires_login()
def index():
    idsrt = request.args(0)
    if  idsrt:
        regsort1s = db(sort1s.id==idsrt).select().first()
        session.codigoEntidade = regsort1s.codigoEntidade
        session.codigoSort1s   = idsrt
    else:
        session.codigoEntidade = 0
        session.codigoSort1s   = 0
    form = SQLFORM(sort1s, idsrt, deletable=True)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao            = int(session.aplicacao_id         or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    if  not idsrt and not request.vars.get('jobStep', ''):
        form.vars.jobStep  = 'STEP1'
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            db(db.sort3s.codigoSort1s==idsrt).delete()
            db(db.sort2s.codigoSort1s==idsrt).delete()
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
        query = sort1s.codigoAplicacao==0
    else:
        query = sort1s.codigoAplicacao==idaplicacao
    buttons = [['Fields',     'sort2sb', '180', '350','460', '600'],
               ['Includes',   'sort3sb', '150', '310','500', '680'],
               ['Gerar sort', 'gerarsort']]
    fields  = db(db.sort2s.codigoSort1s==idsrt).select()
    popups  = []
    if  idsrt and db(db.sort1s.id==idsrt).select()[0].dataGeracao:
        popups.append(['Download', 'sort1sd'])
    return dict(listdetail.index(['Sort Tabela',
                    '<br/>Aplicacao:',
                    str(utl.Select(db,
                            name='codigoAplicacao',
                            table='aplicacoes',
                            fields=['id','descricao'],
                            value=session.aplicacao_id or 0))],
                    'sort1s', sort1s,
                    query,
                    form, fields=['id', 'codigoEntidade', 'jobName', \
                                  'jobRotine', 'jobUser'],
                    scroll=['5%','33%','21%','21%','20%'],
                    noDetail=['codigoAplicacao'],
                    search=['codigoEntidade', 'jobName', \
                            'jobRotine', 'jobUser'],
                    optionDelete=True,
                    buttonClear=True,
                    buttonSubmit=True,
                    buttons=buttons,
                    popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('sort1s', sort1s)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sort1s', sort1s)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('sort1s', sort1s, query=query)

@auth.requires_login()
def gerarsort():
    idsrt = request.args(0) or redirect(URL('index'))
    jcl   = jobs.gerarsort1s(db, idsrt, auth.user.id)
    session.flash       = jcl['flash']
    session.labelErrors = jcl['labelErrors']
    session.msgsErrors  = jcl['msgsErrors']
    redirect(URL('index', args=(idsrt)))

@auth.requires_login()
def sort1sd():
    idsrt         = request.args(0) or redirect(URL('index'))
    parms         = db(db.parametros.id==1).select().first()
    regsrt        = db(db.sort1s.id==idsrt).select().first()
    aplicacao     = db(db.aplicacoes.id==regsrt.codigoAplicacao).select().\
                            first()
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select()[0]
    gersrt        = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'SORT1S') + os.sep
    filesrt       = '%s.jcl'                  % regsrt.jobName
    return listdetail.download(request, response, gersrt, filesrt)

@auth.requires_login()
def sort2sb():
    redirect('../sort2s/index')

@auth.requires_login()
def sort3sb():
    redirect('../sort3s/index')

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
