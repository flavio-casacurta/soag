# coding: utf8

from gluon.contrib.pyfpdf import FPDF
from sqlhpu import Sql

@auth.requires_login()
def index():
    idhpu           = session.get('codigoHpus', 0)
    reghpu          = db(db.hpus.id==idhpu).select().first()
    idsysin         = request.args(0)
    form            = SQLFORM(sysin, idsysin, deletable=False)
    form.vars.hpus  = request.vars.hpus  = idhpu
    form.vars.nome1 = request.vars.nome1 = ''
    form.vars.nome2 = request.vars.nome2 = ''
    form.vars.nome3 = request.vars.nome3 = ''
    if  idsysin:
        regsysin = db(db.sysin.id==idsysin).select().first()
        if  not regsysin.sql:
            sqL = Sql()
            form.vars.sql = request.vars.sql = \
                                  sqL.getTableSelect(db, reghpu.codigoEntidade)
    else:
        sqL = Sql()
        form.vars.sql = request.vars.sql = \
                                  sqL.getTableSelect(db, reghpu.codigoEntidade)

    if  form.accepts(request.vars, session):
        if  idsysin:
            session.flash = 'Sysin SQL Alterada'
        else:
            idsysin       = form.vars.id
            session.flash = 'Sysin SQL Incluída'
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
    return dict(listdetail.index(['SYSIN SQL'],
                                  'sysin', sysin, query, form,
                                  noDetail=['hpus', 'nome1', 'nome2', 'nome3'],
                                  noList=True,
                                  optionDelete=False,
                                  buttonClear=False,
                                  buttonSubmit=True))

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
