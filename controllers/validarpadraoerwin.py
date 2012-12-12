# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    iderwinent = request.args(0)
    iderwin    = session.get('iderwin', 0)
    form       = SQLFORM(db.erwinents, iderwinent, deletable=False)
    if  form.accepts(request.vars, session):
        session.flash = 'Entidade Alterada'
        redirect(URL('index', args=(iderwinent)))
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    if  not iderwin:
        query = db.erwinents.erwin==0
    else:
        query = db.erwinents.erwin==iderwin
    return dict(listdetail.index(['Entidades'],
                                  'erwinents', erwinents,
                                  query,
                                  form, fields=['id',
                                                'entidade',
                                                'nomeExterno1',
                                                'nomeExterno2'],
                                  scroll=['5%','37%','29%','29%'],
                                  width_label='35%',
                                  width_field='65%',
                                  noDetail=['erwin'],
                                  orderBy=['nomeExterno2', 'ASC'],
                                  search=['entidade',
                                          'nomeExterno1',
                                          'nomeExterno2'],
                                  optionDelete=False,
                                  buttonClear=False,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('erwinents', erwinents)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('erwinents', erwinents)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.iderwin else 'erwin==%d' % \
                      session.iderwin
    return listdetail.search('erwinents', erwinents, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Entidades"
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
