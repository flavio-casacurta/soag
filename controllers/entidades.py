# coding: cp1252

from   gluon.contrib.pyfpdf import FPDF
from   Gerpro               import *
import utilities as utl
import datetime

@auth.requires_login()
def index():
    identidade = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    session.entidade_id = identidade
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    else:
        session.entidade_id = identidade
        if  identidade and db(db[entidades].id==identidade).select()[0].geracao:
            entidades.geracao.readable    = True
            entidades.logGeracao.readable = True
            entidades.logGeracao.writable = True
        else:
            entidades.geracao.readable    = False
            entidades.logGeracao.readable = False
            entidades.logGeracao.writable = False
        form = SQLFORM(entidades, identidade, deletable=True \
                    if (auth.user) and \
                       (auth.has_membership(1, auth.user.id, 'Administrador')) \
                    else False,
                    hidden=dict(codigoAplicacao=idaplicacao))
        form.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        if  form.accepts(request.vars, session):
            if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
                session.flash = 'Entidade Excluida'
                redirect(URL('index'))
            else:
                if identidade:
                   session.flash  = 'Entidade Alterada'
                   redirect(URL('index', args=(identidade)))
                else:
                   response.flash = 'Entidade Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[entidades].codigoAplicacao==0 \
                if  not idaplicacao else \
                    db[entidades].codigoAplicacao==idaplicacao
    buttons = [['Gerar Servicos','servicos']]
    popups  = []
    if  identidade and db(db[entidades].id==identidade).select()[0].geracao:
        popups.append(['Download', 'zipFile'])
    return dict(listdetail.index(['Entidades'
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
                  'entidades', entidades,
                  query,
                  form, fields=['id','nomeExterno','nomeFisico','nomeAmigavel'],
                  scroll=['5%','15%','20%','60%'],
                  noDetail=['codigoAplicacao'],
                  keysCheckFields=['Coordenadores','Servicos'],
                  checkFields={'Coordenadores': [['Inclusão', \
                                                  'coordenadorInclusao'],
                                                 ['Alteração',\
                                                  'coordenadorAlteracao'],
                                                 ['Exclusão',
                                                  'coordenadorExclusao'],
                                                 ['Consulta', \
                                                  'coordenadorConsulta'],
                                                 ['Lista',    \
                                                  'coordenadorLista']],
                               'Servicos':      [['Inclusão', \
                                                  'pgmInclusao'],
                                                 ['Alteração',\
                                                  'pgmAlteracao'],
                                                 ['Exclusão', \
                                                  'pgmExclusao'],
                                                 ['Consulta', \
                                                  'pgmConsulta'],
                                                 ['Lista',    \
                                                  'pgmLista']]},
                  search=['nomeExterno','nomeFisico','nomeAmigavel'],
                  optionDelete=True \
                        if  (auth.user) and \
                            (auth.has_membership(1, auth.user.id, \
                            'Administrador') or
                             auth.has_membership(2, auth.user.id, \
                            'Super-Usuario')) \
                        else False,
                  buttonClear=True \
                        if  (auth.user) and \
                            (auth.has_membership(1, auth.user.id, \
                            'Administrador') or
                             auth.has_membership(2, auth.user.id, \
                             'Super-Usuario')) \
                        else False,
                  buttonSubmit=True,
                  buttons=buttons,
                  popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('entidades', entidades)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('entidades', entidades)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                    session.aplicacao_id
    return listdetail.search('entidades', entidades, query=query)

@auth.requires_login()
def report():
    id = request.args(0)
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

@auth.requires_login()
def servicos():
    checklist  = db(db[checkList].codigoAplicacao==session.aplicacao_id).\
                    select().first()
    if  not checklist.entidades:
        session.flash = 'Check List - Entidades - nao confirmado'
        redirect(URL('index', args=(session.entidade_id)))
    if  not checklist.colunas:
        session.flash = 'Check List - Colunas - nao confirmado'
        redirect(URL('index', args=(session.entidade_id)))
    if  not checklist.regrasColunas:
        session.flash = 'Check List - Regras Colunas - nao confirmado'
        redirect(URL('index', args=(session.entidade_id)))
    if  not checklist.origemColunas:
        session.flash = 'Check List - Origem Colunas - nao confirmado'
        redirect(URL('index', args=(session.entidade_id)))
    if  not checklist.colunasEntidades:
        session.flash = 'Check List - Colunas Entidades - nao Atualizado'
        redirect(URL('index', args=(session.entidade_id)))
    if  not checklist.mensagensEntidades:
        session.flash = 'Check List - Mensagens Entidades - nao criadas'
        redirect(URL('index', args=(session.entidade_id)))
    if  not checklist.programas:
        session.flash = 'Check List - Programas - nao nomeados'
        redirect(URL('index', args=(session.entidade_id)))

    identidade = request.args(0) or redirect(URL('index'))
#    entidade   = db(db[entidades].id==identidade).select()[0]
    userName   ='%s %s' % (auth.user.first_name, auth.user.last_name)

    soag      = Gerpro(db, sessionId = auth.user.id
                       , cAppl        = session.get('aplicacao_id',0)
                       , userName     = userName)

    gerpro     = soag.gerpro(identidade)

    if  gerpro[0]:
        session.flash = 'Servicos gerados com sucesso (RC: 0).'
        logFile       = os.path.join( '\\\\'
                                    , '127.0.0.1'
                                    , 'c$'
                                    , db(db[parametros].id==1).select()[0].log
                                    , 'gerpro_%s.log' % auth.user.id)
        logs          = open(logFile, 'r')
        log           = ''
        for logsl in logs:
            log += '%s' % logsl
        db(db[entidades].id==identidade).update(logGeracao=log,
                                             geracao=datetime.datetime.today())
    else:
        session.flash = 'Servicos n�o foram gerados (RC: %s).' % gerpro[1]

    redirect(URL('index', args=(identidade)))

@auth.requires_login()
def zipFile():
    identidade = request.args(0) or redirect(URL('index'))
    entidade   = db(db[entidades].id==identidade).select()[0]
    filedir    = os.path.join( '\\\\'
                             , '127.0.0.1'
                             , 'c$'
                             , db(db[parametros].id==1).select()[0].log) + os.sep
    filename   = '%s.zip' % entidade.nomeExterno
    db(db[entidades].id==identidade).update(logGeracao=\
            'Download efetuado em %s' % str(datetime.datetime.today())[:19])
    return listdetail.download(request, response, filedir, filename)
