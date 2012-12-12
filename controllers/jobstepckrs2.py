# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idprog                  = request.args(0)
    session.codigoProgckrs2 = idprog
    form                    = SQLFORM(progckrs2, idprog, deletable=False)
    form.vars.progckrs      = request.vars.progckrs = \
                                               session.get('codigoProgckrs', 0)
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Comentario Excluido'
            redirect(URL('index'))
        else:
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
    if  not session.get('codigoProgckrs', 0):
        query = progckrs2.progckrs==0
    else:
        query = progckrs2.progckrs==session.codigoProgckrs
    return dict(listdetail.index(['Comentarios'],
                                  'progckrs2', progckrs2,
                                  query, form,
                                  noDetail=['progckrs'],
                                  search=['comentario'],
                                  optionDelete=False,
                                  buttonClear=False,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('progckrs2', progckrs2)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('progckrs2', progckrs2)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoProgckrs else 'progckrs==%d' % \
                      session.codigoProgckrs
    return listdetail.search('progckrs2', progckrs2, query=query)

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
