# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idprog                  = request.args(0)
    session.codigoSortnens4 = idprog
    form                    = SQLFORM(sortnens4, idprog, deletable=True)
    form.vars.sortnens      = request.vars.sortnens = \
                                               session.get('codigoSortnens', 0)
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            db(db.sortnes5.sortnens4==idprog).delete()
            session.flash = 'Sortout Excluido'
            redirect(URL('index'))
        else:
            if  idprog:
                session.flash = 'Sortout Alterado'
                redirect(URL('index', args=(idprog)))
            else:
                session.flash = 'Sortout Incluído'
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
        query = sortnens4.sortnens==0
    else:
        query = sortnens4.sortnens==session.codigoSortnens
    buttons = []
    if  idprog:
        buttons.append(['Includes', 'includes', '180', '350','500', '600'])
    return dict(listdetail.index(['Sortout'],
                                  'sortnens4', sortnens4,
                                  query,
                                  form, fields=['id', 'nome1', 'nome2'],
                                  scroll=['5%','48%','47%'],
                                  noDetail=['sortnens'],
                                  search=['nome1', 'nome2'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True,
                                  buttons=buttons))

@auth.requires_login()
def orderby():
    listdetail.orderby('sortnens4', sortnens4)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sortnens4', sortnens4)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoSortnens else 'sortnens==%d' % \
                      session.codigoSortnens
    return listdetail.search('sortnens4', sortnens4, query=query)

@auth.requires_login()
def includes():
    redirect('../sortnens5/index')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Sortout"
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
