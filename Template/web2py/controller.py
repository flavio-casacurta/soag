# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    id@entidade = request.args(0)
    form = SQLFORM(@entidade, id@entidade, deletable=True)
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
            response.flash = '@Entidade Excluida'
        else:
            if  id@entidade:
                session.flash  = '@Entidade Alterada'
                redirect(URL('index', args=(id@entidade)))
            else:
                response.flash = '@Entidade Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[@entidade].id > 0
    return dict(listdetail.index(['@Entidade'],
                '@entidade', @entidade,
                query,
                form, fields=['id','@campo'],
                scroll=['5%','95%'],
                search=['@campo'],
                optionDelete=True,
                buttonClear=True,
                buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('@entidade', @entidade)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('@entidade', @entidade)
    redirect(URL('index'))

@auth.requires_login()
def search():
    return listdetail.search('@entidade', @entidade)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = '@Entidade'
    heading = 'First Paragraph' 
    text = 'Second Paragraph'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Times','B',15)
    pdf.cell(w=210,h=9,txt=title,border=0,ln=1,align='C',fill=0)
    pdf.set_font('Times','B',15)
    pdf.cell(w=0,h=6,txt=heading,border=0,ln=1,align='L',fill=0)
    pdf.set_font('Times','',15)
    pdf.cell(w=0,h=6,txt=text,border=0,ln=1,align='L',fill=0)
    response.headers['Content-Type']='application/pdf'
    return pdf.output(name='report.pdf',dest='S')

@auth.requires_login()
def download():
    return response.download(request, db)
