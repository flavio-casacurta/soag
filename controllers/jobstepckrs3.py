# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idstep              = session.get('idstep', 0)
    regstep             = db(jobsteps.id==idstep).select().first()
    idckrs              = session.get('codigoProgckrs', 0)
    idprog              = request.args(0)
    form                = SQLFORM(progckrs3, idprog, deletable=True)
    form.vars.progckrs  = request.vars.progckrs = idckrs
    if  not idprog:
        if  request.vars.nome2 <> '*':
            form.vars.nome2 = request.vars.nome2 = \
                                       session.get('rotine', 'ROT01') + 'S' + \
                                 '{:>02}'.format(regstep.step.split('STEP')[1])
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Entrada Excluida'
            redirect(URL('index'))
        else:
            if  idprog:
                session.flash = 'Entrada Alterada'
                redirect(URL('index', args=(idprog)))
            else:
                session.flash = 'Entrada Incluída'
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
    if  not session.codigoProgckrs:
        query = progckrs3.progckrs==0
    else:
        query = progckrs3.progckrs==idckrs
    return dict(listdetail.index(['Entrada'],
                                  'progckrs3', progckrs3,
                                  query,
                                  form, fields=['id', 'nome1', 'nome2', \
                                                'nome3', 'nome4'],
                                  scroll=['5%','24%','24%','24%','23%'],
                                  noDetail=['progckrs'],
                                  search=['nome1', 'nome2', 'nome3', 'nome4'],
                                  referback=['nome2'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('progckrs3', progckrs3)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('progckrs3', progckrs3)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.codigoProgckrs else 'progckrs==%d' % \
                      session.codigoProgckrs
    return listdetail.search('progckrs3', progckrs3, query=query)

@auth.requires_login()
def referback():
    return listdetail.referback(session.get('aplicacao_id', 0), \
                                session.get('idstep', 0), 'progckrs3', 'nome2')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Entrada"
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
