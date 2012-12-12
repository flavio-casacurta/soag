# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import jobs
import utilities as utl

@auth.requires_login()
def index():
    idhpu = request.args(0)
    if  idhpu:
        reghpus                = db(hpus.id==idhpu).select().first()
        session.codigoHpus     = idhpu
        session.jobRotine      = reghpus.jobRotine
    else:
        session.codigohpus     = 0
        session.jobRotine      = ''
    form  = SQLFORM(hpus, idhpu, deletable=True)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao            = int(session.aplicacao_id         or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    if  not idhpu and not request.vars.get('jobStep', ''):
        form.vars.jobStep  = 'STEP1'
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            db(db.sysin.hpus==idhpu).delete()
            session.flash = 'HPU Excluido'
            redirect(URL('index'))
        else:
            if  idhpu:
                session.flash = 'HPU Alterado'
                redirect(URL('index', args=(idhpu)))
            else:
                session.flash = 'HPU Incluído'
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
        query = hpus.codigoAplicacao==0
    else:
        query = hpus.codigoAplicacao==idaplicacao
    buttons = [['Sysin DSN', 'sysindsn', '70', '390','530', '600'],
               ['Sysin SQL', 'sysinsql', '70', '390','530', '600']]
    regsysin = db(db.sysin.hpus==idhpu).select().first()
    if  regsysin:
        buttons.append(['Gerar hpu', 'gerarhpu'])
    popups  = []
    if  idhpu and db(db.hpus.id==idhpu).select()[0].dataGeracao:
        popups.append(['Download', 'hpusd'])
    return dict(listdetail.index(['HPU',
                  '<br/>Aplicacao:',
                  str(utl.Select(db,
                           name='codigoAplicacao',
                           table='aplicacoes',
                           fields=['id','descricao'],
                           filtro='' if (auth.user) and \
                                        (auth.has_membership(1, auth.user.id, \
                                            'Administrador')) else
                                        aplicacoes.empresa==auth.user.empresa,
                           value=session.aplicacao_id or 0))],
                  'hpus', hpus,
                  query,
                  form, fields=['id', 'codigoEntidade', 'jobName', \
                                'jobRotine', 'jobUser'],
                  scroll=['5%','24%','24%','24%','23%'],
                  noDetail=['codigoAplicacao'],
                  search=['codigoEntidade', 'jobName', 'jobRotine', 'jobUser'],
                  optionDelete=True,
                  buttonClear=True,
                  buttonSubmit=True,
                  buttons=buttons,
                  popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('hpus', hpus)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('hpus', hpus)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('hpus', hpus, query=query)

@auth.requires_login()
def gerarhpu():
    idhpu = request.args(0) or redirect(URL('index'))
    hpu   = jobs.gerarhpu(db, idhpu, auth.user.id)
    session.flash       = hpu['flash']
    session.labelErrors = hpu['labelErrors']
    session.msgsErrors  = hpu['msgsErrors']
    redirect(URL('index', args=(idhpu)))

@auth.requires_login()
def sysindsn():
    idhpu    = session.get('codigoHpus', 0)
    regsysin = db(db.sysin.hpus==idhpu).select().first()
    if  idhpu:
        if  regsysin:
            redirect('../sysindsn/index/%s' % regsysin.id)
        else:
            redirect('../sysindsn/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def sysinsql():
    idhpu    = session.get('codigoHpus', 0)
    regsysin = db(db.sysin.hpus==idhpu).select().first()
    if  idhpu:
        if  regsysin:
            redirect('../sysinsql/index/%s' % regsysin.id)
        else:
            redirect('../sysinsql/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def hpusd():
    idhpu         = request.args(0) or redirect(URL('index'))
    parms         = db(db.parametros.id==1).select().first()
    reghpu        = db(db.hpus.id==idhpu).select().first()
    aplicacao     = db(db.aplicacoes.id==reghpu.codigoAplicacao).select().\
                                                                        first()
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select().first()
    gerhpu        = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'HPU') + os.sep
    filehpu       = '%s.jcl' % reghpu.jobName
    return listdetail.download(request, response, gerhpu, filehpu)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "HPUS"
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
