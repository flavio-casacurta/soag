# coding: utf8

@auth.requires_login()
def index():
   sqls = db.executesql('SELECT aplicacoes.aplicacao, mensagensentcol.id, ' + \
                        'mensagenspadraoprefixo.descricao, entidades.nomeamigavel, ' + \
                        'mensagenspadraosufixo.descricao ' + \
                        'FROM ((((aplicacoes INNER JOIN mensagensentcol ' + \
                        'ON aplicacoes.id = mensagensentcol.codigoaplicacao) ' + \
                        'INNER JOIN entidades ' + \
                        'ON mensagensentcol.codigoentcol = entidades.id) ' + \
                        'INNER JOIN mensagenspadrao ' + \
                        'ON mensagensentcol.codigomsgpadrao = mensagenspadrao.id) ' + \
                        'LEFT JOIN mensagenspadraoprefixo ' + \
                        'ON mensagenspadrao.codigomsgprefixo = mensagenspadraoprefixo.id) ' + \
                        'INNER JOIN mensagenspadraosufixo ' + \
                        'ON mensagenspadrao.codigomsgsufixo = mensagenspadraosufixo.id ' + \
                        'WHERE (((mensagensentcol.codigoorigemmsg)=1));')
   msgs = []
   for sql in sqls:
       msgs.append('%s%s: %s %s %s' % (sql[0], ('0' * ((4 - len(str(sql[1])))) + str(sql[1]))  \
                   , sql[2] or '', sql[3] or '', sql[4] or ''))
   return dict({'mensagens': msgs})

   imag0001
