# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import jobs      as jbs
import utilities as utl

@auth.requires_login()
def index():
    idjob = request.args(0)
    if  idjob:
        regjob = db(db.jobs.id==idjob).select()[0]
        session.idjob = idjob
    else:
        session.idob  = 0
    if  request.vars:
        idaplicacao   = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao   = int(session.aplicacao_id or 0)
    if  session.aplicacao_id  <> idaplicacao:
        session.aplicacao_id   = idaplicacao
        redirect(URL('index'))
    form = SQLFORM(db.jobs, idjob, deletable=True)
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
            regstep = db(db.jobsteps.job==idjob).select().first()
            if regstep:
                if  regstep.objeto == 'HPU':
                    db(db.sysin.hpus==regstep.idObjeto).delete()
                    db(db.hpus.id==regstep.idObjeto).delete()
                if  regstep.objeto == 'Programa':
                    db(db.prognens4.prognens==regstep.idObjeto).delete()
                    db(db.prognens3.prognens==regstep.idObjeto).delete()
                    db(db.prognens2.prognens==regstep.idObjeto).delete()
                    db(db.prognens.id==regstep.idObjeto).delete()
                if  regstep.objeto == 'Programa (CKRS)':
                    db(db.progckrs4.progckrs==regstep.idObjeto).delete()
                    db(db.progckrs3.progckrs==regstep.idObjeto).delete()
                    db(db.progckrs2.progckrs==regstep.idObjeto).delete()
                    db(db.progckrs.id==regstep.idObjeto).delete()
                if  regstep.objeto == 'Sort Tabela':
                    db(db.sort3s.codigoSort1s==regstep.idObjeto).delete()
                    db(db.sort2s.codigoSort1s==regstep.idObjeto).delete()
                    db(db.sort1s.id==regstep.idObjeto).delete()
                if  regstep.objeto == 'Sort Arquivo':
                    db(db.sortnens5.sortnens4==regstep.idObjeto).delete()
                    db(db.sortnens4.sortnens==regstep.idObjeto).delete()
                    db(db.sortnens3.sortnens==regstep.idObjeto).delete()
                    db(db.sortnens2.sortnens==regstep.idObjeto).delete()
                    db(db.sortnens.id==regstep.idObjeto).delete()
                db(db.jobsteps.job==idjob).delete()
            session.flash = 'Job Excluido'
            redirect(URL('index'))
        else:
            if  idjob:
                regjob   = db(jobs.id==idjob).select().first()
                regsteps = db(jobsteps.job==idjob).select()
                for regstep in regsteps:
                    db(hpus.id==regstep.idObjeto).\
                                                update(jobRotine=regjob.rotine)
                    db(prognens.id==regstep.idObjeto).\
                                                update(jobRotine=regjob.rotine)
                    db(prognens3.prognens==regstep.idObjeto).\
                                                    update(nome1=regjob.rotine)
                    db(progckrs.id==regstep.idObjeto).\
                                                update(jobRotine=regjob.rotine)
                    db(sort1s.id==regstep.idObjeto).\
                                                update(jobRotine=regjob.rotine)
                    db(sortnens.id==regstep.idObjeto).\
                                                update(jobRotine=regjob.rotine)
                session.flash = 'Job Alterado'
                redirect(URL('index', args=(idjob)))
            else:
                session.flash = 'Job Incluído'
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
        query = db.jobs.codigoAplicacao==0
    else:
        query = db.jobs.codigoAplicacao==idaplicacao
    buttons = [['Steps', 'steps', '140', '350','530', '1500'],
               ['Gerar job',  'gerarjob']]
    popups  = []
    if  idjob and db(db.jobs.id==idjob).select()[0].dataGeracao:
        popups.append(['Download', 'jobsd'])
    return dict(listdetail.index(['Jobs',
                                  '<br/>Aplicacao:',
                                  str(utl.Select(db,
                                                 name='codigoAplicacao',
                                                 table='aplicacoes',
                                                 fields=['id','descricao'],
                                                 value=session.aplicacao_id))],
                                  'jobs', jobs,
                                  query,
                                  form, fields=['id', 'name', 'rotine', \
                                                'usuario'],
                                  scroll=['5%','33%','21%','21%','20%'],
                                  noDetail=['codigoAplicacao'],
                                  search=['name', 'rotine', 'usuario'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True if idaplicacao else False,
                                  buttons=buttons,
                                  popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('jobs', jobs)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('jobs', jobs)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('jobs', jobs, query=query)

@auth.requires_login()
def steps():
    redirect('../jobsteps/index')

@auth.requires_login()
def gerarjob():
    idjob               = request.args(0) or redirect(URL('index'))
    jcl                 = jbs.gerarJob(db, idjob, auth.user.id)
    session.flash       = jcl['flash']
    session.labelErrors = jcl['labelErrors']
    session.msgsErrors  = jcl['msgsErrors']
    redirect(URL('index', args=(idjob)))

@auth.requires_login()
def jobsd():
    idjob         = request.args(0)
    parms         = db(db.parametros.id==1).select().first()
    regjob        = db(db.jobs.id==idjob).select().first()
    aplicacao     = db(db.aplicacoes.id==regjob.codigoAplicacao).\
                                                               select().first()
    nomeaplicacao = aplicacao.aplicacao
    regempresa    = db(db.empresa.id==aplicacao.empresa).select().first()
    gerjob        = os.path.join( '\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.raiz
                                , regempresa.nome
                                , nomeaplicacao
                                , 'GERADOS'
                                , 'JOBS') + os.sep
    filejob       = '%s.jcl' % regjob.name
    return listdetail.download(request, response, gerjob, filejob)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Job"
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
