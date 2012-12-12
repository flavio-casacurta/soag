# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl
import datetime
import Entidades

@auth.requires_login()
def index():
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id = idaplicacao
        redirect(URL('index'))
    else:
        cl = db(db[checkList].codigoAplicacao==idaplicacao).select()
        if  cl:
            idcheckList = cl[0].id
        else:
            idcheckList = 0
        form = SQLFORM(checkList, idcheckList, hidden=dict(codigoAplicacao=\
                    idaplicacao))
        form.vars.usuarioConfirmacao = auth.user.id
        form.vars.dataConfirmacao    = datetime.datetime.today()
        if  form.accepts(request.vars, session):
            if  request.vars.has_key('delete_this_record') and \
                    request.vars.delete_this_record == 'on':
                session.flash = 'CheckList Excluido'
                redirect(URL('index'))
            else:
                if  idcheckList:
                    if  request.vars.aplicacao     and not \
                        request.vars.entidades     and not \
                        request.vars.colunas       and not \
                        request.vars.regrasColunas and not \
                        request.vars.origemColunas:
                        ents = Entidades.Entidades(db, cAppl=idaplicacao)
                        rets = ents.updateEntidadesXprogramas()
                        msgerrors = {}
                        idx       = 0
                        for line in rets[1].split('\n'):
                            if  line:
                                idx += 1
                                msgerrors[idx] = line
                        session.labelErrors = \
                                      'Atualização dos:'
                        session.msgsErrors  = msgerrors
                    session.flash  = 'CheckList Alterado'
                    redirect(URL('index', args=(idcheckList)))
                else:
                    response.flash = 'CheckList Incluído'
    if  session.flash:
        response.flash = session.flash
        session.flash  = None
    if  session.labelErrors:
        form.labelErrors    = session.labelErrors
        session.labelErrors = None
    if  session.msgsErrors:
        form.errors        = session.msgsErrors
        session.msgsErrors = None
    query = db[checkList].codigoAplicacao<0 if not idcheckList else \
                db[checkList].codigoAplicacao==idaplicacao
    return dict(listdetail.index(['CheckList',
                                  '<br/>Aplicacao:',
                                  str(utl.Select(db,
                                           name='aplicacao_id',
                                           table='aplicacoes',
                                           fields=['id','descricao'],
                                           filtro='' if (auth.user) and \
                                                        (auth.has_membership(1,\
                                                         auth.user.id, \
                                                        'Administrador')) \
                                                     else db['aplicacoes'].\
                                                         empresa==auth.user.\
                                                                     empresa, \
                                           value=session.aplicacao_id or 0))],
                                 'checkList', checkList,
                                 query,
                                 form, fields=[],
                                 noDetail=['codigoAplicacao'],
                                 scroll=[],
                                 width_label='45%',
                                 width_field='55%',
                                 optionDelete=False,
                                 buttonClear=False,
                                 buttonSubmit=True))

@auth.requires_login()
def orderby():
    listdetail.orderby('checkList', checkList)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('checkList', checkList)
    redirect(URL('index'))

@auth.requires_login()
def search():
    return listdetail.search('checkList', checkList)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Check List"
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
