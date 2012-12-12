# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idnens                  = session.get('codigoPrognens', 0)
    idprog                  = request.args(0)
    session.codigoSortnens4 = idprog
    form                    = SQLFORM(prognens4, idprog, deletable=True)
    form.vars.prognens      = request.vars.prognens = idnens
    regnens                 = db(prognens.id==idnens).select().first()
    if  not idprog:
        if  not request.vars.nome2:
            regnens         = db(prognens.id==idnens).select().first()
            form.vars.nome2 = request.vars.nome2 = regnens.jobRotine + 'S' + \
                              '{:>02}'.format(regnens.jobStep.split('STEP')[1])
        if  not request.vars.nome3:
            form.vars.nome3 = request.vars.nome3 = \
                                                 session.get('jobPrograma', '')
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Saida Excluida'
            redirect(URL('index'))
        else:
            if  idprog:
                session.flash = 'Saida Alterada'
                redirect(URL('index', args=(idprog)))
            else:
                session.flash = 'Saida Incluída'
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
    if  not session.codigoPrognens:
        query = prognens4.prognens==0
    else:
        query = prognens4.prognens==idnens
    return dict(listdetail.index(['Saida'],
                                  'prognens4', prognens4,
                                  query,
                                  form, fields=['id', 'book', 'nome1', \
                                                'nome2', 'nome3', \
                                                'nome4'],
                                  scroll=['5%','19%','19%','19%','19%','19%'],
                                  noDetail=['prognens'],
                                  search=['book',  'nome1', 'nome2', \
                                          'nome3', 'nome4'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('prognens4', prognens4)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('prognens4', prognens4)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoPrognens else 'prognens==%d' % \
                      session.codigoPrognens
    return listdetail.search('prognens4', prognens4, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Saidas"
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
