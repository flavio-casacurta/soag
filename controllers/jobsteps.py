# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl

@auth.requires_login()
def index():
    idjob  = session.get('idjob', 0)
    idstep = request.args(0)
    if  idstep:
        jobsteps.objeto.disabled = True
        session.idstep           = idstep
        regstep                  = db(db.jobsteps.id==idstep).select().first()
        session.step             = regstep.step
        session.sequencia        = regstep.sequencia
    else:
        jobsteps.objeto.disabled = False
        session.idstep           = 0
        session.step             = ''
        session.sequencia        = 0
    form          = SQLFORM(jobsteps, idstep, deletable=True)
    form.vars.job = request.vars.job = idjob
    if  idstep:
        regstep             = db(jobsteps.id==idstep).select().first()
        form.vars.step      = request.vars.step      = 'STEP%d' % \
                                                              regstep.sequencia
        form.vars.objeto    = request.vars.objeto    = regstep.objeto
        form.vars.idObjeto  = request.vars.idObjeto  = regstep.idObjeto
        form.vars.dsObjeto  = request.vars.dsObjeto  = regstep.dsObjeto
        form.vars.sequencia = request.vars.sequencia = regstep.sequencia
    else:
        regstep             = db(db.jobsteps.job==idjob).\
                                             select(orderby='sequencia').last()
        if  not regstep:
            form.vars.step      = request.vars.step      = 'STEP1'
            form.vars.sequencia = request.vars.sequencia = 1
        else:
            form.vars.step      = request.vars.step      = 'STEP%d' % \
                                                        (regstep.sequencia + 1)
            form.vars.sequencia = request.vars.sequencia = \
                                                        (regstep.sequencia + 1)
    if  form.accepts(request.vars, session):
        if  ('delete_this_record' in request.vars) and \
            request.vars.delete_this_record == 'on':
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
            regs = db(db.jobsteps.job==idjob).select(orderby='sequencia')
            idx  = 0
            for reg in regs:
                idx += 1
                stp  = 'STEP%d' % idx
                db(db.jobsteps.id==reg.id).update(step=stp, sequencia=idx)
            session.flash = 'STEP Excluido'
            redirect(URL('index'))
        else:
            if  idstep:
                session.flash = 'STEP Alterado'
                redirect(URL('index', args=(idstep)))
            else:
                antes_depois    = request.vars.get('antes_depois','')
                antes_depois_de = request.vars.get('antes_depois_de', \
                                                  regstep.id if regstep else 0)
                if  antes_depois == 'Depois' and \
                    antes_depois_de == str(regstep.id if regstep else 0):
                    pass
                else:
                    idstep = form.vars.id
                    if  antes_depois == 'Antes':
                        regas = db((db.jobsteps.job==idjob) &
                                   (db.jobsteps.sequencia>=
                                    int(antes_depois_de))).select(orderby='id')
                        for rega in regas:
                            if  rega.id < idstep:
                                stpreg = rega.sequencia + 1
                                step   = 'STEP%d' % stpreg
                                db(db.jobsteps.id==rega.id).\
                                            update(step=step, sequencia=stpreg)
                                if  rega.objeto == 'HPU':
                                    reghpu = db(hpus.id==rega.idObjeto).\
                                                               select().first()
                                    if  reghpu:
                                        regsysin=db(db.sysin.hpus==\
                                                rega.idObjeto).select().first()
                                        if  regsysin:
                                            db(hpus.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2  = reghpu.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(sysin.hpus==rega.idObjeto).\
                                                            update(nome2=nome2)
                                if  rega.objeto == 'Programa':
                                    regnens = db(prognens.id==rega.idObjeto).\
                                                               select().first()
                                    if  regnens:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regnens.jobPrograma)
                                        db(prognens.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2   = regnens.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(prognens3.prognens==rega.idObjeto).\
                                                            update(nome2=nome2)
                                if  rega.objeto == 'Programa (CKRS)':
                                    regckrs = db(progckrs.id==rega.idObjeto).\
                                                               select().first()
                                    if  regckrs:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regckrs.jobPrograma)
                                        db(db.progckrs.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2   = regckrs.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(progckrs3.progckrs==rega.idObjeto).\
                                                            update(nome2=nome2)
                                if  rega.objeto == 'Sort Tabela':
                                    regs1s = db(sort1s.id==rega.idObjeto).\
                                                               select().first()
                                    if  regs1s:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regs1s.jobArqName)
                                        db(db.sort1s.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                if  rega.objeto == 'Sort Arquivo':
                                    regnens = db(prognens.id==rega.idObjeto).\
                                                               select().first()
                                    if  regnens:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regnens.jobArqName)
                                        db(db.sortnens.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2   = regnens.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(prognens3.prognens==rega.idObjeto).\
                                                            update(nome2=nome2)
                        stpreg = int(antes_depois_de)
                        step   = 'STEP%s' % stpreg
                        db(db.jobsteps.id==idstep).update(step=step, \
                                                              sequencia=stpreg)
                    else:
                        regas = db((db.jobsteps.job==idjob) &
                                   (db.jobsteps.sequencia>
                                    int(antes_depois_de))).select(orderby='id')
                        for rega in regas:
                            if  rega.id < idstep:
                                stpreg = rega.sequencia + 1
                                step   = 'STEP%d' % stpreg
                                db(db.jobsteps.id==rega.id).\
                                            update(step=step, sequencia=stpreg)
                                if  rega.objeto == 'HPU':
                                    reghpu = db(hpus.id==rega.idObjeto).\
                                                               select().first()
                                    if  reghpu:
                                        regsysin=db(db.sysin.hpus==\
                                                rega.idObjeto).select().first()
                                        if  regsysin:
                                            db(hpus.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        db(db.hpus.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2  = reghpu.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(sysin.hpus==rega.idObjeto).\
                                                            update(nome2=nome2)
                                if  rega.objeto == 'Programa':
                                    regnens = db(prognens.id==rega.idObjeto).\
                                                               select().first()
                                    if  regnens:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regnens.jobPrograma)
                                        db(db.prognens.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2   = regnens.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(prognens3.prognens==rega.idObjeto).\
                                                            update(nome2=nome2)
                                if  rega.objeto == 'Programa (CKRS)':
                                    regckrs = db(progckrs.id==rega.idObjeto).\
                                                               select().first()
                                    if  regckrs:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regckrs.jobPrograma)
                                        db(db.progckrs.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2   = regckrs.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(progckrs3.progckrs==rega.idObjeto).\
                                                            update(nome2=nome2)
                                if  rega.objeto == 'Sort Tabela':
                                    regs1s = db(sort1s.id==rega.idObjeto).\
                                                               select().first()
                                    if  regs1s:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regs1s.jobArqName)
                                        db(db.sort1s.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                if  rega.objeto == 'Sort Arquivo':
                                    regnens = db(prognens.id==rega.idObjeto).\
                                                               select().first()
                                    if  regnens:
                                        db(jobsteps.id==rega.id).\
                                           update(dsObjeto=regnens.jobArqName)
                                        db(db.sortnens.id==rega.idObjeto).\
                                                           update(jobStep=step)
                                        nome2   = regnens.jobRotine + 'S' + \
                                                        '{:>02}'.format(stpreg)
                                        db(prognens3.prognens==rega.idObjeto).\
                                                            update(nome2=nome2)
                        stpreg = int(antes_depois_de) + 1
                        step   = 'STEP%d' % stpreg
                        db(db.jobsteps.id==idstep).update(step=step,
                                                              sequencia=stpreg)
                session.flash = 'STEP Incluído'
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
    if  not session.idjob:
        query = jobsteps.job==0
    else:
        query = jobsteps.job==session.idjob
    if  idstep:
        regstep = db(db.jobsteps.id==idstep).select().first()
        if  regstep.objeto == 'HPU':
            buttons = [['Editar HPU', 'hpu', '140', '350','530', '1500']]
        elif  regstep.objeto == 'Programa':
              buttons = [['Editar Programa', 'programa', '140', '350','530', \
                                                                       '1500']]
        elif  regstep.objeto == 'Programa (CKRS)':
              buttons = [['Editar CKRS', 'ckrs', '140', '350','530', '1500']]
        elif  regstep.objeto == 'Sort Tabela':
              buttons = [['Editar Sort Tabela', 'sort1s', '140', '350','530', \
                                                                       '1500']]
        else:
              buttons = [['Editar Sort Arquivo', 'sortns', '140', '350','530',\
                                                                       '1500']]
    else:
        buttons = []
    if  idstep:
        livre = ''
    else:
        livre = 'Inserir' + utl.SelectString(name='antes_depois', \
                                             options=['Antes', 'Depois'], \
                                             default='Depois') + \
                            utl.Select(db, name='antes_depois_de', \
                                           table='jobsteps', \
                                           fields=['sequencia', 'step'], \
                                           filtro=jobsteps.job==session.idjob,
                                           value=regstep.sequencia \
                                                 if regstep else 0, \
                                           submit=False)
    return dict(listdetail.index(['Steps'],
                                  'jobsteps', jobsteps,
                                  query,
                                  form, fields=['id', 'step', 'objeto', \
                                                              'dsObjeto'],
                                  scroll=['5%','31%','31%','33%'],
                                  noDetail=['job', 'sequencia', 'dsObjeto', \
                                                                'idObjeto'],
                                  search=['step', 'objeto', 'dsObjeto'],
                                  orderBy=['sequencia','ASC'],
                                  livre=livre,
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True,
                                  buttonsRefresh=buttons))

@auth.requires_login()
def orderby():
    listdetail.orderby('jobsteps', jobsteps)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('jobsteps', jobsteps)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.idjob else 'job==%d' % \
                      session.idjob
    return listdetail.search('jobsteps', jobsteps, query=query)

@auth.requires_login()
def hpu():
    idjob   = session.get('idjob',  0)
    regjob  = db(jobs.id==idjob).select().first()
    idstep  = session.get('idstep', 0)
    regstep = db(jobsteps.id==idstep).select().first()
    if  regstep:
        session.name    = regjob.name
        session.rotine  = regjob.rotine
        session.usuario = regjob.usuario
        if  regstep.idObjeto:
            redirect('../jobstephpu/index/%s' % regstep.idObjeto)
        else:
            redirect('../jobstephpu/index')

@auth.requires_login()
def programa():
    idjob   = session.get('idjob',  0)
    idstep  = session.get('idstep', 0)
    regjob  = db(jobs.id==idjob).select().first()
    regstep = db(jobsteps.id==idstep).select().first()
    if  regstep:
        session.name    = regjob.name
        session.rotine  = regjob.rotine
        session.usuario = regjob.usuario
        if  regstep.idObjeto:
            redirect('../jobstepnens/index/%s' % regstep.idObjeto)
        else:
            redirect('../jobstepnens/index')

@auth.requires_login()
def ckrs():
    idjob   = session.get('idjob',  0)
    idstep  = session.get('idstep', 0)
    regjob  = db(jobs.id==idjob).select().first()
    regstep = db(jobsteps.id==idstep).select().first()
    if  regstep:
        session.name    = regjob.name
        session.rotine  = regjob.rotine
        session.usuario = regjob.usuario
        if  regstep.idObjeto:
            redirect('../jobstepckrs/index/%s' % regstep.idObjeto)
        else:
            redirect('../jobstepckrs/index')

@auth.requires_login()
def sort1s():
    idjob   = session.get('idjob',  0)
    idstep  = session.get('idstep', 0)
    regjob  = db(jobs.id==idjob).select().first()
    regstep = db(jobsteps.id==idstep).select().first()
    if  regstep:
        session.name    = regjob.name
        session.rotine  = regjob.rotine
        session.usuario = regjob.usuario
        if  regstep.idObjeto:
            redirect('../jobstep1s/index/%s' % regstep.idObjeto)
        else:
            redirect('../jobstep1s/index')

@auth.requires_login()
def sortns():
    idjob   = session.get('idjob',  0)
    idstep  = session.get('idstep', 0)
    regjob  = db(jobs.id==idjob).select().first()
    regstep = db(jobsteps.id==idstep).select().first()
    if  regstep:
        session.name    = regjob.name
        session.rotine  = regjob.rotine
        session.usuario = regjob.usuario
        if  regstep.idObjeto:
            redirect('../jobstepns/index/%s' % regstep.idObjeto)
        else:
            redirect('../jobstepns/index')

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Steps"
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
