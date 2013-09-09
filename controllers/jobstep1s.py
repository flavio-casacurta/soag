# coding: utf8

from gluon.contrib.pyfpdf import FPDF

@auth.requires_login()
def index():
    idsrt = request.args(0)
    if  idsrt:
        regsort1s = db(sort1s.id==idsrt).select().first()
        session.codigoEntidade = regsort1s.codigoEntidade
        session.codigoSort1s   = idsrt
    else:
        session.codigoEntidade = 0
        session.codigoSort1s   = 0
    idaplicacao = int(session.aplicacao_id or 0)
    identidade  = int(request.vars.codigoEntidade or 0)
    form = SQLFORM(sort1s, idsrt, deletable=False)
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
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            db(db.sort3s.codigoSort1s==idsrt).delete()
            db(db.sort2s.codigoSort1s==idsrt).delete()
            session.flash = 'SORT Excluido'
            redirect(URL('index'))
        else:
            if  idsrt:
                session.flash = 'SORT Alterado'
            else:
                idstep  = session.get('idstep', 0)
                idsrt   = form.vars.id
                reg1s   = db(db.sort1s.id==idsrt).select().first()
                if  reg1s:
                    db(db.jobsteps.id==idstep).update(idObjeto=idsrt, \
                                                     dsObjeto=reg1s.jobArqName)
                else:
                    db(db.jobsteps.id==idstep).update(idObjeto=idsrt)
                session.flash = 'SORT Incluído'
            redirect(URL('index', args=(idsrt)))
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
        query = sort1s.codigoAplicacao==0
    else:
        query = sort1s.codigoAplicacao==idaplicacao
    buttons = [['Fields',   'sort2sb', '140', '350','530', '1500'],
               ['Includes', 'sort3sb', '140', '350','530', '1500']]
    fields  = db(db.sort2s.codigoSort1s==idsrt).select()
    popups  = []
    return dict(listdetail.index(['Sort Tabela'],
                    'sort1s', sort1s,
                    query, form,
                    noDetail=['codigoAplicacao','jobStep','jobName',\
                              'jobRotine','jobUser','usuarioGeracao',\
                              'dataGeracao'],
                    noList=True,
                    optionDelete=False,
                    buttonClear=False,
                    buttonSubmit=True if idaplicacao else False,
                    buttons=buttons,
                    popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('sort1s', sort1s)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('sort1s', sort1s)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('sort1s', sort1s, query=query)

@auth.requires_login()
def sort2sb():
    redirect('../jobstep2s/index')

@auth.requires_login()
def sort3sb():
    redirect('../jobstep3s/index')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "SORT Tabela"
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
