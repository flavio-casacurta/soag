# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idprimaryKey    = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
        identidade  = int(request.vars.entidade_id  or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
        identidade  = int(session.entidade_id  or 0)
    if  session.aplicacao_id <> idaplicacao or \
        session.entidade_id  <> identidade:
        session.aplicacao_id = idaplicacao
        session.entidade_id  = identidade
        redirect(URL('index'))
    else:
        pk = db(db[primaryKeys].id==idprimaryKey).select()
        if  pk:
            primaryKeys.codigoInsercao.writable = False \
                if pk[0].codigoInsercao == 1 else True
        else:
            primaryKeys.codigoInsercao.writable = True
        form = SQLFORM(primaryKeys, idprimaryKey, deletable=True \
                    if (auth.user) and (auth.has_membership(1, auth.user.id, \
                        'Administrador')) \
                    else False, \
                    hidden=dict(codigoAplicacao=idaplicacao, \
                                codigoEntidade=identidade))
        form.vars.codigoInsercao     = request.vars.codigoInsercao or 0
        form.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        if  form.accepts(request.vars, session):
            if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
                session.flash = 'Primary Key Excluida'
                redirect(URL('index'))
            else:
                if idprimaryKey:
                   session.flash  = 'Primary Key Alterada'
                   redirect(URL('index', args=(idprimaryKey)))
                else:
                   response.flash = 'Primary Key Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[primaryKeys].codigoAplicacao==0 \
                if not idaplicacao else db[primaryKeys].codigoEntidade==0 \
                if not identidade  else db[primaryKeys].codigoAplicacao==\
                       idaplicacao
    return dict(listdetail.index(['Primary Keys',
                '<br />Aplicacao:',
                str(utl.Select(db,
                        name='aplicacao_id',
                        table='aplicacoes',
                        fields=['id','descricao'],
                        filtro='' if (auth.user) and (auth.has_membership(1, \
                                      auth.user.id, 'Administrador')) else
                                      db['aplicacoes'].empresa==\
                                      auth.user.empresa,
                        value=session.aplicacao_id or 0)),
                '<br />Entidade:',
                str(utl.Select(db,
                        name='entidade_id',
                        table='entidades',
                        fields=['id','nomeFisico'],
                        masks=[[],['nomeExterno','nomeFisico']],
                        value=session.entidade_id or 0))],
                'primaryKeys', primaryKeys,
                query,
                form, fields=['id','codigoColuna','codigoInsercao'],
                noDetail=['codigoAplicacao', 'codigoEntidade'],
                filtros=[['codigoEntidade', identidade]],
                scroll=['5%','48%','47%'],
                search=['codigoColuna','codigoInsercao'],
                optionDelete=True \
                    if (auth.user) and \
                       (auth.has_membership(1, auth.user.id, \
                        'Administrador') or \
                        auth.has_membership(2, auth.user.id, \
                        'Super-Usuario')) \
                    else False,
                buttonClear=True \
                    if (auth.user) and \
                       (auth.has_membership(1, auth.user.id, \
                       'Administrador') or \
                        auth.has_membership(2, auth.user.id, \
                        'Super-Usuario')) \
                    else False,
                buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('primaryKeys', primaryKeys)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('primaryKeys', primaryKeys)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else ['codigoAplicacao==%d' % \
                                                        session.aplicacao_id,
                                                 'and',
                                                 'codigoEntidade==%d' % \
                                                        session.entidade_id]
    return listdetail.search('primaryKeys', primaryKeys, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Primary Keys"
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
