# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idbookcampo = request.args(0)
    if  request.vars:
        idbook = int(request.vars.books_id or 0)
    else:
        idbook = session.book_id or 0
    if  session.book_id <> idbook:
        session.book_id  = idbook
        redirect(URL('index'))
    form = SQLFORM(booksCampos, idbookcampo, \
                   deletable=True\
                   if (auth.user) and \
                  (auth.has_membership(1, auth.user.id, 'Administrador'))\
                   else False)
    form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = \
                                   auth.user.id
    form.vars.dataConfirmacao    = request.vars.dataConfirmacao    = \
                                   datetime.datetime.today()
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and \
            request.vars.delete_this_record == 'on':
            response.flash = 'Campo Excluido'
        else:
            if  idbookcampo:
                session.flash  = 'Campo Alterado'
                redirect(URL('index', args=(idbookcampo)))
            else:
                response.flash = 'Campo Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[booksCampos].book==0\
            if not idbook else db[booksCampos].book==idbook
    return dict(listdetail.index(['Campos - Book:',
                                  str(utl.Select(db,
                                                 name='books_id',
                                                 table='books',
                                                 fields=['id','descricao'],
                                                 value=idbook))],
                                  'booksCampos', booksCampos,
                                  query,
                                  form, fields=['id','nome','natureza',\
                                                'tamanho','tipo'],
                                  scroll=['5%','45%','15%','15%','50%'],
                                  noDetail=['book'],
                                  search=['nome'],
                                  optionDelete=True\
                                  if (auth.user) and \
                                     (auth.has_membership(1, auth.user.id, \
                                      'Administrador'))\
                                  else False,
                                  buttonClear=True\
                                  if (auth.user) and \
                                     (auth.has_membership(1, auth.user.id, \
                                      'Administrador'))\
                                  else False,
                                  buttonSubmit=True\
                                  if idbookcampo else False))
                                  
@auth.requires_login()
def orderby():
    listdetail.orderby('booksCampos', booksCampos)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('booksCampos', booksCampos)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.book_id else 'book==%d' % session.book_id
    return listdetail.search('booksCampos', booksCampos, query=query)

@auth.requires_login()
def report():
    id    = request.args(0) or redirect(URL('index'))
    title = "Books Campos"
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
