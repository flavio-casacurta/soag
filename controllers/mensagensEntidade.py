# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime
from MensagensPadrao    import MensagensPadrao

@auth.requires_login()
def index():
    idmensagensEntCol  = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    else:
        db.mensagensEntCol.codigoEntCol.label      = 'Entidade'
        db.mensagensEntCol.codigoEntCol.where      = [entidades.codigoAplicacao==idaplicacao]
        db.mensagensEntCol.codigoEntCol.lookup     = [db, 'entidades', ['(','nomeExterno',')', ' ', 'nomeFisico']]
        db.mensagensEntCol.codigoEntCol.orderby    = db.entidades.nomeExterno
        db.mensagensEntCol.codigoEntCol.widget     = widgets.selectdb

        db.mensagensEntCol.codigoRegra.label       = 'Função'
        db.mensagensEntCol.codigoRegra.lookup      = [db, 'regras', 'descricao']
        db.mensagensEntCol.codigoRegra.where       = [((regras.visivel==True) & (regras.tipoPrograma==1))]
        db.mensagensEntCol.codigoRegra.join        = [['origemMensagens', 'origem', [['origem', 'E']]]]
        db.mensagensEntCol.codigoRegra.widget      = widgets.selectdb

        db.mensagensEntCol.lookups                 = {'codigoEntCol':['entidades', ['(', 'nomeExterno',
                                                   ') ', 'nomeFisico'], False]
                                                     ,'codigoTipoMsg':['tipoMensagens',['descricao'], False]
                                                     ,'codigoRegra':['regras',['descricao'], False]
                                                     ,'usuarioConfirmacao':['auth_user', ['first_name','last_name']]}

        form = SQLFORM(mensagensEntCol, idmensagensEntCol, deletable=True \
                            if (auth.user) and (auth.has_membership(1, \
                                auth.user.id, 'Administrador')) \
                            else False, \
                        hidden=dict(codigoAplicacao=idaplicacao))

        form.vars.codigoOrigemMsg  = request.vars.codigoOrigemMsg  = 1

        if  (request.vars and
             request.vars.codigoTipoMsg and
             request.vars.codigoRegra):

            form.vars.codigoEntCol     = request.vars.codigoEntCol
            form.vars.codigoTipoMsg    = request.vars.codigoTipoMsg
            form.vars.codigoRegra      = request.vars.codigoRegra

            msgPadrao = MensagensPadrao(db, cAppl=idaplicacao)
            codigoMsgPadrao = msgPadrao.selectMensagenPadraoByDados(request.vars.codigoOrigemMsg
                                                                   ,request.vars.codigoTipoMsg
                                                                   ,request.vars.codigoRegra)
            form.vars.codigoMsgPadrao = request.vars.codigoMsgPadrao = codigoMsgPadrao.id

        form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = request.vars.dataConfirmacao    = datetime.datetime.today()
        if  form.accepts(request.vars, session):

            db(db.checkListPrototipo.codigoAplicacao==idaplicacao).update(mensagens = False)

            if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
                session.flash = 'Mensagem Excluida'
                redirect(URL('index'))
            else:
                if  idmensagensEntCol:
                    session.flash  = 'Mensagem Alterada'
                    redirect(URL('index', args=(idmensagensEntCol)))
                else:
                    response.flash = 'Mensagem Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[mensagensEntCol].codigoAplicacao<0 \
                if  not idaplicacao else \
                    ((db[mensagensEntCol].codigoAplicacao==idaplicacao)
                    &(db[mensagensEntCol].codigoOrigemMsg==1))
    return dict(listdetail.index(['Mensagens Entidade',
                    '<br/>Aplicacao:',
                    str(utl.Select(db,
                                   name='aplicacao_id',
                                   table='aplicacoes',
                                   fields=['id','descricao'],
                                   filtro='' if (auth.user) and \
                                                (auth.has_membership(1, \
                                                 auth.user.id, \
                                                'Administrador')) \
                                             else db['aplicacoes'].\
                                                  empresa==auth.user.\
                                                           empresa,
                                         value=session.aplicacao_id or 0))],
                    'mensagensEntCol', mensagensEntCol,
                    query,
                    form, fields=['id','codigoMensagem','codigoEntCol','codigoTipoMsg','codigoRegra'],
                    noDetail=['codigoAplicacao', 'codigoOrigemMsg', 'codigoMsgPadrao'],
                    scroll=['5%','10%','55%','15%','15%'],
                    search=['codigoMensagem','codigoEntCol'],
                    optionDelete=True if (auth.user) and \
                                         (auth.has_membership(1, auth.user.id, \
                                         'Administrador') \
                                      or  auth.has_membership(2, auth.user.id, \
                                      'Super-Usuario')) \
                                      else False,
                    buttonClear=True if (auth.user) and \
                                        (auth.has_membership(1, auth.user.id, \
                                        'Administrador') \
                                     or  auth.has_membership(2, auth.user.id, \
                                         'Super-Usuario')) \
                                     else False,
                    buttonSubmit=True if idaplicacao else False))

@auth.requires_login()
def orderby():
    listdetail.orderby('mensagensEntCol', mensagensEntCol)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('mensagensEntCol', mensagensEntCol)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = 'codigoAplicacao==0' if not session.aplicacao_id else \
            'codigoAplicacao==%d' % session.aplicacao_id
    return listdetail.search('mensagensEntCol', mensagensEntCol, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Regras Colunas"
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

# vim: ft=python
