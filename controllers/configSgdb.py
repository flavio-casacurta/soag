# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import datetime
import utilities as utl
import Sqlalchemy as modelo

@auth.requires_login()
def index():
    iddatabase = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    form   = SQLFORM(database, iddatabase, deletable=True, hidden=dict(codigoAplicacao=idaplicacao))
    form.vars.usuarioConfirmacao = auth.user.id
    form.vars.dataConfirmacao    = datetime.datetime.today()
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
            session.flash  ='SGDB Excluido'
        else:
            if  iddatabase:
                session.flash  = 'SGDB Alterado'
                redirect(URL('index', args=(iddatabase)))
            else:
                response.flash = 'SGDB Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[database].id > 0

    query = ((db.database.id<0) if not idaplicacao else
                      (db.database.codigoAplicacao==idaplicacao))

    if  iddatabase:
        buttonSelectProguess = [['Testar Conexao', URL('testConn', args=(iddatabase)),
                                                   URL('index', args=(iddatabase))]]
    else:
        buttonSelectProguess = []
    return dict(listdetail.index(['SGDBs'
                                 '<br/>Aplicacao:',
                                 str(utl.Select(db,
                                 name='aplicacao_id',
                                 table='aplicacoes',
                                 fields=['id','descricao'],
                                 filtro='' \
                                 if (auth.user) and \
                                    (auth.has_membership(1, \
                                     auth.user.id, \
                                    'Administrador')) \
                                 else \
                                     db['aplicacoes'].empresa==\
                                         auth.user.empresa,
                                         value=idaplicacao))],
                'database', database,
                query,
                form, fields=['id', 'sgdbDB', 'userDB', 'hostDB', 'portDB', 'nameDB'],
                noDetail=['codigoAplicacao'],
                scroll=['5%','19%','19%','19%','19%','19%'],
                search=['sgdbDB'],
                optionDelete=True,
                buttonClear=False,
                buttonSelectProguess=buttonSelectProguess,
                buttonSubmit=True if idaplicacao else False))

@auth.requires_login()
def testConn():
    iddatabase = request.args(0) or 0
    idaplicacao = db(database.id==iddatabase).select().first().codigoAplicacao
    if  not idaplicacao:
        session.flash = 'Nenhuma Aplicacao selecionada'
    else:
        sqa = modelo.Sqlalchemy(db, cAppl=idaplicacao, info=True)
        resp, engine = sqa.tryEngine()
        if  resp:
            session.flash       = 'Conexao OK!'
            session.labelErrors = ''
            session.msgsErrors  = ''

        else:
            session.flash       = 'Erro de conexao!'
            session.labelErrors = 'Erro de conexao!'
            session.msgsErrors  = {1: engine}

@auth.requires_login()
def orderby():
    listdetail.orderby('database', database)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('database', database)
    redirect(URL('index'))

@auth.requires_login()
def search():
    return listdetail.search('database', database)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "SGDB"
    heading = "First Paragraph"
    text = 'bla ' * 100
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
