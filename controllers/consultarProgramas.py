# coding: utf8

import utilities as utl

@auth.requires_login()
def index():
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
        identidade  = int(request.vars.sel_entidade or 0)
    else:
        idaplicacao = int(session.aplicacao_id or 0)
        identidade  = int(session.identidade   or 0)
    if  session.identidade <> identidade:
        session.identidade  = identidade
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
        redirect(URL('index'))
    if  identidade == 999999:
        sqls = db.executesql('SELECT aplicacoes.aplicacao ' + \
                 '     , aplicacoes.soag ' + \
                 '     , 1 AS Expr1 ' + \
                 '     , programas.nomeprograma ' + \
                 '     , regras.regra ' + \
                 '     , regras.descricao ' + \
                 '     , entidades.nomeexterno ' + \
                 '     , entidades.nomeamigavel ' + \
                 'FROM ((aplicacoes ' + \
                 'INNER JOIN programas ON aplicacoes.id            = ' + \
                 'programas.codigoaplicacao) ' + \
                 'INNER JOIN entidades ON programas.codigoentidade = ' + \
                 'entidades.id) ' + \
                 'INNER JOIN regras    ON programas.codigoregra    = ' + \
                 'regras.id' + \
                 '      WHERE aplicacoes.id=%s;' % idaplicacao)
    else:
        sqls = db.executesql('SELECT aplicacoes.aplicacao ' + \
                 '     , aplicacoes.soag ' + \
                 '     , 1 AS Expr1 ' + \
                 '     , programas.nomeprograma ' + \
                 '     , regras.regra ' + \
                 '     , regras.descricao ' + \
                 '     , entidades.nomeexterno ' + \
                 '     , entidades.nomeamigavel ' + \
                 'FROM ((aplicacoes ' + \
                 'INNER JOIN programas ON aplicacoes.id            = ' + \
                 'programas.codigoaplicacao) ' + \
                 'INNER JOIN entidades ON programas.codigoentidade = ' + \
                 'entidades.id) ' + \
                 'INNER JOIN regras    ON programas.codigoregra    = ' + \
                 'regras.id ' + \
                 '      WHERE aplicacoes.id=%s' % idaplicacao + \
                 '        AND entidades.id=%s;' % identidade)

    pgms = []
    csvs = "Programa;Funcao;Entidade;Descricao\n"

    for sql in sqls:
        if  sql[1] == 'T':
            pgms.append('{}{}{}{} - {} - {} - {}'.format(sql[0], sql[2], sql[3],
                        sql[4], sql[5], sql[6], sql[7]))

            csvs += "{}{}{}{};{};{};{}\n".format(sql[0], sql[2], sql[3],
                        sql[4], sql[5], sql[6], sql[7])
        else:
            pgms.append('{} - {} - {} - {}'.format(sql[3], sql[5], sql[6], sql[7]))
            csvs += "{};{};{};{}\n".format(sql[3], sql[5], sql[6], sql[7])

    outcsv = os.path.join( '\\\\'
                         , '127.0.0.1'
                         , 'c$'
                         , os.getenv('temp')
                         , 'csvs.csv')
    out    = open(outcsv, 'w')
    out.write(csvs)
    out.close()

    popups  = []
    if  (idaplicacao or identidade) and pgms:
        popups.append(['Download Lista de Programas', 'downloadpgms'])

    return dict({'title': ['Consulta Programas<br/>Aplicacao:%s<br/>Entidade:%s' \
                     % (utl.Select(db, name='aplicacao_id',
                                       table='aplicacoes',
                                       fields=['id','descricao'],
                                       filtro='' if (auth.user) and \
                                                  (auth.has_membership(1, \
                                                auth.user.id, \
                                               'Administrador')) \
                                            else db['aplicacoes'].\
                                                empresa==auth.user.empresa,
                                       value=session.aplicacao_id or 0),
                        utl.Select(db, name='sel_entidade',
                                       table='entidades',
                                       fields=['id','nomeFisico'],
                                       masks=[[],['nomeExterno','nomeFisico']],
                                       filtro=db['entidades'].\
                                                 codigoAplicacao==idaplicacao,
                                       orderby='nomeExterno',
                                       todos='Todas Entidades',
                                       value=session.identidade)),
                                       utl.buttonsDownload(popups)],
                        'mensagens': pgms})

@auth.requires_login()
def downloadpgms():
    germsg  = os.path.join( '\\\\'
                          , '127.0.0.1'
                          , 'c$'
                          , os.getenv('temp')) + os.sep
    filemsg = 'csvs.csv'
    return listdetail.download(request, response, germsg, filemsg)

@auth.requires_login()
def download():
    return response.download(request, db)
