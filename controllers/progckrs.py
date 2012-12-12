# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import jobs
import utilities as utl

@auth.requires_login()
def index():
    idprog = request.args(0)
    if  idprog:
        regprogckrs            = db(progckrs.id==idprog).select()[0]
        session.codigoProgckrs = idprog
        session.jobRotine      = regprogckrs.jobRotine
        session.jobPrograma    = regprogckrs.jobPrograma
    else:
        session.codigoProgckrs = 0
        session.jobRotine      = ''
        session.jobPrograma    = ''
    form = SQLFORM(progckrs, idprog, deletable=True)
    if  request.vars:
        idaplicacao            = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao            = int(session.aplicacao_id         or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    if  not idprog and not request.vars.get('jobStep', ''):
        form.vars.jobStep      = request.vars.jobStep = 'STEP1'
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            db(db.progckrs4.progckrs==idprog).delete()
            db(db.progckrs3.progckrs==idprog).delete()
            db(db.progckrs2.progckrs==idprog).delete()
            session.flash = 'Programa Excluido'
            redirect(URL('index'))
        else:
            if  idprog:
                session.flash = 'Programa Alterado'
                redirect(URL('index', args=(idprog)))
            else:
                session.flash = 'Programa Incluído'
                redirect(URL('index'))
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    if  not idaplicacao:
        query = progckrs.codigoAplicacao==0
    else:
        query = progckrs.codigoAplicacao==idaplicacao
    buttons = [['Comentarios', 'progckrs2', '250', '390','280', '600'],
               ['Entrada',     'progckrs3',  '70', '390','530', '600'],
               ['Saida',       'progckrs4',  '40', '390','590', '600'],
               ['Gerar JCL',   'gerarjcl']]
    popups  = []
    if  idprog and db(db.progckrs.id==idprog).select()[0].dataGeracao:
        popups.append(['Download', 'progckrsd'])
    return dict(listdetail.index(['Programa (CKRS)',
                '<br/>Aplicacoes:',
                str(utl.Select(db,
                        name='codigoAplicacao',
                        table='aplicacoes',
                        fields=['id','descricao'],
                        value=session.aplicacao_id))],
                'progckrs', progckrs,
                query,
                form, fields=['id', 'jobName', 'jobRotine', 'jobPrograma'],
                scroll=['5%','32%','32%','31%'],
                noDetail=['codigoAplicacao'],
                search=['jobName', 'jobRotine', 'jobPrograma'],
                optionDelete=True,
                buttonClear=True,
                buttonSubmit=True,
                buttons=buttons,
                popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('progckrs', progckrs)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('progckrs', progckrs)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                    session.aplicacao_id
    return listdetail.search('progckrs', progckrs, query=query)

@auth.requires_login()
def gerarjcl():
    idprog = request.args(0) or redirect(URL('index'))
    jcl    = jobs.gerarckrs(db, idprog, auth.user.id)
    session.flash       = jcl['flash']
    session.labelErrors = jcl['labelErrors']
    session.msgsErrors  = jcl['msgsErrors']
    redirect(URL('index', args=(idprog)))

@auth.requires_login()
def progckrsd():
    idprog        = request.args(0) or redirect(URL('index'))
    parms         = db(db.parametros.id==1).select()[0]
    regprog       = db(db.progckrs.id==idprog).select()[0]
    aplicacao     = db(db.aplicacoes.id==reghpu.codigoAplicacao).select().\
                                                                        first()
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select().first()
    gerprog       = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'PROGCKRS') + os.sep
    filesrt       = '%s.jcl' % regprog.jobName
    return listdetail.download(request, response, gerprog, filesrt)

@auth.requires_login()
def progckrs2():
    idprog   = session.get('codigoProgckrs', 0)
    regckrs2 = db(db.progckrs2.progckrs==idprog).select().first()
    if  idprog:
        if  regckrs2:
            redirect('../progckrs2/index/%s' % regckrs2.id)
        else:
            redirect('../progckrs2/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def progckrs3():
    redirect('../progckrs3/index')

@auth.requires_login()
def progckrs4():
    redirect('../progckrs4/index')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "SORT com varias entradas e varias saidas"
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
