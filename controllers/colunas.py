# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idcoluna        = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id = idaplicacao
        redirect(URL('index'))
    form = SQLFORM(colunas, idcoluna, deletable=True
            if (auth.user) and (auth.has_membership(1, auth.user.id, 'Administrador'))
            else False, hidden=dict(codigoAplicacao=idaplicacao))
    form.vars.usuarioConfirmacao = auth.user.id
    form.vars.codigoDatatype     = request.vars.codigoDatatype
    if  (auth.user) and (auth.has_membership(1, auth.user.id, 'Administrador')):
        colunas.lookups = {'usuarioConfirmacao': ['auth_user', ['first_name','last_name']]}
    else:
        colunas.lookups = {'usuarioConfirmacao': ['auth_user', ['first_name','last_name']],
                           'codigoDatatype': ['datatypes', ['descricao']]}
    form.vars.dataConfirmacao    = datetime.datetime.today()
    if  form.accepts(request.vars, session):
        db(db.checkListPrototipo.codigoAplicacao==idaplicacao).update(model = False)
        if  request.vars.has_key('delete_this_record') and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Coluna Excluida'
            redirect(URL('index'))
        else:
            if  idcoluna:
                session.flash  = 'Coluna Alterada'
                redirect(URL('index', args=(idcoluna)))
            else:
                response.flash = 'Coluna Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[colunas].codigoAplicacao<0 \
                if not idaplicacao else \
                       db[colunas].codigoAplicacao==idaplicacao
    return dict(listdetail.index(['Colunas',
                                  '<br/>Aplicacao:',
                                  str(utl.Select(db,
                                           name='aplicacao_id',
                                           table='aplicacoes',
                                           fields=['id','descricao'],
                                           filtro='' if (auth.user) and \
                                                       (auth.has_membership(1,\
                                                         auth.user.id, \
                                                         'Administrador')) \
                                                     else \
                                                         db['aplicacoes'].\
                                                         empresa==auth.user.\
                                                         empresa,
                                           value=session.aplicacao_id or 0))],
                                  'colunas', colunas,
                                  query,
                                  form, fields=['id','columnName',\
                                                'attributeName','label'],
                                  noDetail=['codigoAplicacao'],
                                  scroll=['5%','15%','40%','40%'],
                                  search=['columnName','attributeName',\
                                          'label'],
                                  optionDelete=True if (auth.user) and \
                                                       (auth.has_membership(1,\
                                                        auth.user.id, \
                                                        'Administrador') or \
                                                        auth.has_membership(2,\
                                                        auth.user.id, \
                                                        'Super-Usuario')) \
                                                    else False,
                                  buttonClear=True if (auth.user) and \
                                                      (auth.has_membership(1, \
                                                       auth.user.id, \
                                                       'Administrador') or \
                                                       auth.has_membership(2, \
                                                       auth.user.id, \
                                                       'Super-Usuario')) \
                                                   else False,
                                  buttonSubmit=True if idaplicacao else False))

@auth.requires_login()
def orderby():
    listdetail.orderby('colunas', colunas)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('colunas', colunas)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = 'codigoAplicacao==0' \
                if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                       session.aplicacao_id
    return listdetail.search('colunas', colunas, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Colunas"
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
