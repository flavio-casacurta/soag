# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idregrasColuna  = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    else:
        if  request.vars:
            if  str(request.vars.codigoColuna).strip() == '0':
                session.flash = 'Coluna deve ser preenchida'
                redirect(URL('index'))
        if  not idregrasColuna:
            if  request.vars:
                regra=db(db[regras].id==request.vars.codigoRegra).\
                            select().first()
                if  regra.argumento1:
                    if  not request.vars.argumento1:
                        session.flash = 'Argumento 1 deve ser preenchido'
                        redirect(URL('index'))
                else:
                    if  request.vars.argumento1:
                        session.flash = 'Argumento 1 nao deve ser preenchido'
                        redirect(URL('index'))
                if  regra.argumento2:
                    if  not request.vars.argumento2:
                        session.flash = 'Argumento 2 deve ser preenchido'
                        redirect(URL('index'))
                else:
                    if  request.vars.argumento2:
                        session.flash = 'Argumento 2 nao deve ser preenchido'
                        redirect(URL('index'))
        form = SQLFORM(regrasColunas, idregrasColuna, deletable=True \
                            if (auth.user) and (auth.has_membership(1, \
                                auth.user.id, 'Administrador')) \
                            else False, \
                        hidden=dict(codigoAplicacao=idaplicacao))
        form.vars.codigoRegra        = request.vars.codigoRegra
        form.vars.codigoColuna       = request.vars.codigoColuna
        form.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        if  form.accepts(request.vars, session):
            db(db.checkListPrototipo.codigoAplicacao==idaplicacao).update( model = False
                                                                         , controllers = False)
            if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
                session.flash = 'Regra Coluna Excluida'
                redirect(URL('index'))
            else:
                if  idregrasColuna:
                    session.flash  = 'Regra Coluna Alterada'
                    redirect(URL('index', args=(idregrasColuna)))
                else:
                    response.flash = 'Regra Coluna Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[regrasColunas].codigoAplicacao<0 \
                if  not idaplicacao else \
                    db[regrasColunas].codigoAplicacao==idaplicacao
    return dict(listdetail.index(['Regras Colunas',
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
                    'regrasColunas', regrasColunas,
                    query,
                    form, fields=['id','codigoColuna','codigoRegra',\
                                  'argumento1','argumento2'],
                    noDetail=['codigoAplicacao'],
                    scroll=['5%','18%','17%','30%','30%'],
                    search=['codigoColuna','codigoRegra'],
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
    listdetail.orderby('regrasColunas', regrasColunas)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('regrasColunas', regrasColunas)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = 'codigoAplicacao==0' if not session.aplicacao_id else \
            'codigoAplicacao==%d' % session.aplicacao_id
    return listdetail.search('regrasColunas', regrasColunas, query=query)

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
