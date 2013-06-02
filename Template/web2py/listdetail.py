# coding: utf8

from gluon import streamer, contenttype as c

class listdetail():

    def tabela(self, name, tabela):
        orderdirection = dict()
        for field in tabela.fields:
            orderdirection[field] = 'desc'
        session[name] = dict(listdetail = dict(page=0,
                                               orderfield='id',
                                               orderdirection=\
                                                   orderdirection,
                                               orderby=name + '.id asc'))
        return session[name]['listdetail']

    def index(self, titulos, name, tabela, query, form, noList=False, \
              detail=[], noDetail=[], noLookups=[], abas=dict(), fields=[], \
              scroll=[], noCheckFields=[], keysCheckFields=[], livre='', \
              checkFields={}, custom='', right='', labelId='', search=[], \
              buttons=[], buttonsRefresh=[], popups=[], executes=[], \
              optionDelete=True, reference={}, extra=[], buttonClear=True, \
              buttonProcess=False, buttonProcessLabel='Processar', \
              buttonSelect=False, buttonPopup=False, \
              buttonSelectLabel='Processar Selecionados', \
              buttonSubmit=True, buttonsAjax=[], buttonsAjaxProguess=[],
              orderBy=[], referback=[], width_label='25%', width_field='75%',
              filtros=[], buttonSelectProguess=[]):
        tabela.listdetail   = self.tabela(name, tabela)
        orderfield          = tabela.listdetail['orderfield']
        orderdirection      = tabela.listdetail['orderdirection']
        orderby             = tabela.listdetail['orderby']
        tabela.id.represent = lambda id: INPUT(_type='checkbox', _id='chk_id',\
                                              _name='chk_id', _value='%s' % id)
        for field in tabela.fields:
            if  field in fields:
                tabela[field].label = A(tabela[field].label,
                                        _href=URL('orderby', \
                                                    vars=dict(orderfield=field,
                                        orderdirection=orderdirection[field])))
        idreg = request.args(0) or 0
        if  not idreg:
            page = tabela.listdetail['page']
        else:
            page = 0
            if  query:
                if  orderBy:
                    if  orderBy[1].upper() == 'DESC':
                        rows = db(query).select(limitby=(page,page+4),\
                                                           orderby=~orderBy[0])
                    else:
                        rows = db(query).select(limitby=(page,page+4),\
                                                            orderby=orderBy[0])
                else:
                    rows = db(query).select(limitby=(page,page+4),\
                                                               orderby=orderby)
            else:
                if  orderBy:
                    rows = db(db[tabela]).select(limitby=(page,page+4),\
                                                               orderby=orderby)
                else:
                    rows = db(db[tabela]).select(limitby=(page,page+4),\
                                                               orderby=orderby)
            ok = False
            while rows:
                for row in rows:
                    if  row.id == int(idreg):
                        ok = True
                        break
                if  ok:
                    break
                else:
                    page += 4
                    if  query:
                        if  orderBy:
                            if  orderBy[1].upper() == 'DESC':
                                rows = db(query).select(limitby=(page,page+4),\
                                                           orderby=~orderBy[0])
                            else:
                                rows = db(query).select(limitby=(page,page+4),\
                                                            orderby=orderBy[0])
                        else:
                            rows = db(query).select(limitby=(page,page+4),\
                                                               orderby=orderby)
                    else:
                        if  orderBy:
                            if  orderBy[1].upper() == 'DESC':
                                rows = db(db[tabela]).select(limitby=\
                                             (page,page+4),orderby=~orderBy[0])
                            else:
                                rows = db(db[tabela]).select(limitby=\
                                              (page,page+4),orderby=orderBy[0])
                        else:
                            rows = db(db[tabela]).select(limitby=\
                                                 (page,page+4),orderby=orderby)
            if  not ok: page = 0
        if  len(fields):
            fields = [tabela[field] for field in fields]
        else:
            fields = [tabela[field] for field in tabela.fields]
        if  orderBy:
            if  orderBy[1].upper() == 'DESC':
                lista = str(crud.select(tabela, tabela.id>0, fields=fields, \
                                   limitby=[page,page+4], orderby=~orderBy[0]))
            else:
                lista = str(crud.select(tabela, tabela.id>0, fields=fields, \
                                    limitby=[page,page+4], orderby=orderBy[0]))
        else:
            lista = str(crud.select(tabela, tabela.id>0, fields=fields, \
                                       limitby=[page,page+4], orderby=orderby))
        if  query:
            if  orderBy:
                if  orderBy[1].upper() == 'DESC':
                    rowsdb = db(query).select(orderby=~orderBy[0])
                else:
                    rowsdb = db(query).select(orderby=orderBy[0])
            else:
                rowsdb = db(query).select(orderby=orderby)
        else:
            if  orderBy:
                if  orderBy[1].upper() == 'DESC':
                    rowsdb = db(db[tabela]).select(orderby=~orderBy[0])
                else:
                    rowsdb = db(db[tabela]).select(orderby=orderBy[0])
            else:
                rowsdb = db(db[tabela]).select(orderby=orderby)
        backward = A('<< Anterior', _href=URL('paginacao', args=[page-4])) \
                                                     if page else '<< Anterior'
        linhas   = db(db[tabela]).select(limitby=(page,page+4))
        qtde     = db(db[tabela]).count() if lista else 0
        forward  = A('Próxima >>', _href=URL('paginacao', args=[page+4])) \
                                             if qtde > page+4 else 'Próxima >>'
        nav      = "Exibindo %d ao %d de %d registros"  % (page+1 \
                     if qtde>0 else 0, page+len(linhas) if qtde>0 else 0, qtde)
        paginas  = [backward, forward, nav]
        lista   += '\r\n' + str(DIV(TABLE(TR(TD(paginas[0],
                                                  XML('&nbsp;&nbsp;&nbsp;'),
                                                  paginas[2],
                                                  XML('&nbsp;&nbsp;&nbsp;'),
                                                  paginas[1],
                                                  _align='right',
                                                  _width='100%')))))
        if  not scroll:
            listaScroll = ''
        else:
            listaScroll  = '<div class="scrollTable">\r\n'
            listaScroll += '    <table class="header">\r\n'
            listaScroll += '        <tr>\r\n'
            idx          = 0
            for field in fields:
                if  str(field)[len(str(tabela))+1:len(str(field))] == 'id':
                    listaScroll += "            <th style='width: " + \
                                                         scroll[idx] + "'>" + \
        "<input type='checkbox' class='chk_all' name='chk_all'/>" + '</th>\r\n'
                else:
                    listaScroll += "            <th style='width: " + \
                          scroll[idx] + "'>" + (str(field.label)) + '</th>\r\n'
                idx     += 1
            listaScroll += '        </tr>\r\n'
            listaScroll += '    </table>\r\n'
            listaScroll += '    <div class="scroller">\r\n'
            listaScroll += '        <table>\r\n'
            ocorid       = 0
            qtds         = 0
            for row in rowsdb:
                if  filtros:
                    ok = False
                    for filtro in filtros:
                        if  len(filtro) > 2:
                            if  eval('row.' + filtro[0] + ' ' + filtro[1] + \
                                                          ' ' + filtro[2]):
                                ok = True
                                break
                        else:
                            if  eval('row.' + filtro[0]) == filtro[1]:
                                ok = True
                                break
                    if  not ok:
                        continue
                listaScroll += '            <tr>\r\n'
                idx          = 0
                for field in fields:
                    cpo = str(field)[len(str(tabela))+1:len(str(field))]
                    if  cpo == 'id':
                        ocorid      += 1
                        cpoc         = XML("<input type='checkbox' class='" + \
                                           "chk_id' name='chk_id' value='"  + \
                                                           str(row.id) + "'/>")
                        listaScroll += "<th style='width: " + scroll[idx] + \
                                                "'> " + str(cpoc) + '</th>\r\n'
                    else:
                        try:
                            lookups = tabela.lookups
                        except:
                            lookups = {}
                        if  lookups and lookups.has_key(cpo):
                            lookup = db(db[lookups[cpo][0]].id==row[cpo]).\
                                                                       select()
                            if  lookup:
                                lkps = ''
                                for idy in xrange(0, len(lookups[cpo][1])):
                                    try:
                                        lkp = lookup[0][lookups[cpo][1][idy]]
                                    except:
                                        lkp = lookups[cpo][1][idy]
                                    lkps += lkp
                                listaScroll += " <th style='width: " + \
                                                         scroll[idx] + "'>" + \
                                    str(A(lkps if str(lkps) <> 'None' else \
                                   ' ',_href=URL(args=(row.id)))) + '</th>\r\n'
                            else:
                                listaScroll += " <th style='width: " + \
                                                         scroll[idx] + "'>" + \
                                    str(A(lookups[cpo][0],\
                                       _href=URL(args=(row.id)))) + '</th>\r\n'
                        else:
                            listaScroll += " <th style='width: " + \
                                                         scroll[idx] + "'>" + \
                                str(A(row[cpo] if str(row[cpo]) <> 'None' \
                              else ' ',_href=URL(args=(row.id)))) + '</th>\r\n'
                    idx += 1
                qtds += 1
                listaScroll += '            </tr>\r\n'
            listaScroll += '        </table>\r\n'
            listaScroll += '    </div>\r\n'
            listaScroll += '    <div align=\'right\'>\r\n'
            listaScroll += '        <table>\r\n'
            listaScroll += '            <tr>\r\n'
            listaScroll += '                <td">\r\n'
            listaScroll += '                    <h5>'
            listaScroll += '%s registro(s).' % qtds
            listaScroll += '                    </h5>\r\n'
            listaScroll += '                </td>\r\n'
            listaScroll += '            </tr>\r\n'
            listaScroll += '        </table>\r\n'
            listaScroll += '    </div>\r\n'
            listaScroll += '</div>\r\n'
        response.custom = XML(custom)
        response.right  = XML(right)
        if  search:
            response.search = XML('<hr/><h5>&nbsp;Filtro: &nbsp' + \
                                    str(SELECT([tabela[field].label \
                                for field in tabela.fields if field in search],
                                                  _id='keyfield',
                                                  _name='keyfield',
                                                  _style="width: 165px")) + \
                                                                  '</h5>' + \
                                    str(INPUT(_id='keyword',
                                          _name='keyword',
                                          _onkeyup=XML("ajax('" + \
                 URL('search') + "',['keyfield','keyword'],'target_search');"),
                                          _style=XML("width: 260px"))) + \
                                    str(DIV(_id='target_search')))
        else:
            response.search = ''
        return dict(titulos=titulos,
                    tabela=tabela,
                    form=form,
                    noList=noList,
                    detail=detail,
                    noDetail=noDetail,
                    noLookups=noLookups,
                    extra=extra,
                    livre=livre,
                    referback=referback,
                    optionDelete=optionDelete,
                    buttonClear=buttonClear,
                    buttonProcess=buttonProcess,
                    buttonProcessLabel=buttonProcessLabel,
                    buttonSelect=buttonSelect,
                    buttonSelectLabel=buttonSelectLabel,
                    buttonSelectProguess=buttonSelectProguess,
                    buttonSubmit=buttonSubmit,
                    buttonPopup=buttonPopup,
                    abas=abas,
                    lista=lista,
                    listaScroll=listaScroll,
                    query=query,
                    orderBy=orderBy,
                    buttons=buttons,
                    buttonsRefresh=buttonsRefresh,
                    buttonsAjax=buttonsAjax,
                    buttonsAjaxProguess=buttonsAjaxProguess,
                    popups=popups,
                    executes=executes,
                    paginas=paginas,
                    noCheckFields=noCheckFields,
                    keysCheckFields=keysCheckFields,
                    checkFields=checkFields,
                    width_label=width_label,
                    width_field=width_field)

    def orderby(self, name, tabela):
        tabela.listdetail = self.tabela(name, tabela)
        orderfield        = request.vars.orderfield     or 'id'
        orderdirection    = request.vars.orderdirection or 'desc'
        if  orderdirection == 'asc':
            tabela.listdetail['orderby'] = name + '.' + orderfield + ' asc'
            orderdirection               = 'desc'
        else:
            tabela.listdetail['orderby'] = name + '.' + orderfield + ' desc'
            orderdirection               = 'asc'
        tabela.listdetail['orderfield']                 = orderfield
        tabela.listdetail['orderdirection'][orderfield] = orderdirection

    def paginacao(self, name, tabela):
        tabela.listdetail['page'] = int(request.args(0)) or 0

    def search(self, name, tabela, query=''):
        tabela.listdetail = self.tabela(name, tabela)
        keyfields         = request.vars.keyfield
        label             = ''
        setLabel          = False
        for keyfield in keyfields:
            if  keyfield == '>':
                setLabel = True
                continue
            if  keyfield == '<':
                setLabel = False
                continue
            if  setLabel: label += keyfield
        field = label
        for fields in tabela.fields:
            if tabela[fields].label == label:
                field = fields
                break
        value = '%' + request.vars.keyword.lower() + '%'
        if  len(value) < 4: return ''
        try:
            ocor = tabela.lookups
        except:
            tabela.lookups = []
        if  not isinstance(query, list):
            query = [query]
        if  len(tabela.lookups):
            if  tabela.lookups.has_key(field):
                rows  = db(db[tabela.lookups[field][0]][tabela.lookups[field]\
                                                  [1][0]].like(value)).select()
                pages = db(db[tabela][field].belongs((row.id for row in \
                                      rows))).select(orderby=db[tabela][field])
                items = []
                for page in pages:
                    lookup = db(db[tabela.lookups[field][0]].id==page[field]).\
                                                                       select()
                    if  query[0] == '':
                        items.append(A(lookup[0][tabela.lookups[field][1]], \
                                           _href=URL('index', args=(page.id))))
                    else:
                        qry = ''
                        for qrx in query:
                            qry += (' ' if qry else '') + ('page.' \
                                 if qrx != 'and' and qry != 'or' else '') + qrx
                        if  eval(qry):
                            items.append(A(lookup[0][tabela.lookups[field][1]\
                                     [0]], _href=URL('index', args=(page.id))))
            else:
                rows  = db(db[tabela][field].lower().like(value)).\
                                              select(orderby=db[tabela][field])
                items = []
                for row in rows:
                    if  query[0] == '':
                        items.append(A(row[field], _href=URL('index', \
                                                               args=(row.id))))
                    else:
                        qry = ''
                        for qrx in query:
                            qry += (' ' if qry else '') + ('row.' \
                                 if qrx != 'and' and qry != 'or' else '') + qrx
                        if  eval(qry):
                            items.append(A(row[field], _href=URL('index', \
                                                               args=(row.id))))
        else:
            rows  = db(db[tabela][field].lower().like(value)).select(orderby=\
                                                             db[tabela][field])
            items = []
            for row in rows:
                if  query[0] == '':
                    items.append(A(row[field], _href=URL('index', \
                                                               args=(row.id))))
                else:
                    qry = ''
                    for qrx in query:
                        qry += (' ' if qry else '') + ('row.' if qrx != 'and' \
                                                 and qry != 'or' else '') + qrx
                    if  eval(qry):
                        items.append(A(row[field], _href=URL('index', \
                                                               args=(row.id))))
        return UL(*items).xml()

    def referback(self, idaplicacao, idstep, idcontroller, idobjeto):
        regstp = db(db.jobsteps.id==idstep).select().first()
        if  regstp.objeto == 'HPU':
            nome1 = 'nome1'
            nome2 = 'nome2'
            nome3 = 'nome3'
        elif  regstp.objeto == 'Programa':
            nome1 = 'nome2'
            nome2 = 'nome3'
            nome3 = 'nome4'
        elif  regstp.objeto == 'Programa (CKRS)':
            nome1 = 'nome2'
            nome2 = 'nome3'
            nome3 = 'nome4'
        elif  regstp.objeto == 'Sort Tabela':
            nome1 = 'nome2'
            nome2 = 'nome3'
            nome3 = 'nome4'
        else:
            nome1 = 'nome1'
            nome2 = 'nome2'
            nome3 = 'nome3'
        regsteps = db(db.jobsteps).select(orderby='job,step,sequencia')
        items    = ''
        rotina   = ''
        job      = 0
        step     = ''
        ocor     = 0
        qtde     = len(regsteps)
        for regstep in regsteps:
            ocor  += 1
            regjob = db(db.jobs.id==regstep.job).select().first()
            if  regjob.codigoAplicacao <> idaplicacao:
                continue
            if  regstep.job == int(session.idjob or 0) and \
                                  (regstep.step == session.get('step', '') or \
                              regstep.sequencia > int(session.sequencia or 0)):
                continue
            if  regjob.rotine <> rotina:
                items += ('</ul></ul></ul><ul>' if items else '<ul>') + \
                            '<li>Rotina: %s</li>' % regjob.rotine
                rotina = regjob.rotine
                items += '<ul><li>Job: %s</li>' % regjob.name
                job    = regstep.job
                items += '<ul><li>%s - %s %s</li>' % \
                               (regstep.step, regstep.objeto, regstep.dsObjeto)
                step   = regstep.step
            else:
                if  regstep.job <> job:
                    items += ('</ul><ul>' if items else '<ul>') + \
                                '<li>Job: %s</li>' % regjob.name
                    job    = regstep.job
                    items += '<ul><li>%s - %s %s</li>' % \
                               (regstep.step, regstep.objeto, regstep.dsObjeto)
                    step   = regstep.step
                else:
                    if  regstep.step <> step:
                        items += '%s<ul><li>%s - %s %s</li>' % \
                                                 ('<ul>' if ocor==qtde else '',
                                                  regstep.step, regstep.objeto, 
                                                              regstep.dsObjeto)
                        step   = regstep.step
            if  regstep.objeto == 'HPU':
                reghpu = db(db.hpus.id==regstep.idObjeto).select().first()
                if  not reghpu:
                    items += '<ul><li>Nenhuma saida definida</li></ul>'
                else:
                    regent = db(db.tabelas.id==reghpu.codigoEntidade).\
                                                               select().first()
                    items += '<ul>'
                    dsname = 'SYSREC01 - AD.C87.%s.%s' % (regjob.rotine + \
                                      'S%s.HPU.SYSREC01' % regstep.sequencia, \
                                                            regent.nome)
                    if  regstep.job == int(session.idjob or 0):
                        vlr1 = '*'
                        vlr2 = step
                        vlr3 = 'SYSREC01'
                        vlr4 = ''
                    else:
                        vlr1 = regjob.rotine + \
                               'S%s' % '{:>02}'.format(regstep.sequencia)
                        vlr2 = 'SYSREC01'
                        vlr3 = regent.nome
                        vlr4 = ''
                    items += '<li>' + \
                                  str(A(dsname, _style=XML('cursor: pointer'),\
                        _onclick=XML("jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome1, vlr1) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome2, vlr2) + \
                               "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome3, vlr3) + \
                                 ("jQuery('#%s_nome4').attr('value','%s');" % \
                                                         (idcontroller, vlr4) \
                               if  regstp.objeto == 'Sort Arquivo' else '') + \
                              "jQuery('#referback_%s').text('');" % idobjeto)))
                items += '</li>'
                items += '</ul>'
            if  regstep.objeto == 'Programa':
                regnens  = db(db.prognens.id==regstep.idObjeto).\
                                                               select().first()
                if  not regnens:
                    items += '<ul><li>Nenhuma saida definida</li></ul>'
                else:
                    idx       = 0
                    regnens4s = db(db.prognens4.prognens==regnens.id).select()
                    for regnens4 in regnens4s:
                        idx   += 1
                        items += '<ul>'
                        dsname = '%s - AD.C87.%s%s%s%s' % \
                              (regnens4.nome1, regjob.rotine + 'S%s' % \
                                          '{:>02}'.format(regstep.sequencia), \
                              ('.' + regnens4.nome3) if regnens4.nome3 else '',
                              ('.' + regnens4.nome4) if regnens4.nome4 else '',
                              ('.' + regnens4.nome5) if regnens4.nome5 else '')
                        if  regstep.job == int(session.idjob or 0):
                            vlr1 = '*'
                            vlr2 = step
                            vlr3 = regnens4.nome1
                            vlr4 = ''
                        else:
                            vlr1 = regjob.rotine + 'S%s' % \
                                             '{:>02}'.format(regstep.sequencia)
                            vlr2 = (regnens4.nome3) if regnens4.nome3 else ''
                            vlr3 = (regnens4.nome4) if regnens4.nome4 else ''
                            vlr4 = (regnens4.nome5) if regnens4.nome5 else ''
                        items += '<li>' + \
                                  str(A(dsname, _style=XML('cursor: pointer'),\
                        _onclick=XML("jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome1, vlr1) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome2, vlr2) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome3, vlr3) + \
                                 ("jQuery('#%s_nome4').attr('value','%s');" % \
                                                         (idcontroller, vlr4) \
                               if  regstp.objeto == 'Sort Arquivo' else '') + \
                              "jQuery('#referback_%s').text('');" % idobjeto)))
                        items += '</li>'
                        items += '</ul>'
                    if  not idx:
                        items += '<ul><li>Nenhuma Saida definida</li></ul>'
            if  regstep.objeto == 'Programa (CKRS)':
                regckrs  = db(db.progckrs.id==regstep.idObjeto).\
                                                               select().first()
                if  not regckrs:
                    items += '<ul><li>Nenhuma saida definida</li></ul>'
                else:
                    idx       = 0
                    regckrs4s = db(db.progckrs4.progckrs==regckrs.id).select()
                    for regckrs4 in regckrs4s:
                        idx   += 1
                        items += '<ul>'
                        dsname = '%s - AD.C87.%s%s%s%s' % \
                              (regnens4.nome1, regjob.rotine + 'S%s' % \
                                          '{:>02}'.format(regstep.sequencia), \
                              ('.' + regckrs4.nome3) if regckrs4.nome3 else '',
                              ('.' + regckrs4.nome4) if regckrs4.nome4 else '',
                              ('.' + regckrs4.nome5) if regckrs4.nome5 else '')
                        if  regstep.job == int(session.idjob or 0):
                            vlr1 = '*'
                            vlr2 = step
                            vlr3 = regckrs4.nome1
                            vlr4 = ''
                        else:
                            vlr1 = regjob.rotine + 'S%s' % \
                                             '{:>02}'.format(regstep.sequencia)
                            vlr2 = (regckrs4.nome3) if regckrs4.nome3 else ''
                            vlr3 = (regckrs4.nome4) if regckrs4.nome4 else ''
                            vlr4 = (regckrs4.nome5) if regckrs4.nome5 else ''
                        items += '<li>' + \
                                  str(A(dsname, _style=XML('cursor: pointer'),\
                        _onclick=XML("jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome1, vlr1) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome2, vlr2) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome3, vlr3) + \
                                 ("jQuery('#%s_nome4').attr('value','%s');" % \
                                                         (idcontroller, vlr4) \
                               if  regstp.objeto == 'Sort Arquivo' else '') + \
                              "jQuery('#referback_%s').text('');" % idobjeto)))
                        items += '</li>'
                        items += '</ul>'
                    if  not idx:
                        items += '<ul><li>Nenhuma Saida definida</li>'
            if  regstep.objeto == 'Sort Tabela':
                reg1s  = db(db.sort1s.id==regstep.idObjeto).select().first()
                if  not reg1s:
                    items += '<ul><li>Nenhuma saida definida</li></ul>'
                else:
                    regent = db(db.tabelas.id==reg1s.codigoEntidade).\
                                                               select().first()
                    items += '<ul>'
                    dsname = 'SORTOUT - AD.C87.%s%s%s' % \
                        (regjob.rotine + 'S%s.SORT' % \
                                   '{:>02}'.format(regstep.sequencia), \
                                   '.' + regent.nome,
                                   '.' + reg1s.jobArqName)
                    if  regstep.job == int(session.idjob or 0):
                        vlr1 = '*'
                        vlr2 = step
                        vlr3 = 'SORTOUT'
                        vlr4 = ''
                    else:
                        vlr1 = regjob.rotine
                        vlr2 = 'S%s.SORT' % '{:>02}'.format(regstep.sequencia)
                        vlr3 = regent.nome
                        vlr4 = reg1s.jobArqName
                    items += '<li>' + \
                                  str(A(dsname, _style=XML('cursor: pointer'),\
                        _onclick=XML("jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome1, vlr1) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome2, vlr2) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome3, vlr3) + \
                                 ("jQuery('#%s_nome4').attr('value','%s');" % \
                                                         (idcontroller, vlr4) \
                               if  regstp.objeto == 'Sort Arquivo' else '') + \
                              "jQuery('#referback_%s').text('');" % idobjeto)))
                items += '</li>'
                items += '</ul>'
            if  regstep.objeto == 'Sort Arquivo':
                regnens  = db(db.sortnens.id==regstep.idObjeto).\
                                                               select().first()
                if  not regnens:
                    items += '<ul><li>Nenhuma saida definida</li></ul>'
                else:
                    regnens4s = db(db.sortnens4.sortnens==regnens.id).select()
                    idx       = 0
                    for regnens4 in regnens4s:
                        idx   += 1
                        items += '<ul>'
                        origem = 'SYSOUT%s' % '{:>02}'.format(idx)
                        dsname = 'SYSOUT%s - AD.C87.%s%s%s' % \
                                     ('{:>02}'.format(idx), regjob.rotine + \
                        'S%s.SORT' % '{:>02}'.format(regstep.sequencia), \
                        '.' + regnens4.nome1, \
                              ('.' + regnens4.nome2) if regnens4.nome2 else '')
                        if  regstep.job == int(session.idjob or 0):
                            vlr1 = '*'
                            vlr2 = step
                            vlr3 = origem
                            vlr4 = ''
                        else:
                            vlr1 = regjob.rotine + \
                                'S%s' % '{:>02}'.format(regstep.sequencia)
                            vlr2 = 'SORT'
                            vlr3 = regnens4.nome1
                            vlr4 = (regnens4.nome2) if regnens4.nome2 else ''
                        items += '<li>' + \
                                  str(A(dsname, _style=XML('cursor: pointer'),\
                        _onclick=XML("jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome1, vlr1) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome2, vlr2) + \
                                     "jQuery('#%s_%s').attr('value','%s');" % \
                                                (idcontroller, nome3, vlr3) + \
                                 ("jQuery('#%s_nome4').attr('value','%s');" % \
                                                         (idcontroller, vlr4) \
                               if  regstp.objeto == 'Sort Arquivo' else '') + \
                              "jQuery('#referback_%s').text('');" % idobjeto)))
                        items += '</li>'
                        items += '</ul>'
                    if  not idx:
                        items += '<ul><li>Nenhuma Saida definida</li></ul>'
            items += '</ul>'
        return XML(items)

    def download(self, request, response, filedir=None, filename=None, \
                      chunk_size=streamer.DEFAULT_CHUNK_SIZE, attachment=True):
        if  not filedir or not filename:
            return ''
        filedirname = filedir + filename
        response.headers['Content-Type'] = c.contenttype(filedirname)
        if  attachment:
            response.headers['Content-Disposition'] = \
                                           "attachment; filename=%s" % filename
        return response.stream(filedirname, chunk_size=chunk_size, \
                                                               request=request)

listdetail = listdetail()
