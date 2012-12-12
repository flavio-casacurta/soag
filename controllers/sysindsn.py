# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idhpu          = session.get('codigoHpus', 0)
    reghpu         = db(db.hpus.id==idhpu).select().first()
    idsysin        = request.args(0)
    form           = SQLFORM(sysin, idsysin, deletable=True)
    form.vars.hpus = request.vars.hpus = idhpu
    form.vars.sql  = request.vars.sql  = ''
    if  not idsysin:
        if  not request.vars.nome2:
            form.vars.nome2 = request.vars.nome2 = reghpu.jobRotine + 'S' + \
                               '{:>02}'.format(reghpu.jobStep.split('STEP')[1])
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Sysin DSN Excluida'
            redirect(URL('index'))
        else:
            if  idsysin:
                session.flash = 'Sysin DSN Alterada'
                redirect(URL('index', args=(idsysin)))
            else:
                session.flash = 'Sysin DSN Incluída'
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
    if  not session.codigoHpus:
        query = sysin.hpus==0
    else:
        query = sysin.hpus==session.codigoHpus
    return dict(listdetail.index(['Sysin DSN'],
                                  'sysin', sysin,
                                  query,
                                  form, fields=['id', 'nome1', 'nome2', \
                                                'nome3'],
                                  scroll=['5%','32%','32%','31%'],
                                  noDetail=['hpus', 'sql'],
                                  search=['nome1', 'nome2', 'nome3'],
                                  optionDelete=True,
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
