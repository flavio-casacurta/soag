# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idsrt                  = request.args(0)
    form                   = SQLFORM(sort2s, idsrt, deletable=True)
    form.vars.codigoSort1s = request.vars.codigoSort1s = session.codigoSort1s
    form.vars.campo        = request.vars.campo
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Field Excluido'
            redirect(URL('index'))
        else:
            if  idsrt:
                session.flash = 'Field Alterado'
                redirect(URL('index', args=(idsrt)))
            else:
                session.flash = 'Field Incluído'
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
    if  not session.codigoSort1s:
        query = sort2s.codigoSort1s==0
    else:
        query = sort2s.codigoSort1s==session.codigoSort1s
    return dict(listdetail.index(['Campos do Sort'],
                                  'sort2s', sort2s,
                                  query,
                                  form, fields=['id', 'campo', 'ordem'],
                                  scroll=['5%','48%','47%'],
                                  noDetail=['codigoSort1s'],
                                  search=['campo', 'ordem'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('sort2s', sort2s)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sort2s', sort2s)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoSort1s else 'codigoSort1s==%d' % \
                      session.codigoSort1s
    return listdetail.search('sort2s', sort2s, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Field"
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
