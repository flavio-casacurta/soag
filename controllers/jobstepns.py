# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idjob  = session.get('idjob', 0)
    idprog = request.args(0)
    if  idprog:
        regsortnens            = db(sortnens.id==idprog).select()[0]
        session.codigoSortnens = idprog
        session.codigoBook     = regsortnens.book
    else:
        session.codigoSortnens = 0
        session.codigoBook     = 0
    idaplicacao = int(session.aplicacao_id or 0)
    idbook      = int(request.vars.book or 0)
    form = SQLFORM(sortnens, idprog, deletable=False)
    form.vars.codigoAplicacao = request.vars.codigoAplicacao = idaplicacao
    form.vars.jobStep         = request.vars.jobStep         = \
                                                 session.get('step',   'STEP1')
    form.vars.jobName         = request.vars.jobName         = \
                                              session.get('name',   'JOB00001')
    form.vars.jobRotine       = request.vars.jobRotine       = \
                                              session.get('rotine', 'ROT01')
    form.vars.jobUser         = request.vars.jobUser         = \
                                              session.get('usuario','USR00001')
    if  form.accepts(request.vars, session):
        if  idprog:
            session.flash = 'SORT Alterado'
        else:
            idstep = session.get('idstep', 0)
            idprog = form.vars.id
            regns  = db(db.sortnens.id==idprog).select().first()
            if  regns:
                db(db.jobsteps.id==idstep).update(idObjeto=idprog, \
                                                 dsObjeto=regns.jobArqName)
            else:
                db(db.jobsteps.id==idstep).update(idObjeto=idprog)
            session.flash = 'SORT Incluído'
        redirect(URL('index', args=(idprog)))
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
        query = sortnens.codigoAplicacao==0
    else:
        query = sortnens.codigoAplicacao==idaplicacao
    buttons = [['Fields',  'sortnens2', '140', '350','530', '1500'],
               ['Sortin',  'sortnens3', '140', '350','530', '1500'],
               ['Sortout', 'sortnens4', '140', '350','530', '1500']]
    popups  = []
    return dict(listdetail.index(['Sort Arquivo'],
                    'sortnens', sortnens,
                    query, form,
                    noDetail=['codigoAplicacao','jobStep','jobName',\
                              'jobRotine','jobUser','usuarioGeracao',\
                              'dataGeracao'],
                    noList=True,
                    optionDelete=False,
                    buttonClear=False,
                    buttonSubmit=True,
                    buttons=buttons,
                    popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('sortnens', sortnens)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sortnens', sortnens)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('sortnens', sortnens, query=query)

@auth.requires_login()
def sortnens2():
    redirect('../jobstepns2/index')

@auth.requires_login()
def sortnens3():
    redirect('../jobstepns3/index')

@auth.requires_login()
def sortnens4():
    redirect('../jobstepns4/index')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "SORT Arquivo"
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
