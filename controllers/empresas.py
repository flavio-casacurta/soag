# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import datetime

@auth.requires_login()
def index():
    idempresa = request.args(0)
    form      = SQLFORM(empresa, idempresa, deletable=False)
    if  form.accepts(request.vars, session):
        if  idempresa:
            session.flash  = 'Empresa Alterada'
            redirect(URL('index', args=(idempresa)))
        else:
            response.flash = 'Empresa Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[empresa].id > 0
    return dict(listdetail.index(['Empresas'],
                'empresa', empresa,
                query,
                form, fields=['id','nome'],
                scroll=['5%','95%'],
                search=['nome'],
                optionDelete=False,
                buttonClear=True,
                buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('empresa', empresa)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('empresa', empresa)
    redirect(URL('index'))

@auth.requires_login()
def search():
    return listdetail.search('empresa', empresa)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Empresa"
    heading = "First Paragraph"
    text = 'bla ' * 100
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
