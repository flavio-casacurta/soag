# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idjob  = session.get('idjob', 0)
    idprog = request.args(0)
    form   = SQLFORM(prognens, idprog, deletable=False)
    idaplicacao = int(session.aplicacao_id or 0)
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
            session.flash = 'Programa Alterado'
        else:
            idstep  = session.get('idstep', 0)
            idprog  = form.vars.id
            regnens = db(db.prognens.id==idprog).select().first()
            if  regnens:
                db(db.jobsteps.id==idstep).update(idObjeto=idprog, \
                                                  dsObjeto=regnens.jobPrograma)
            else:
                db(db.jobsteps.id==idstep).update(idObjeto=idprog)
            session.flash = 'Programa Incluído'
        redirect(URL('index', args=(idprog)))
    if  idprog:
        regprognens            = db(prognens.id==idprog).select().first()
        session.codigoPrognens = idprog
        session.jobRotine      = regprognens.jobRotine
        session.jobPrograma    = regprognens.jobPrograma
        form.vars.jobPrograma  = request.vars.jobPrograma = \
                                                        regprognens.jobPrograma
    else:
        session.codigoPrognens = 0
        session.jobRotine      = ''
        session.jobPrograma    = ''
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
    buttons = [['Comentarios', 'prognens2', '140', '350','530', '1500'],
               ['Entrada',     'prognens3', '140', '350','530', '1500'],
               ['Saida',       'prognens4', '140', '350','530', '1500']]
    popups  = []
    return dict(listdetail.index(['Programa'],
                'prognens', prognens, query, form,
                noDetail=['codigoAplicacao','jobStep','jobName',\
                          'jobRotine','jobUser','usuarioGeracao',\
                          'dataGeracao'],
                optionDelete=False,
                buttonClear=False,
                buttonSubmit=True,
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
def prognens2():
    idprog   = session.get('codigoPrognens', 0)
    regnens2 = db(db.prognens2.prognens==idprog).select().first()
    if  idprog:
        if  regnens2:
            redirect('../jobstepnens2/index/%s' % regnens2.id)
        else:
            redirect('../jobstepnens2/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def prognens3():
    idprog = session.get('codigoPrognens', 0)
    if  idprog:
        redirect('../jobstepnens3/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def prognens4():
    idprog = session.get('codigoPrognens', 0)
    if  idprog:
        redirect('../jobstepnens4/index')
    else:
        redirect(URL('index'))

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Programa"
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
