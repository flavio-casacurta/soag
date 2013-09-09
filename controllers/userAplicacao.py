# coding: utf8

from   gluon.contrib.pyfpdf import FPDF
import utilities as utl

@auth.requires_login()
def index():
    iduserAplicacao = request.args(0)
    if  request.vars:
        idaplicacao = int(request.vars.codigoAplicacao or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id = idaplicacao
        redirect(URL('index'))
    form = SQLFORM(userAplicacao, iduserAplicacao, deletable=True)
    if  form.vars.codigoAplicacao is None:
        form.vars.codigoAplicacao = request.vars.codigoAplicacao = idaplicacao
    if  form.accepts(request.vars, session):
        db(db.checkListPrototipo.codigoAplicacao==idaplicacao).update(users = False)
        if  request.vars.has_key('delete_this_record') and \
            request.vars.delete_this_record == 'on':
            session.flash = 'Usuário Excluido'
            redirect(URL('index'))
        else:
            if  iduserAplicacao:
                session.flash  = 'Usuário Alterado'
                redirect(URL('index', args=(iduserAplicacao)))
            else:
                response.flash = 'Usuário Incluído'
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
        query = userAplicacao.codigoAplicacao==-1
    else:
        query = userAplicacao.codigoAplicacao==idaplicacao
    buttons = []
    popups  = []
    return dict(listdetail.index(['Usuários',
                                  '<br/>Aplicação:',
                                  str(utl.Select(db,
                                                 name='codigoAplicacao',
                                                 table='aplicacoes',
                                                 fields=['id','descricao'],
                                                 filtro='' \
                                                 if (auth.user) and \
                                                    (auth.has_membership(1, \
                                                     auth.user.id, 'Administrador')) \
                                                 else aplicacoes.empresa==\
                                                      auth.user.empresa,
                                                 value=session.aplicacao_id or 0))],
                                  'userAplicacao', userAplicacao,
                                  query,
                                  form, fields=['id','username','first_name','last_name','email'],
                                  scroll=['5%','23%','23%','23%','26%'],
                                  noDetail=['codigoAplicacao'],
                                  search=['username','first_name','last_name'],
                                  optionDelete=True,
                                  buttonClear=True,
                                  buttonSubmit=True if idaplicacao else False,
                                  buttons=buttons,
                                  popups=popups))

@auth.requires_login()
def orderby():
    listdetail.orderby('userAplicacao', userAplicacao)
    redirect(URL('index'))

@auth.requires_login()
def paginacao():
    listdetail.paginacao('userAplicacao', userAplicacao)
    redirect(URL('index'))

@auth.requires_login()
def search():
    query = '' if not session.aplicacao_id else 'codigoAplicacao==%d' % \
                      session.aplicacao_id
    return listdetail.search('userAplicacao', userAplicacao, query=query)

@auth.requires_login()
def report():
    id = request.args(0) or 0
    if not id: redirect(URL('index'))
    title = "Usuarios"
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
