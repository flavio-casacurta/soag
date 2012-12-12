# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idjob = session.get('idjob', 0)
    idhpu = request.args(0)
    if  idhpu:
        reghpus            = db(hpus.id==idhpu).select().first()
        session.codigoHpus = idhpu
        session.jobRotine  = reghpus.jobRotine
    else:
        session.codigohpus = 0
        session.jobRotine  = ''
    idaplicacao = int(session.aplicacao_id or 0)
    identidade  = int(request.vars.codigoEntidade or 0)
    form        = SQLFORM(hpus, idhpu, deletable=False)
    form.vars.codigoAplicacao = request.vars.codigoAplicacao = idaplicacao
    form.vars.jobStep         = request.vars.jobStep         = \
                                                 session.get('step',   'STEP1')
    form.vars.jobName         = request.vars.jobName         = \
                                              session.get('name',   'JOB00001')
    form.vars.jobRotine       = request.vars.jobRotine       = \
                                              session.get('rotine', 'ROT01')
    form.vars.jobUser         = request.vars.jobUser         = \
                                              session.get('usuario','USR00001')
    if  form.accepts(request.vars, session):
        if  idhpu:
            session.flash = 'HPU Alterado'
        else:
            idstep = session.get('idstep', 0)
            idhpu  = form.vars.id
            reghpu = db(db.hpus.id==idhpu).select().first()
            regent = db(db.entidades.id==reghpu.codigoEntidade).\
                                                               select().first()
            if  regent:
                db(jobsteps.id==idstep).update(idObjeto=idhpu, \
                  dsObjeto='(%s) %s' % (regent.nomeExterno, regent.nomeFisico))
            else:
                db(jobsteps.id==idstep).update(idObjeto=idhpu)
            session.flash = 'HPU Incluído'
        redirect(URL('index', args=(idhpu)))
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
    buttons = [['Sysin DSN', 'sysindsn', '140', '350','530', '1500'],
               ['Sysin SQL', 'sysinsql', '140', '350','530', '1500']]
    popups  = []
    return dict(listdetail.index(['HPU'],
                  'hpus', hpus, query, form,
                  noDetail=['codigoAplicacao','jobStep','jobName',\
                            'jobRotine','jobUser','usuarioGeracao',\
                            'dataGeracao'],
                  noList=True,
                  optionDelete=False,
                  buttonClear=False,
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
def sysindsn():
    idhpu    = session.get('codigoHpus', 0)
    regsysin = db(db.sysin.hpus==idhpu).select().first()
    if  idhpu:
        if  regsysin:
            redirect('../jobstephpusysindsn/index/%s' % regsysin.id)
        else:
            redirect('../jobstephpusysindsn/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def sysinsql():
    idhpu    = session.get('codigoHpus', 0)
    regsysin = db(db.sysin.hpus==idhpu).select().first()
    if  idhpu:
        if  regsysin:
            redirect('../jobstephpusysinsql/index/%s' % regsysin.id)
        else:
            redirect('../jobstephpusysinsql/index')
    else:
        redirect(URL('index'))

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
