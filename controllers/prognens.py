# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import jobs
import utilities as utl

@auth.requires_login()
def index():
    idprog = request.args(0)
    if  idprog:
        regprognens            = db(prognens.id==idprog).select().first()
        session.codigoPrognens = idprog
        session.jobRotine      = regprognens.jobRotine
        session.jobPrograma    = regprognens.jobPrograma
    else:
        session.codigoPrognens = 0
        session.jobRotine      = ''
        session.jobPrograma    = ''
    form = SQLFORM(prognens, idprog, deletable=True)
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
            db(db.prognens4.prognens==idprog).delete()
            db(db.prognens3.prognens==idprog).delete()
            db(db.prognens2.prognens==idprog).delete()
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
        query = prognens.codigoAplicacao==0
    else:
        query = prognens.codigoAplicacao==idaplicacao
    buttons = [['Comentarios', 'prognens2', '250', '390','280', '600'],
               ['Entrada',     'prognens3',  '70', '390','530', '600'],
               ['Saida',       'prognens4',  '40', '390','620', '600'],
               ['Gerar JCL',   'gerarjcl']]
    popups  = []
    if  idprog and db(db.prognens.id==idprog).select()[0].dataGeracao:
        popups.append(['Download', 'prognensd'])
    return dict(listdetail.index(['Programa',
                '<br/>Aplicacoes:',
                str(utl.Select(db,
                        name='codigoAplicacao',
                        table='aplicacoes',
                        fields=['id','descricao'],
                        value=session.aplicacao_id))],
                'prognens', prognens,
                query,
                form, fields=['id', 'jobName', 'jobRotine', 'jobPrograma'],
                scroll=['5%','32%','32%','31%'],
                noDetail=['codigoAplicacao'],
                search=['jobName', 'jobRotine', 'jobPrograma'],
                optionDelete=True,
                buttonClear=True,
                buttonSubmit=True if idaplicacao else False,
                buttons=buttons,
                popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('prognens', prognens)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('prognens', prognens)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                    session.aplicacao_id
    return listdetail.search('prognens', prognens, query=query)

@auth.requires_login()
def gerarjcl():
    idprog = request.args(0) or redirect(URL('index'))
    jcl    = jobs.gerarnens(db, idprog, auth.user.id)
    session.flash       = jcl['flash']
    session.labelErrors = jcl['labelErrors']
    session.msgsErrors  = jcl['msgsErrors']
    redirect(URL('index', args=(idprog)))

@auth.requires_login()
def prognensd():
    idprog        = request.args(0) or redirect(URL('index'))
    parms         = db(db.parametros.id==1).select()[0]
    regprog       = db(db.prognens.id==idprog).select()[0]
    aplicacao     = db(db.aplicacoes.id==regprog.codigoAplicacao).\
                                         select().first()
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select().first()
    gerprog       = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'PROGNENS') + os.sep
    filesrt       = '%s.jcl' % regprog.jobName
    return listdetail.download(request, response, gerprog, filesrt)

@auth.requires_login()
def prognens2():
    idprog   = session.get('codigoPrognens', 0)
    regnens2 = db(db.prognens2.prognens==idprog).select().first()
    if  idprog:
        if  regnens2:
            redirect('../prognens2/index/%s' % regnens2.id)
        else:
            redirect('../prognens2/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def prognens3():
    redirect('../prognens3/index')

@auth.requires_login()
def prognens4():
    redirect('../prognens4/index')

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

# vim: ft=python
