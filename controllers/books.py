# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import jobs
import datetime

@auth.requires_login()
def index():
    idbookcampo = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.codigoAplicacao or 0)
        idbook      = int(request.vars.book            or 0)
    else:
        idaplicacao = int(session.aplicacao_id         or 0)
        idbook      = int(session.book_id              or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    if  session.book_id <> idbook:
        session.book_id  = idbook
        redirect(URL('index'))
    if  not idaplicacao:
        idbook = session.book_id = 0
    form = SQLFORM(booksCampos, idbookcampo, deletable=True \
                if  (auth.user) and \
                    (auth.has_membership(1, auth.user.id, \
                            'Administrador')) \
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
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    query = booksCampos.book==0 if not idbook else \
                booksCampos.book==idbook
    if  idbook:
        book = db(db.books.id==idbook).select().first()
        if  book:
            buttonsAjax = [['Deletar Book', 'deletar o Book %s' % book.nome, \
                                         URL('deletarBook'), URL('index')]]
        else:
            buttonsAjax = []
    else:
        buttonsAjax = []
    return dict(listdetail.index(['Books',
                                  '<br/>Aplicacao:',
                                  str(utl.Select(db,
                                           name='codigoAplicacao',
                                           table='aplicacoes',
                                           fields=['id', \
                                                   'descricao'],
                                           value=idaplicacao)),
                                  '<br/>Book:',
                                  str(utl.Select(db,
                                           name='book',
                                           table='books',
                                           fields=['id','nome'],
                                           filtro=db['books'].\
                                               codigoAplicacao==\
                                                   idaplicacao,
                                           value=idbook)),
                                  'Tamanho: %s bytes' % str(\
                                    jobs.lreclBook(db, 'booksCampos', 'book', \
                                                  idbook)) if idbook else '',
                                  str(utl.buttonsAjax(buttonsAjax))],
                                  'booksCampos', booksCampos,
                                  query,
                                  form, fields=['id','nome','posicao',\
                                                'bytes','picture','tipo'],
                                  filtros=[['bytes', '>', '0']],
                                  scroll=['5%','35%','10%','10%','25%','15%'],
                                  noDetail=['codigoAplicacao','book',\
                                            'itemGrupo'],
                                  search=['nome'],
                                  optionDelete=True \
                                      if (auth.user) and \
                                         (auth.has_membership(1, \
                                          auth.user.id, \
                                         'Administrador')) \
                                      else False,
                                  buttonClear=True \
                                      if (auth.user) and \
                                         (auth.has_membership(1, \
                                          auth.user.id, \
                                         'Administrador')) \
                                      else False,
                                  buttonSubmit=True if idbookcampo else False))

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
    query = '' if not session.book_id else 'book==%d and bytes>0' % \
                    session.book_id
    return listdetail.search('booksCampos', booksCampos, query=query)

@auth.requires_login()
def deletarBook():
    book = db(db.books.id==session.book_id).select().first()
    db(db.booksCampos.book==session.book_id).delete()
    db(db.books.id==session.book_id).delete()
    session.flash = 'Book %s Excluido.' % book.nome
    return ''

@auth.requires_login()
def report():
    id    = request.args(0) or redirect(URL('index'))
    title = "Books"
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
