# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime

@auth.requires_login()
def index():
    idcolentidade = request.args(0)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao      or 0)
        identidade             = int(request.vars.codigoEntidade       or 0)
        idcoluna               = int(request.vars.codigoColuna         or 0)
        identidadeReferenciada = int(request.vars.entidadeReferenciada or 0)
    else:
        idaplicacao            = int(session.aplicacao_id              or 0)
        identidade             = int(session.entidade_id               or 0)
        idcoluna               = int(session.codigoColuna              or 0)
        identidadeReferenciada = int(session.entidadeReferenciada_id   or 0)
    if  session.aplicacao_id            <> idaplicacao            or \
        session.entidade_id             <> identidade             or \
        session.entidadeReferenciada_id <> identidadeReferenciada:
        session.aplicacao_id            = idaplicacao
        session.entidade_id             = identidade
        session.entidadeReferenciada_id = identidadeReferenciada
        redirect(URL('index'))
    form = SQLFORM(colunasEntidadesReferenciadas, idcolentidade, deletable=True)
    form.vars.entidadeReferenciada = identidadeReferenciada
    form.vars.codigoColuna         = idcoluna
    form.vars.usuarioConfirmacao   = auth.user.id
    form.vars.dataConfirmacao      = datetime.datetime.today()
    if  form.accepts(request.vars, session):
        if  request.vars.has_key('delete_this_record') and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Coluna Entidade Referenciada Excluida'
            redirect(URL('index'))
        else:
            if  idcolentidade:
                session.flash = 'Coluna Entidade Referenciada Alterada'
                redirect(URL('index', args=(idcolentidade)))
            else:
                response.flash = 'Coluna Entidade Referenciada Incluída'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    query = db[colunasEntidadesReferenciadas].codigoAplicacao==0 \
                if not idaplicacao else \
                        db[colunasEntidadesReferenciadas].codigoEntidade==0 \
                if not identidade  else \
                        db[colunasEntidadesReferenciadas].codigoAplicacao==\
                            idaplicacao and \
            db[colunasEntidadesReferenciadas].entidadeReferenciada==\
                        identidadeReferenciada
    return dict(listdetail.index(['Colunas x Entidades Referenciadas',
                                  '<br/>Aplicacao:',
                                  str(utl.Select(db,
                                        name='codigoAplicacao',
                                        table='aplicacoes',
                                        fields=['id','descricao'],
                                        filtro='' if (auth.user) and \
                                                     (auth.has_membership(1, \
                                                      auth.user.id, \
                                                     'Administrador')) \
                                                  else
                                                     db['aplicacoes'].empresa\
                                                         ==auth.user.empresa,
                                        value=session.aplicacao_id or 0)),
                                  '<br/>Entidade:',
                                  str(utl.Select(db,
                                        name='codigoEntidade',
                                        table='entidades',
                                        fields=['id','nomeFisico'],
                                        masks=[[],\
                                        ['nomeExterno','nomeFisico']],
                                        value=session.entidade_id or 0)),
                                  '<br/>Entidade Referenciada:',
                                  str(utl.Select(db,
                                        name='entidadeReferenciada',
                                        table='foreignKeys',
                                        fields=['codigoEntidadeReferenciada', \
                                                'codigoEntidadeReferenciada'],
                                        lookups={'codigoEntidadeReferenciada':\
                                                 ['entidades','nomeFisico']},
                                        filtro=db['foreignKeys'].\
                                                  codigoEntidade==session.\
                                                  entidade_id,
                                        distinct=True,
                                        value=session.entidadeReferenciada_id \
                                                or 0))],
                                  'colunasEntidadesReferenciadas', \
                                   colunasEntidadesReferenciadas,
                                  query,
                                  form, fields=['id','codigoColuna'],
                                  scroll=['5%','95%'],
                                  noDetail=['codigoAplicacao', \
                                            'codigoEntidade', \
                                            'entidadeReferenciada'],
                                  noLookups=['codigoColuna'],
                                  noCheckFields=['confirmado'],
                                  keysCheckFields=['Consulta','Lista'],
                                  checkFields={'Consulta': [['Saida', 
                                                             'consultaSaida']],
                                               'Lista':    [['Saida', 
                                                             'listaSaida']]},
                                  search=['codigoColuna'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('colunasEntidadesReferenciadas', \
                        colunasEntidadesReferenciadas)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('colunasEntidadesReferenciadas', \
                          colunasEntidadesReferenciadas)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('colunasEntidadesReferenciadas', \
                              colunasEntidadesReferenciadas, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Colunas Entidades Referenciadas"
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
