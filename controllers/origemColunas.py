# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idorigemColuna  = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    else:
        form = SQLFORM(origemColunasAplicacao, idorigemColuna, deletable=True \
                if  (auth.user) and \
                    (auth.has_membership(1, auth.user.id, 'Administrador')) \
                else False,
                hidden=dict(codigoAplicacao=idaplicacao))
        if  request.vars:
            if  str(request.vars.codigoColuna).strip() == '0':
                session.flash = 'Coluna deve ser preenchida'
                redirect(URL('index'))
            form.vars.codigoRegra    = request.vars.codigoRegra
            form.vars.codigoColuna   = request.vars.codigoColuna
        form.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = request.vars.dataConfirmacao = \
                                       datetime.datetime.today()
        if  form.accepts(request.vars, session):
            db(db.checkListPrototipo.codigoAplicacao==idaplicacao).update( model = False
                                                                         , controllers = False)
            if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
                session.flash = 'Origem Coluna Excluida'
                redirect(URL('index'))
            else:
                if  idorigemColuna:
                    session.flash = 'Origem Coluna Alterada'
                    redirect(URL('index', args=(idorigemColuna)))
                else:
                    response.flash = 'Origem Coluna Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[origemColunasAplicacao].codigoAplicacao<0 \
                if not idaplicacao else \
                    db[origemColunasAplicacao].codigoAplicacao==idaplicacao
    return dict(listdetail.index(['Origem Colunas',
                '<br/>Aplicacao:',
                str(utl.Select(db,
                        name='aplicacao_id',
                        table='aplicacoes',
                        fields=['id','descricao'],
                        filtro='' if (auth.user) and \
                                     (auth.has_membership(1, auth.user.id, \
                                     'Administrador')) \
                                  else db['aplicacoes'].empresa==\
                                       auth.user.empresa,
                        value=session.aplicacao_id or 0))],
                'origemColunasAplicacao', origemColunasAplicacao,
                query,
                form, fields=['id','codigoColuna','codigoRegra','origem'],
                noDetail=['codigoAplicacao'],
                scroll=['5%','25%','20%','50%'],
                search=['codigoColuna','codigoRegra','origem'],
                optionDelete=True \
                    if (auth.user)       and \
                       (auth.has_membership(1, auth.user.id, \
                       'Administrador')  or \
                        auth.has_membership(2, auth.user.id, \
                        'Super-Usuario')) \
                    else False,
                buttonClear=True \
                    if (auth.user)      and \
                       (auth.has_membership(1, auth.user.id, \
                       'Administrador') or \
                        auth.has_membership(2, auth.user.id, \
                        'Super-Usuario')) \
                    else False,
                buttonSubmit=True if idaplicacao else False))

@auth.requires_login()
def orderby():
    listdetail.orderby('origemColunasAplicacao', origemColunasAplicacao)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('origemColunasAplicacao', origemColunasAplicacao)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = 'codigoAplicacao==0' if not session.aplicacao_id else \
                    'codigoAplicacao==%d' % session.aplicacao_id
    return listdetail.search('origemColunasAplicacao', origemColunasAplicacao, \
                    query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Origem Colunas"
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
