# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idstep          = session.get('idstep', 0)
    regstep         = db(jobsteps.id==idstep).select().first()
    idhpu           = session.get('codigoHpus', 0)
    idsysin         = request.args(0)
    form            = SQLFORM(sysin, idsysin, deletable=False)
    form.vars.hpus  = request.vars.hpus = idhpu
    if  not idsysin:
        form.vars.nome2 = request.vars.nome2 = \
                                       session.get('rotine', 'ROT01') + 'S' + \
                                 '{:>02}'.format(regstep.step.split('STEP')[1])
    form.vars.sql = request.vars.sql = ''
    if  form.accepts(request.vars, session):
        if  idsysin:
            session.flash = 'Sysin DSN Alterada'
        else:
            idsysin       = form.vars.id
            session.flash = 'Sysin DSN Incluída'
        redirect(URL('index', args=(idsysin)))
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    if  not session.codigoHpus:
        query = sysin.hpus==0
    else:
        query = sysin.hpus==session.codigoHpus
    regstep = db(db.jobsteps.id==idstep).select().first()
    return dict(listdetail.index(['SYSIN DSN'],
                                  'sysin', sysin, query, form,
                                  noDetail=['hpus', 'sql'],
                                  noList=True,
                                  referback=['nome1'],
                                  optionDelete=False,
                                  buttonClear=False,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('sysin', sysin)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sysin', sysin)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoHpus else 'hpus==%d' % \
                      session.codigoHpus
    return listdetail.search('sysin', sysin, query=query)

@auth.requires_login()
def referback():
    return listdetail.referback(session.get('aplicacao_id', 0), \
                                session.get('idstep', 0), 'sysin', 'nome1')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Sysin"
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
