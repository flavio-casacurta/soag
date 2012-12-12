# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import LoadDB
import utilities as utl
import datetime
import erwin as modelo
import cPickle as pickle

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
    form = SQLFORM(erwins, iderwin, deletable=True,
                                      hidden=dict(codigoAplicacao=idaplicacao))
    if  not iderwin:
        erwins.nome.writable         = True
        erwins.arquivo.readable      = True
        erwins.arquivo.writable      = True
        form.vars.status             = request.vars.status = 2
        form.vars.mensagem           = 'Pendente de Importacao'
        form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = \
                                       auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        optionDelete                 = True \
                if (auth.user) and (auth.has_membership(1, auth.user.id, \
                                    'Administrador')) else False
    else:
        erwin = db(db[erwins].id==iderwin).select()[0]
        if  erwin.status == 5:
            erwins.nome.writable         = False
            erwins.arquivo.readable      = False
            erwins.arquivo.writable      = False
            optionDelete                 = False
            form = SQLFORM(erwins, iderwin)
        else:
            erwins.nome.writable         = True
            erwins.arquivo.readable      = True
            erwins.arquivo.writable      = True
            form.vars.status             = request.vars.status = 2
            form.vars.mensagem           = 'Pendente de Importacao'
            form.vars.usuarioConfirmacao = \
                        request.vars.usuarioConfirmacao = auth.user.id
            form.vars.dataConfirmacao    = datetime.datetime.today()
            optionDelete                 = True\
                if (auth.user) and (auth.has_membership(1, auth.user.id, \
                                    'Administrador')) else False
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Erwin Excluido'
            redirect(URL('index'))
        else:
            if  iderwin:
                session.flash  = 'Erwin Alterado'
                redirect(URL('index', args=(iderwin)))
            else:
                response.flash = 'Erwin Incluído'
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
                          (db.erwins.codigoAplicacao==idaplicacao)
    else:
        query = (db.erwins.id<0) \
                    if not idaplicacao else \
                          (db.erwins.codigoAplicacao==idaplicacao) & \
                          (db.erwins.status==idstatus)
    if  iderwin:
        buttonSelectProguess = [['Importar', URL('importar', args=(iderwin)),
                                             URL('index', args=(iderwin))]]
        parms = db(db.parametros.id == 1).select().first()
        arqui = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'private'
                            , 'erwin_%s.p' % iderwin)
        try:
            pickef = pickle.load(open(arqui, "rb"))
        except:
            pickef = None
    else:
        buttonSelectProguess = []
    if  iderwin and idstatus == 3:
        if  pickef:
            buttonSelectProguess.append(['Validar',
                                         'validar', '210', '350','300', '600'])
    if  iderwin and idstatus == 4:
        if  pickef:
            buttonSelectProguess.append(['Validar',
                                         'validar', '210', '350','300', '600'])
            buttonSelectProguess.append(['Processar',
                                              URL('processar', args=(iderwin)),
                                                 URL('index', args=(iderwin))])
    return dict(listdetail.index(['Erwin',
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
                                                table='statuserwin',
                                                fields=['id','descricao'],
                                                orderby='id',
                                                value=idstatus))],
                                 'erwins', erwins,
                                 query,
                                 form, fields=['id','nome','status'],
                                  noDetail=['codigoAplicacao',
                                            'nomeExterno1',
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
                                 buttonSubmit=True))

@auth.requires_login()
def importar():
    iderwin = request.args(0)
    if  not iderwin:
        session.flash = 'Nenhum erwin selecionado'
    else:
        prc = LoadDB.importarErwin(db, iderwin)
        if  prc['retorno']:
            db(db.erwins.id == iderwin).update(status=3,
                                               mensagem='Pendente Validacao',
                                               usuarioConfirmacao=auth.user.id,
                                     dataConfirmacao=datetime.datetime.today())
            session.status_id = 3
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
                            , 'erwin_%s.p' % iderwin)
        pickle.dump(prc['erwin'], open(arqui, "wb"))

@auth.requires_login()
def validar():
    iderwin = session.get('iderwin', 0)
    if  iderwin:
        session.reload = True
        session.href   = ''
        redirect('../validarerwin/index/%s' % iderwin)
    else:
        redirect(URL('index'))

@auth.requires_login()
def processar():
    iderwin = request.args(0)
    if  not iderwin:
        session.flash = 'Nenhum erwin selecionado'
    else:
        erwin = db(db.erwins.id == iderwin).select().first()
        if  erwin.status != 4:
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
                                , 'erwin_%s.p' % iderwin)
            try:
                pickef = pickle.load(open(arqui, "rb"))
            except:
                pickef = None
            loadDb = LoadDB.LoadDB(db, cAppl=session.aplicacao_id,
                                                              iderwin=iderwin)
            model  = modelo.Erwin()
            model.load(picke=pickef)
            prc    = loadDb.processarErwin(iderwin, auth.user.id, model)
            if  prc['retorno']:
                db(db.erwins.id == iderwin).update(status=5,
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

def uploader():
    nome = request.vars.Filedata.filename
    if  nome:
        parms = db(db.parametros.id==1).select().first()
        lines = request.vars.Filedata.file.read().replace('\r', '')
        crypt = utl.CryptFileName('erwins', 'arquivo', nome)
        arq   = os.path.join( '\\\\'
                            , '127.0.0.1'
                            , 'c$'
                            , parms.web2py
                            , 'applications'
                            , parms.soag
                            , 'uploads'
                            , crypt)
        with open(arq, 'w') as f1:
            f1.write(lines)
        db(db.erwins.insert(nome=nome.split('.')[0], arquivo=crypt,
                              status=2, mensagem='Pendente de Processamento.'))
    return True

@auth.requires_login()
def report():
    id    = request.args(0) or redirect(URL('index'))
    title = "Erwin"
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
