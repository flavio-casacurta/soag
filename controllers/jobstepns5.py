# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idsrt               = request.args(0)
    form                = SQLFORM(sortnens5, idsrt, deletable=True)
    form.vars.sortnens4 = request.vars.sortnens4 = session.codigoSortnens4
    form.vars.campo     = request.vars.campo
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Include Excluido'
            redirect(URL('index'))
        else:
            if  idsrt:
                session.flash = 'Include Alterado'
                redirect(URL('index', args=(idsrt)))
            else:
                session.flash = 'Include Incluído'
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
    if  not session.codigoSortnens:
        query = sortnens5.sortnens4==0
    else:
        query = sortnens5.sortnens4==session.codigoSortnens4
    return dict(listdetail.index(['Includes'],
                                  'sortnens5', sortnens5,
                                  query,
                                  form, fields=['id', 'tipo', 'campo',\
                                                'operacao','valor'],
                                  scroll=['5%','15%','50%','15%','15%'],
                                  noDetail=['sortnens4'],
                                  search=['tipo', 'campo','operacao','valor'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('sortnens5', sortnens5)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sortnens5', sortnens5)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoSortnens4 else 'sortnens4==%d' % \
                      session.codigoSortnens4
    return listdetail.search('sortnens5', sortnens5, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Includes"
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
