# coding: utf8

@auth.requires_login()
def index():
   return dict({'mensagens': session.msgtbasicas or []})

@auth.requires_login()
def clear():
   session.msgtbasicas = []
   redirect(URL('index'))

@auth.requires_login()
def aplicar():
   parms = db(db[parametros]).select()[0]
   fn    = "%sapplications/%s/modules/InsertTabelasBasicasSOAG.sql" % \
                   (parms.web2py, parms.soag)
   try:
       arqs  = file(fn)
       sql   = ''
       for arq in arqs:
           sql += arq
       db.executesql(sql)
       session.msgtbasicas = ['Carga das Tabelas Basicas efetuada com sucesso.']
   except:
       session.msgtbasicas = \
                        ['Script InsertTabelasBasicasSOAG.sql nao encontrado.']
   redirect(URL('index'))
