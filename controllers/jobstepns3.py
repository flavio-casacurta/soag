# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idstep              = session.get('idstep', 0)
    regstep             = db(jobsteps.id==idstep).select().first()
    idnens              = session.get('codigoSortnens', 0)
    regnens             = db(sortnens.id==idnens).select().first()
    idsrt               = request.args(0)
    form                = SQLFORM(sortnens3, idsrt, deletable=True)
    form.vars.sortnens  = request.vars.sortnens = idnens
    if  not idsrt:
        if  request.vars.nome1 <> '*':
            form.vars.nome1 = request.vars.nome1 = \
                                       session.get('rotine', 'ROT01') + 'S' + \
                                 '{:>02}'.format(regstep.step.split('STEP')[1])
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Sortin Excluido'
            redirect(URL('index'))
        else:
            if  idsrt:
                session.flash = 'Sortin Alterado'
                redirect(URL('index', args=(idsrt)))
            else:
                session.flash = 'Sortin Incluído'
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
        query = sortnens3.sortnens==0
    else:
        query = sortnens3.sortnens==session.codigoSortnens
    return dict(listdetail.index(['Sortin'],
                                  'sortnens3', sortnens3,
                                  query,
                                  form, fields=['id', 'nome1', \
                                                'nome2', 'nome3', 'nome4'],
                                  scroll=['5%','24%','24%','24%','23%'],
                                  noDetail=['sortnens'],
                                  search=['nome1', 'nome2', 'nome3', 'nome4'],
                                  referback=['nome1'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('sortnens3', sortnens3)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sortnens3', sortnens3)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoSortnens else 'sortnens==%d' % \
                      session.codigoSortnens
    return listdetail.search('sortnens3', sortnens3, query=query)

@auth.requires_login()
def referback():
    return listdetail.referback(session.get('aplicacao_id', 0), \
                                session.get('idstep', 0), 'sortnens3', 'nome1')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Sortin"
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
