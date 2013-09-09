# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import LoadDB
import utilities as utl
import datetime
import Sqlalchemy as modelo

@auth.requires_login()
def index():
    iderwin = request.args(0)
    if  iderwin:
        session.iderwin = iderwin
    else:
        session.iderwin = 0
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    if  request.vars:
        idstatus = int(request.vars.status_id or 2)
    else:
        idstatus = session.status_id or 2
    if  session.status_id <> idstatus:
        session.status_id  = idstatus
        redirect(URL('index'))
    if  not iderwin:
        erwins.nome.requires = IS_IN_DB(db(database.codigoAplicacao==session.aplicacao_id)
                                       ,database.nameDB
                                       ,'%(nameDB)s', zero='-- Selecione --')
    else:
        erwins.nome.writable = False

    erwins.lookups = {'status': ['statussgdb',  ['descricao']], \
                      'usuarioConfirmacao': ['auth_user', ['first_name','last_name']]}
    form = SQLFORM(erwins, iderwin, deletable=True,
                                      hidden=dict(codigoAplicacao=idaplicacao))
    if  not iderwin:
        form.vars.status             = request.vars.status = 2
        form.vars.mensagem           = 'Pendente de Teste de Conexao'
        form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        optionDelete                 = True if (auth.user) and (auth.has_membership(1, auth.user.id, 'Administrador')) else False
    else:
        sgdb = db(db.erwins.id==iderwin).select()[0]
        if  sgdb.status == 6:
            optionDelete                 = False
            form = SQLFORM(erwins, iderwin)
        else:
            erwins.nome.writable         = True
            form.vars.status             = request.vars.status = 2
            form.vars.mensagem           = 'Pendente de Teste de Conexao'
            form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = auth.user.id
            form.vars.dataConfirmacao    = datetime.datetime.today()
            optionDelete                 = True if (auth.user) and (auth.has_membership(1, auth.user.id, 'Administrador')) else False
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and request.vars.delete_this_record == 'on':
            session.flash = 'SGDB Excluido'
            redirect(URL('index'))
        else:
            if  iderwin:
                session.flash  = 'SGDB Alterado'
                redirect(URL('index', args=(iderwin)))
            else:
                response.flash = 'SGDB Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors         = session.msgsErrors
        session.msgsErrors  = None
    if  idstatus == 1:
        query = (db.erwins.id<0) \
                    if not idaplicacao else \
                          ((db.erwins.codigoAplicacao==idaplicacao) & (db.erwins.arquivo==''))
    else:
        query = (db.erwins.id<0) \
                    if not idaplicacao else ((db.erwins.codigoAplicacao==idaplicacao) &
                                            (db.erwins.arquivo=='') &
                                            (db.erwins.status==idstatus))
    parms = db(db.parametros.id == 1).select().first()
    arqui = os.path.join( '\\\\'
                        , '127.0.0.1'
                        , 'c$'
                        , parms.web2py
                        , 'applications'
                        , parms.soag
                        , 'private'
                        , 'sgdb_%s.pickle' % iderwin)
    try:
        session.pickef = utl.unPic(arqui)
    except:
        session.pickef = None
    buttonSelectProguess = []
    if  iderwin and sgdb.status == 2:
        buttonSelectProguess = [['Testar Conexao', URL('testConn', args=(iderwin)),
                                                   URL('index', args=(iderwin))]]
    if  iderwin and sgdb.status == 3:
        buttonSelectProguess = [['Importar', URL('importar', args=(iderwin)),
                                             URL('index', args=(iderwin))]]
    if  iderwin and sgdb.status == 4:
        if  session.pickef:
            buttonSelectProguess = [['Validar', 'validar', '210', '350','300', '600']]
    if  iderwin and sgdb.status == 5:
        if  session.pickef:
            buttonSelectProguess = [['Processar', URL('processar', args=(iderwin)),
                                                  URL('index', args=(iderwin))]]
    return dict(listdetail.index(['SGDB',
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
                                         value=idaplicacao)),
                                 'Status:',
                                 str(utl.Select(db,
                                                name='status_id',
                                                table='statussgdb',
                                                fields=['id','descricao'],
                                                orderby='id',
                                                value=idstatus))],
                                 'erwins', erwins,
                                 query,
                                 form, fields=['id','nome','status'],
                                 noDetail=['codigoAplicacao',
                                           'nomeExterno1',
                                           'arquivo',
                                           'default1',
                                           'nomeExterno2',
                                           'nomeExterno3',
                                           'default3'],
                                 scroll=['5%','60%','35%'],
                                 search=['nome','status'],
                                 optionDelete=optionDelete,
                                 buttonClear=True,
                                 buttonProcess=False,
                                 buttonSelectProguess=buttonSelectProguess,
                                 buttonSubmit=True if idaplicacao and idstatus else False))

