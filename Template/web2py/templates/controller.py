# coding: utf8

from gluon.contrib.pyfpdf import FPDF
from message import msgGet
@IMPORTS

@auth.requires_login()
def index():
    id@ENTIDADE = request.args(0)
    form = SQLFORM(@ENTIDADE, id@ENTIDADE@DELETABLE)
    session.flash = None
    if  not id@ENTIDADE:
        if  request.vars:
@INCLUSAO
    else:
        if  request.vars:
@ALTERACAO
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
            session.flash  = msgGet(db,'@MSGEXCLUIDA')
        else:
            if  id@ENTIDADE:
                session.flash  = msgGet(db,'@MSGALTERADA')
                redirect(URL('index', args=(id@ENTIDADE)))
            else:
                session.flash  = msgGet(db,'@MSGINCLUIDA')
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[@ENTIDADE]@QUERYID
    return dict(listdetail.index(['@LABEL'],
                '@ENTIDADE', @ENTIDADE,
                query,
                form, fields=[@FIELDSID@CAMPOS],
                scroll=[@SCROLL@LENGTHS],
                search=[@CAMPOS],
                optionDelete=@OPTIONDELETE,
                buttonClear=True,
                buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('@ENTIDADE', @ENTIDADE)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('@ENTIDADE', @ENTIDADE)
    redirect(URL('index'))

@auth.requires_login()
def search():
    return listdetail.search('@ENTIDADE', @ENTIDADE)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = '@LABEL'
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
