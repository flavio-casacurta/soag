# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idprog                  = request.args(0)
    session.codigoPrognens2 = idprog
    form                    = SQLFORM(prognens2, idprog, deletable=False)
    form.vars.prognens      = request.vars.prognens = \
                                               session.get('codigoPrognens', 0)
    if  form.accepts(request.vars, session):
        if  idprog:
            session.flash = 'Comentario Alterado'
        else:
            idprog        = form.vars.id
            session.flash = 'Comentario Incluído'
        redirect(URL('index', args=(idprog)))
    if  session.get('flash', None):
        response.flash = session.flash
        session.flash  = None
    if  session.get('labelErrors', None):
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    if  not session.get('codigoPrognens', 0):
        query = prognens2.prognens==0
    else:
        query = prognens2.prognens==session.codigoPrognens
    return dict(listdetail.index(['Comentarios'],
                                  'prognens2', prognens2,
                                  query, form,
                                  noDetail=['prognens'],
                                  noList=True,
                                  optionDelete=False,
                                  buttonClear=False,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('prognens2', prognens2)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('prognens2', prognens2)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoPrognens else 'prognens==%d' % \
                      session.codigoPrognens
    return listdetail.search('prognens2', prognens2, query=query)

@auth.requires_login()
def report():
    id = request.args(0)
    if not id: redirect(URL('index'))
    title = "Comentarios"
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
