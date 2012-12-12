# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idmensagensPadrao = request.args(0)
    if  idmensagensPadrao:
        msgp = db(db[mensagensPadrao].id==idmensagensPadrao).select().first()
        if  msgp:
            mensagensPadrao.codigoMsgPrefixo.filtro = \
                [['origem', '==', msgp.codigoOrigemMsg]]
            mensagensPadrao.codigoMsgSufixo.filtro  = \
                [['origem', '==', msgp.codigoOrigemMsg]]
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    else:
        form = SQLFORM(mensagensPadrao, idmensagensPadrao, deletable=True,
                            hidden=dict(codigoAplicacao=idaplicacao))
        form.vars.codigoRegra        = request.vars.codigoRegra
        form.vars.codigoOrigemMsg    = request.vars.codigoOrigemMsg
        form.vars.codigoMsgPrefixo   = request.vars.codigoMsgPrefixo
        form.vars.codigoMsgSufixo    = request.vars.codigoMsgSufixo
        form.vars.usuarioConfirmacao = request.vars.usuarioConfirmacao = \
                                            auth.user.id
        form.vars.dataConfirmacao    = request.vars.dataConfirmacao    = \
                                            datetime.datetime.today()
        if  form.accepts(request.vars, session):
            if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
                session.flash = 'Mensagem Padrao Excluida'
                redirect(URL('index'))
            else:
                if  idmensagensPadrao:
                    session.flash = 'Mensagem Padrao Alterada'
                    redirect(URL('index', args=(idmensagensPadrao)))
                else:
                    response.flash = 'Mensagem Padrao Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[mensagensPadrao].codigoAplicacao==0 \
                if not idaplicacao else \
                       db[mensagensPadrao].codigoAplicacao==idaplicacao
    return dict(listdetail.index(['Mensagem Padrao',
                    '<br/>Aplicacao:',
                    str(utl.Select(db,
                            name='aplicacao_id',
                            table='aplicacoes',
                            fields=['id','descricao'],
                            filtro='' if (auth.user) and \
                                         (auth.has_membership(1, \
                                          auth.user.id, \
                                         'Administrador')) \
                                      else \
                                          db['aplicacoes'].empresa==\
                                              auth.user.empresa,
                            value=session.aplicacao_id or 0))],
                    'mensagensPadrao', mensagensPadrao,
                    query,
                    form, fields=['id','codigoOrigemMsg','codigoTipoMsg',\
                                  'codigoRegra'],
                    noDetail=['codigoAplicacao'],
                    scroll=['5%','32%','32%','31%'],
                    search=['codigoOrigemMsg','codigoTipoMsg','codigoRegra'],
                    extra=['codigoMsgPrefixo', 'codigoMsgSufixo'],
                    optionDelete=False,
                    buttonClear=True if (auth.user) and \
                                        (auth.has_membership(1, auth.user.id, \
                                        'Administrador') or
                                         auth.has_membership(2, auth.user.id, \
                                        'Super-Usuario')) \
                                     else False,
                    buttonSubmit=True if idmensagensPadrao else False))

@auth.requires_login()
def orderby():
    listdetail.orderby('mensagensPadrao', mensagensPadrao)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('mensagensPadrao', mensagensPadrao)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('mensagensPadrao', mensagensPadrao, query=query)

@auth.requires_login()
def extra():
    MsgPrefixo = db(db[mensagensPadraoPrefixo].id==\
                    request.vars.codigoMsgPrefixo or 0).select().first()
    MsgSufixo  = db(db[mensagensPadraoSufixo].id==\
                    request.vars.codigoMsgSufixo or 0).select().first()
    entidades  = str(utl.Select(db,
                        name='entidade_id',
                        table='entidades',
                        fields=['id','nomeAmigavel'],
                        value=session.entidade_id or 1,
                        width='32%',
                        submit=False))
    ret        = ('<td align="right"><label>Preview:</label></td><td>'  + \
                      (MsgPrefixo.descricao or 'None') + '&nbsp;&nbsp;' + \
                          entidades + (MsgSufixo.descricao or 'None')   + \
                  '</td>')
    return ret

@auth.requires_login()
def report():
    id = request.args(0) or redirect(URL('index'))
    title = "Mensagens Padrao"
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
