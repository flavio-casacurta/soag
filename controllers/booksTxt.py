# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import jobs
import datetime

@auth.requires_login()
def index():
    idbooktxt         = request.args(0)
    session.idbooktxt = idbooktxt
    if  request.vars:
        idaplicacao = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao = int(session.aplicacao_id         or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    if  request.vars:
        if  request.vars.action == 'select':
            redirect(URL('selecionar', args=(request.vars.chk_id)))
        idstatus = int(request.vars.status_id or 2)
    else:
        idstatus = session.status_id or 2
    if  session.status_id <> idstatus:
        session.status_id  = idstatus
        redirect(URL('index'))
    booksTxt.arquivo.parm = idaplicacao
    form = SQLFORM(booksTxt, idbooktxt, deletable=True)
    if  not idbooktxt:
        booksTxt.nome.writable       = True
        booksTxt.arquivo.readable    = True
        booksTxt.arquivo.writable    = True
        form.vars.status             = request.vars.status = 2
        form.vars.mensagem           = 'Pendente de Processamento.'
        form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = \
                  auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        optionDelete                 = True \
                if (auth.user)          and \
                   (auth.has_membership(1, auth.user.id, \
                       'Administrador')) \
                else False
    else:
        book = db(db.booksTxt.id==idbooktxt).select()[0]
        if  book.status == 3:
            booksTxt.nome.writable       = False
            booksTxt.arquivo.readable    = False
            booksTxt.arquivo.writable    = False
            optionDelete                 = False
            form = SQLFORM(booksTxt, idbooktxt)
        else:
            booksTxt.nome.writable       = True
            booksTxt.arquivo.readable    = True
            booksTxt.arquivo.writable    = True
            form.vars.status             = request.vars.status = 2
            form.vars.mensagem           = 'Pendente de Processamento.'
            form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = \
                    auth.user.id
            form.vars.dataConfirmacao    = datetime.datetime.today()
            optionDelete                 = True \
                    if (auth.user) and \
                       (auth.has_membership(1, auth.user.id, \
                           'Administrador')) \
                    else False
        idstatus = int(request.vars.status_id or 2)
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and   \
            request.vars.delete_this_record == 'on':
            session.flash = 'Book Excluido'
            redirect(URL('index'))
        else:
            if  idbooktxt:
                session.flash = 'Book Alterado'
                redirect(URL('index', args=(idbooktxt)))
            else:
                response.flash  = 'Book Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    if  not idaplicacao:
        query = booksTxt.codigoAplicacao==0
    else:
        if  idstatus == 1:
            query = booksTxt.codigoAplicacao==idaplicacao
        else:
            query = booksTxt.codigoAplicacao==idaplicacao
    if  not idaplicacao:
        noDetail=['*']
    else:
        noDetail=['codigoAplicacao']
    return dict(listdetail.index(['Books',
                                  '<br/>Aplicacao:',
                                  str(utl.Select(db,
                                           name='codigoAplicacao',
                                           table='aplicacoes',
                                           fields=['id','descricao'],
                                           value=session.aplicacao_id or 0)),
                                  '<br/>Status:',
                                  str(utl.Select(db,
                                           name='status_id',
                                           table='Status',
                                           fields=['id','descricao'],
                                           orderby='id',
                                           value=idstatus))],
                                  'booksTxt', booksTxt,
                                  query,
                                  form, fields=['id','nome','status'],
                                  filtros=[['status', idstatus]] \
                                              if  idstatus <> 1 else [],
                                  scroll=['5%','60%','35%'],
                                  noDetail=noDetail,
                                  search=['nome','status'],
                                  optionDelete=optionDelete,
                                  buttonClear=True \
                                      if (auth.user) and \
                                         (auth.has_membership(1, auth.user.id,\
                                              'Administrador')) \
                                      else False,
                                  buttonProcess=False,
                                  buttonSelect=True \
                                      if (idstatus<>3 and \
                                          db(db.booksTxt.status==2).count())  \
                                      else False,
                                  buttonSubmit=True if idaplicacao and idstatus else False))

@auth.requires_login()
def processar():
    imp = jobs.booksImport(request.args, db, request.folder, \
                           session.aplicacao_id, auth.user.id)
    session.flash       = imp['flash']
    session.labelErrors = imp['labelErrors']
    session.msgsErrors  = imp['msgsErrors']
    if  not imp['retorno']:
        redirect(URL('index', args=(session.idbooktxt)))
    redirect(URL('index'))

@auth.requires_login()
def selecionar():
    chks = request.args or ['']
    if  not chks[0]:
        session.flash = 'Nenhum book selecionado'
        redirect(URL('index', args=(session.idbooktxt)))
    else:
        redirect(URL('processar', args=(chks)))

@auth.requires_login()
def orderby():
    listdetail.orderby('books', books)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('books', books)
    redirect(URL('index'))

@auth.requires_login()
def search():
    if  not session.status_id:
        query = ''
    else:
       if  session.status_id == 1:
           query = ''
       else:
           if  not session.aplicacao_id:
               query = ''
           else:
               query = '(codigoAplicacao==%d) & (status==%d)' % \
                               (session.aplicacao_id, session.status_id)
    return listdetail.search('books', books, query=query)

def uploader():
    parm = int(request.args(0) or 0)
    nome = request.vars.Filedata.filename
    if  nome and parm:
        parms = db(db.parametros.id==1).select().first()
        lines = request.vars.Filedata.file.read()
        crypt = utl.CryptFileName('booksTxt', 'arquivo', nome)
        arq   = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'uploads'
                            , crypt)
        with open(arq, 'w') as f1:
            f1.write(lines.replace('\r', ''))
        db(db.booksTxt.insert(codigoAplicacao=parm, \
                              nome=nome.split('.')[0], arquivo=crypt, \
                              status=2, mensagem='Pendente de Processamento.'))
    return True

@auth.requires_login()
def report():
    id    = request.args(0) or redirect(URL('index'))
    title = "Books txt"
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

# vim: ft=python