@auth.requires_login()
def testConn():
    idaplicacao = session.aplicacao_id
    if  not idaplicacao:
        session.flash = 'Nenhuma Aplicacao selecionada'
    else:
        sqa = modelo.Sqlalchemy(db, cAppl=idaplicacao, info=True)
        resp, engine = sqa.tryEngine()
        if  resp:
            db(db.erwins.id == request.args(0)).update(status=3
                                                      ,mensagem='Pendente Importacao'
                                                      ,usuarioConfirmacao=auth.user.id
                                                      ,dataConfirmacao=datetime.datetime.today())
            session.status_id = 3
            session.flash       = 'Conexao OK!'
            session.labelErrors = ''
            session.msgsErrors  = ''

        else:
            session.flash       = 'Erro de conexao!'
            session.labelErrors = 'Erro de conexao!'
            session.msgsErrors  = {1: engine}

@auth.requires_login()
def importar():
    iderwin = request.args(0)
    if  not iderwin:
        session.flash = 'Nenhum SGDB selecionado'
    else:
        prc = LoadDB.importarSgdb(db, iderwin)
        if  prc['retorno']:
            db(db.erwins.id == iderwin).update(status=4,
                                               mensagem='Pendente Validacao',
                                               usuarioConfirmacao=auth.user.id,
                                     dataConfirmacao=datetime.datetime.today())
            session.status_id = 4
        session.flash       = prc['flash']
        session.labelErrors = prc['labelErrors']
        session.msgsErrors  = prc['msgsErrors']
        parms = db(db.parametros.id == 1).select().first()
        arqui = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'private'
                            , 'sgdb_%s.pickle' % iderwin)
        utl.pic(prc['sgdb'],arqui)

@auth.requires_login()
def validar():
    iderwin = session.get('iderwin', 0)
    if  iderwin:
        session.reload = True
        session.href   = ''
        redirect('../validarsgbd/index/%s' % iderwin)
    else:
        redirect(URL('index'))

@auth.requires_login()
def processar():
    iderwin = request.args(0)
    if  not iderwin:
        session.flash = 'Nenhum SGDB selecionado'
    else:
        sgdb = db(db.erwins.id == iderwin).select().first()
        if  sgdb.status != 5:
            session.flash = 'Para processamento, realize a validacao primeiro'
        else:
            parms = db(db.parametros.id == 1).select().first()
            arqui = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.web2py
                                , 'applications'
                                , parms.soag
                                , 'private'
                                , 'sgdb_%s.pickle' % iderwin)
            try:
                session.pickef = utl.unPic(arqui)
            except:
                session.pickef = None
            loadDb = LoadDB.LoadDB(db, cAppl=session.aplicacao_id, iderwin=iderwin)
            model  = modelo.Sqlalchemy(db, cAppl=None)
            model.load(picke=session.pickef)
            prc    = loadDb.processarSqlalchemy(model)
            if  prc['retorno']:
                db(db.erwins.id == iderwin).update(status=6,
                                            mensagem='Processamento Efetuado',
                                            usuarioConfirmacao=auth.user.id,
                                     dataConfirmacao=datetime.datetime.today())
                session.status_id = 2
            session.flash       = prc['flash']
            session.labelErrors = prc['labelErrors']
            session.msgsErrors  = prc['msgsErrors']

@auth.requires_login()
def orderby():
    listdetail.orderby('erwins', erwins)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('erwins', erwins)
    redirect(URL('index'))

@auth.requires_login()
def search():
    if not session.status_id:
       query = ''
    else:
       if  session.status_id == 1:
           query = ''
       else:
           query = 'status==%d' % session.status_id
    return listdetail.search('erwins', erwins, query=query)

@auth.requires_login()
def report():
    id    = request.args(0) or redirect(URL('index'))
    title = "SGDB"
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
