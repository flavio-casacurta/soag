# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idparametros = request.args(0)
    form         = SQLFORM(parametros, idparametros, deletable=False)
    if  form.accepts(request.vars, session):
        if  idparametros:
            session.flash = 'Parametro Alterado'
            redirect(URL('index', args=(idparametros)))
        else:
            response.flash = 'Parametro Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[parametros].id>0
    return dict(listdetail.index(['Parametros'],
                'parametros', parametros,
                query,
                form, fields=['id','raiz','web2py','soag','log'],
                scroll=['5%','30%','30%','14%','21%'],
                optionDelete=False,
                buttonClear=True,
                buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('parametros', parametros)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('parametros', parametros)
    redirect(URL('index'))

@auth.requires_login()
def search():
    return listdetail.search('parametros', parametros)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Parametros"
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
