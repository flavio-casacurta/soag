# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import jobs
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idcolentidade   = request.args(0)
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
        form = SQLFORM(colunasEntidades, idcolentidade, deletable=True \
                if (auth.user) and \
                   (auth.has_membership(1, auth.user.id, 'Administrador')) \
                else False,
                hidden=dict(codigoAplicacao=idaplicacao, \
                                codigoEntidade=identidade))
        form.vars.codigoColuna       = request.vars.codigoColuna
        form.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        if  form.accepts(request.vars, session):
            if  request.vars.has_key('delete_this_record') and \
                request.vars.delete_this_record == 'on':
                session.flash = 'Coluna Entidade Excluida'
                redirect(URL('index'))
            else:
                if  idcolentidade:
                    session.flash  = 'Coluna Entidade Alterada'
                    redirect(URL('index', args=(idcolentidade)))
                else:
                    response.flash = 'Coluna Entidade Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  not idaplicacao or not identidade:
        query = db[colunasEntidades].codigoAplicacao==0
    else:
        query = db[colunasEntidades].codigoAplicacao==idaplicacao
    return dict(listdetail.index(['Colunas x Entidades',
                                  '<br />Aplicacao:',
                                  str(utl.Select(db,
                                       name='aplicacao_id',
                                       table='aplicacoes',
                                       fields=['id','descricao'],
                                       filtro='' if (auth.user) and \
                                                    (auth.has_membership(1, \
                                                     auth.user.id, \
                                                    'Administrador')) \
                                                 else
                                                    db['aplicacoes'].empresa==\
                                                        auth.user.empresa,
                                       value=session.aplicacao_id)),
                                  '<br/>Entidade:',
                                  str(utl.Select(db, name='entidade_id',
                                       table='entidades',
                                       fields=['id','nomeFisico'],
                                       masks=[[],['nomeExterno','nomeFisico']],
                                       filtro=db['entidades'].codigoAplicacao\
                                                   ==idaplicacao,
                                       value=session.entidade_id)),
                                  'Tamanho: %s bytes' % str(\
                                    jobs.lrecl(db, session.entidade_id))],
                                  'colunasEntidades', colunasEntidades,
                                  query,
                                  form, fields=['id','codigoColuna'],
                                  filtros=[['codigoEntidade', identidade]],
                                  scroll=['5%','48%','47%'],
                                  noDetail=['codigoAplicacao', \
                                            'codigoEntidade'],
                                  noCheckFields=['ehNotNull'],
                                  keysCheckFields=['Inclusao','Alteracao',\
                                                   'Exclusao','Consulta',\
                                                   'Lista'],
                                  checkFields={'Inclusao':  [['Entrada', \
                                                              'inclusaoEntrada'],
                                                             ['Saida',   \
                                                              'inclusaoSaida']],
                                               'Alteracao': [['Entrada', \
                                                              'alteracaoEntrada'],
                                                             ['Saida',   \
                                                              'alteracaoSaida']],
                                               'Exclusao':  [['Entrada', \
                                                              'exclusaoEntrada'],
                                                             ['Saida',   \
                                                              'exclusaoSaida']],
                                               'Consulta':  [['Entrada', \
                                                              'consultaEntrada'],
                                                             ['Saida',   \
                                                              'consultaSaida']],
                                               'Lista':     [['Entrada', \
                                                              'listaEntrada'],
                                                             ['Saida',   \
                                                              'listaSaida']]},
                                  search=['codigoColuna'],
                                  optionDelete=True \
                                        if  (auth.user) and \
                                            (auth.has_membership(1, \
                                             auth.user.id,'Administrador') or
                                             auth.has_membership(2, \
                                             auth.user.id,'Super-Usuario')) \
                                        else False,
                                  buttonClear=True \
                                        if  (auth.user) and \
                                            (auth.has_membership(1, \
                                             auth.user.id, 'Administrador') or \
                                             auth.has_membership(2, \
                                             auth.user.id, 'Super-Usuario')) \
                                        else False,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('colunasEntidades', colunasEntidades)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('colunasEntidades', colunasEntidades)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                    session.aplicacao_id
    return listdetail.search('colunasEntidades', colunasEntidades, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Colunas Entidades"
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
