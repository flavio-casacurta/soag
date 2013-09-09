# coding: utf8

import utilities as utl, os

@auth.requires_login()
def index():
    if  request.vars:
        idaplicacao = int(request.vars.aplicacao_id or 0)
        identcol = request.vars.sel_ent_col
    else:
        idaplicacao = int(session.aplicacao_id or 0)
        identcol = session.identcol or 'Entidades'
    if  session.aplicacao_id <> idaplicacao:
        session.aplicacao_id  = idaplicacao
    if  session.identcol <> identcol:
        session.identcol  = identcol
    if  identcol == 'Entidades':
        sqlE = """
        SELECT aplicacoes.aplicacao
             , mensagensentcol.codigoMensagem
             , mensagenspadraoprefixo.descricao
             , entidades.nomeamigavel
             , mensagenspadraosufixo.descricao
          FROM ((((aplicacoes
                   INNER JOIN mensagensentcol
                           ON aplicacoes.id = mensagensentcol.codigoaplicacao)
                   INNER JOIN entidades
                           ON mensagensentcol.codigoentcol = entidades.id)
                   INNER JOIN mensagenspadrao
                           ON mensagensentcol.codigomsgpadrao = mensagenspadrao.id)
                   INNER JOIN mensagenspadraoprefixo
                           ON mensagenspadrao.codigomsgprefixo = mensagenspadraoprefixo.id)
                   INNER JOIN mensagenspadraosufixo
                           ON mensagenspadrao.codigomsgsufixo = mensagenspadraosufixo.id
         WHERE (((mensagensentcol.codigoaplicacao)={})
           AND  ((mensagensentcol.codigoorigemmsg)=1))
         ORDER BY mensagensentcol.codigomensagem;
         """.format(idaplicacao)
        sqls = db.executesql(sqlE)
    else:
        sqlC = """
        SELECT aplicacoes.aplicacao
             , mensagensentcol.codigoMensagem
             , mensagenspadraoprefixo.descricao
             , colunas.attributename
             , mensagenspadraosufixo.descricao
             , colunas.id
             , mensagenspadrao.codigoregra
          FROM ((((aplicacoes
                   INNER JOIN mensagensentcol
                           ON aplicacoes.id = mensagensentcol.codigoaplicacao)
                   INNER JOIN colunas
                           ON mensagensentcol.codigoentcol = colunas.id)
                   INNER JOIN mensagenspadrao
                           ON mensagensentcol.codigomsgpadrao = mensagenspadrao.id)
                   INNER JOIN mensagenspadraoprefixo
                           ON mensagenspadrao.codigomsgprefixo = mensagenspadraoprefixo.id)
                   INNER JOIN mensagenspadraosufixo
                           ON mensagenspadrao.codigomsgsufixo = mensagenspadraosufixo.id
         WHERE (((mensagensentcol.codigoaplicacao)={})
           AND  ((mensagensentcol.codigoorigemmsg)=2))
         ORDER BY mensagensentcol.codigomensagem;
         """.format(idaplicacao)
        sqls = db.executesql(sqlC)
    msgs = []
    csvs = ""
    for sql in sqls:
        sql2 = sql[2].decode('utf-8').encode('cp1252')
        sql3 = sql[3].decode('utf-8').encode('cp1252')
        sql4 = sql[4].decode('utf-8').encode('cp1252')
        if  identcol == 'Entidades':
            msgs.append('{}{:04}:{}'.format(sql[0]
                                           ,sql[1]
                                           ,((sql[2] + ' ' if sql[2].strip() else '') +
                                             (sql[3] + ' ' if sql[3].strip() else '') +
                                             (sql[4]       if sql[4].strip() else ''))))

            csvs += "{}{:04};{}\n".format(sql[0]
                                         ,sql[1]
                                         ,(sql2 + ' ' if sql2.strip() else '') +
                                          (sql3 + ' ' if sql3.strip() else '') +
                                          (sql4       if sql4.strip() else ''))
        else:
            sqlA = """
            SELECT regrascolunas.argumento1
                 , regrascolunas.argumento2
              FROM regrascolunas
             WHERE  regrascolunas.codigocoluna = {}
               AND  regrascolunas.codigoregra  = {};
            """.format(sql[5], sql[6])
            args = db.executesql(sqlA)
            if  args:
                arg0 = args[0][0].decode('utf-8').encode('cp1252')
                arg1 = args[0][1].decode('utf-8').encode('cp1252')
                msgs.append('{}{:04}:{} - {} {}'.format(sql[0]
                                               ,sql[1]
                                               ,((sql[2] + ' ' if sql[2].strip() else '') +
                                                 (sql[3] + ' ' if sql[3].strip() else '') +
                                                 (sql[4]       if sql[4].strip() else ''))
                                               ,args[0][0]
                                               ,args[0][1]))

                csvs += "{}{:04};{} - {} {}\n".format(sql[0]
                                             ,sql[1]
                                             ,(sql2 + ' ' if sql2.strip() else '') +
                                              (sql3 + ' ' if sql3.strip() else '') +
                                              (sql4       if sql4.strip() else '')
                                             ,arg0
                                             ,arg1)


            else:
                msgs.append('{}{:04}:{}'.format(sql[0]
                                               ,sql[1]
                                               ,((sql[2] + ' ' if sql[2].strip() else '') +
                                                 (sql[3] + ' ' if sql[3].strip() else '') +
                                                 (sql[4]       if sql[4].strip() else ''))))

                csvs += "{}{:04};{}\n".format(sql[0]
                                             ,sql[1]
                                             ,(sql2 + ' ' if sql2.strip() else '') +
                                              (sql3 + ' ' if sql3.strip() else '') +
                                              (sql4       if sql4.strip() else ''))

    outcsv = os.path.join( '\\\\'
                         , '127.0.0.1'
                         , 'c$'
                         , os.getenv('temp')
                         , 'csvs.csv')
    out    = open(outcsv, 'w')
    out.write(csvs)
    out.close()

    popups  = []
    if  identcol and msgs:
        popups.append(['Download Mensagens', 'downloadmsgs'])

    return dict({'title': ['Aplicacao:',
                           str(utl.Select(db,
                                  name='aplicacao_id',
                                  table='aplicacoes',
                                  fields=['id','descricao'],
                                  filtro=('' if (auth.user) and
                                               (auth.has_membership(1, auth.user.id,
                                               'Administrador'))
                                            else db['aplicacoes'].empresa==
                                                 auth.user.empresa),
                                  value=session.aplicacao_id or 0)),
                           '<br/>Mensagens referente as {} geradas pelo Sistema'.format(
                               utl.SelectString(name='sel_ent_col',
                                   options=[['Entidades','Entidades'],
                                       ['Colunas','Colunas']],
                                           default=session.get('identcol',''),
                                           submit=True)),
                                           utl.buttonsDownload(popups)],
                 'mensagens': msgs})

@auth.requires_login()
def downloadmsgs():
    germsg  = os.path.join( '\\\\'
                          , '127.0.0.1'
                          , 'c$'
                          , os.getenv('temp')) + os.sep
    filemsg = 'csvs.csv'
    return listdetail.download(request, response, germsg, filemsg)

@auth.requires_login()
def download():
    return response.download(request, db)
