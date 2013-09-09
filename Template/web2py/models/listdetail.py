# coding: utf8

from gluon import streamer, contenttype as c

class listdetail():

    def tabela(self, name, tabela):
        if  'pks' not in tabela:
            if  '_primarykey' not in tabela:
                tabela._primarykey = ['id' if 'id' in tabela else tabela.fields[0]]
            tabela.pks = tabela._primarykey
        if  name not in session:
            session[name] = dict()
        if  'listdetail' not in session[name]:
            session[name]['listdetail'] = dict()
        tb = session[name]
        orderdirection = dict()
        for field in tabela.fields:
            orderdirection[field] = 'desc'
        tb['listdetail']['page'] = 0
        if  'orderfield' not in tb['listdetail']:
            tb['listdetail']['orderfield'] = tabela.pks[0]
        if  'orderdirection' not in tb['listdetail']:
            tb['listdetail']['orderdirection'] = orderdirection
        if  'orderby' not in tb['listdetail']:
            tb['listdetail']['orderby'] = name + '.' + tabela.pks[0] + ' asc'
        return tb['listdetail']

    def index(self, titulos, name, tabela, query, form, noList=False,
              detail=[], noDetail=[], noLookups=[], abas=dict(), fields=[],
              scroll=[], noCheckFields=[], keysCheckFields=[], livre='',
              checkFields={}, custom='', right='', labelId='', search=[],
              buttons=[], buttonsRefresh=[], popups=[], executes=[],
              optionDelete=True, reference={}, extra=[], buttonClear=True,
              buttonProcess=False, buttonProcessLabel='Processar',
              buttonSelect=False, buttonPopup=False,
              buttonSelectLabel='Processar Selecionados',
              buttonSubmit=True, buttonsAjax=[], buttonsAjaxProguess=[],
              orderBy=[], referback=[], width_label='25%', width_field='75%',
              filtros=[], buttonSelectProguess=[]):
        tabela.listdetail   = self.tabela(name, tabela)
        orderfield          = tabela.listdetail['orderfield']
        orderdirection      = tabela.listdetail['orderdirection']
        orderby             = tabela.listdetail['orderby']
        if  'id' in tabela:
            tabela.id.represent = lambda id: INPUT(_type='checkbox', _id='chk_id', _name='chk_id', _value='%s' % id)
        for field in tabela.fields:
            if  field in fields:
                tabela[field].label = A(tabela[field].label, _href=URL('orderby', vars=dict(orderfield=field, orderdirection=orderdirection[field])))
        idreg = request.args(0) or ''
        if  not idreg:
            page = tabela.listdetail['page']
        else:
            page = 0
            if  query:
                if  orderBy:
                    if  orderBy[1].upper() == 'DESC':
                        rows = db(query).select(limitby=(page,page+4), orderby=~orderBy[0])
                    else:
                        rows = db(query).select(limitby=(page,page+4), orderby=orderBy[0])
                else:
                    rows = db(query).select(limitby=(page,page+4), orderby=orderby)
            else:
                if  orderBy:
                    rows = db(db[tabela]).select(limitby=(page,page+4), orderby=orderby)
                else:
                    rows = db(db[tabela]).select(limitby=(page,page+4), orderby=orderby)
            ok = False
            while rows:
                for row in rows:
                    k = ''
                    for v in tabela.pks:
                        k += str(eval('row.'+v))
                    if  eval(k+'=='+str(idreg)):
                        ok = True
                        break
                if  ok:
                    break
                else:
                    page += 4
                    if  query:
                        if  orderBy:
                            if  orderBy[1].upper() == 'DESC':
                                rows = db(query).select(limitby=(page,page+4), orderby=~orderBy[0])
                            else:
                                rows = db(query).select(limitby=(page,page+4), orderby=orderBy[0])
                        else:
                            rows = db(query).select(limitby=(page,page+4), orderby=orderby)
                    else:
                        if  orderBy:
                            if  orderBy[1].upper() == 'DESC':
                                rows = db(db[tabela]).select(limitby=(page,page+4),orderby=~orderBy[0])
                            else:
                                rows = db(db[tabela]).select(limitby=(page,page+4),orderby=orderBy[0])
                        else:
                            rows = db(db[tabela]).select(limitby=(page,page+4),orderby=orderby)
            if  not ok: page = 0
        if  len(fields):
            fields = [tabela[field] for field in fields]
        else:
            fields = [tabela[field] for field in tabela.fields]
        if  orderBy:
            if  orderBy[1].upper() == 'DESC':
                lista = str(crud.select(tabela, eval('tabela.'+tabela.pks[0]+'>0'), fields=fields, limitby=[page,page+4], orderby=~orderBy[0]))
            else:
                lista = str(crud.select(tabela, eval('tabela.'+tabela.pks[0]+'>0'), fields=fields, limitby=[page,page+4], orderby=orderBy[0]))
        else:
            lista = str(crud.select(tabela, eval('tabela.'+tabela.pks[0]+'>0'), fields=fields, limitby=[page,page+4], orderby=orderby))
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
        backward = (A('<< Anterior', _href=URL('paginacao', args=[page-4])) if page else '<< Anterior')
        linhas   = db(db[tabela]).select(limitby=(page,page+4))
        qtde     = db(db[tabela]).count() if lista else 0
        forward  = (A('Próxima >>', _href=URL('paginacao', args=[page+4])) if qtde > page+4 else 'Próxima >>')
        nav      = "Exibindo %d ao %d de %d registros"  % (page+1 if qtde>0 else 0, page+len(linhas) if qtde>0 else 0, qtde)
        paginas  = [backward, forward, nav]
        lista   += '\r\n' + str(DIV(TABLE(TR(TD(paginas[0], XML('&nbsp;&nbsp;&nbsp;'), paginas[2], XML('&nbsp;&nbsp;&nbsp;'), paginas[1], _align='right', _width='100%')))))
        if  not scroll:
            listaScroll = ''
        else:
            listaScroll  = '<div class="scrollTable">\r\n'
            listaScroll += '    <table class="header">\r\n'
            listaScroll += '        <tr>\r\n'
            idx          = 0
            for field in fields:
                if  str(field)[len(str(tabela))+1:len(str(field))] == 'id':
                    listaScroll += ("            <th style='width: " + scroll[idx] + "'>" + "<input type='checkbox' class='chk_all' name='chk_all'/>" + '</th>\r\n')
                else:
                    listaScroll += ("            <th style='width: " + scroll[idx] + "'>" + (str(field.label)) + '</th>\r\n')
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
                            if  eval('row.' + filtro[0] + ' ' + filtro[1] + ' ' + filtro[2]):
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
                        cpoc         = XML("<input type='checkbox' class='" + "chk_id' name='chk_id' value='"  + str(row.id) + "'/>")
                        listaScroll += ("<th style='width: " + scroll[idx] + "'> " + str(cpoc) + '</th>\r\n')
                    else:
                        try:
                            lookups = tabela.lookups
                        except:
                            lookups = {}
                        args = ''
                        for v in tabela.pks:
                            args += str(eval('row.'+v))
                        if  lookups and lookups.has_key(cpo):
                            if  'id' in tabela:
                                lookup = db(eval('db[lookups[cpo][0]].'+tabela.pks[0]+'=='+str(row[cpo]))).select()
                            else:
                                lookup = db(eval('db[lookups[cpo][0]].'+cpo+'=='+str(row[cpo]))).select()
                            if  lookup:
                                lkps = ''
                                for idy in xrange(0, len(lookups[cpo][1])):
                                    try:
                                        lkp = lookup[0][lookups[cpo][1][idy]]
                                    except:
                                        lkp = lookups[cpo][1][idy]
                                    lkps += lkp
                                listaScroll += (" <th style='width: " + scroll[idx] + "'>" + str(A(lkps if str(lkps) <> 'None' else ' ',_href=URL(args=(args)), _onClick="setScroll();")) + '</th>\r\n')
                            else:
                                listaScroll += (" <th style='width: " + scroll[idx] + "'>" + str(A(lookups[cpo][0] if row[cpo] != 0 else ' ', _href=URL(args=(args)), _onClick="setScroll();")) + '</th>\r\n')
                        else:
                            listaScroll += (" <th style='width: " + scroll[idx] + "'>" + str(A(row[cpo] if str(row[cpo]) <> 'None' else ' ',_href=URL(args=(args)), _onClick="setScroll();")) + '</th>\r\n')
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
            response.search = XML('<hr/><h5>&nbsp;Filtro: &nbsp' +
                                  str(SELECT([tabela[field].label
                                  for field in tabela.fields if field in search],
                                            _id='keyfield',
                                            _name='keyfield',
                                            _style="width: 165px")) +
                                            '</h5>' +
                                  str(INPUT(_id='keyword',
                                            _name='keyword',
                                            _onkeyup=XML("ajax('" +
                                  URL('search') + "',['keyfield','keyword'],'target_search');"),
                                            _style=XML("width: 260px"))) +
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
        orderfield        = request.vars.orderfield
        orderdirection    = request.vars.orderdirection or 'desc'
        if  orderdirection == 'asc':
            tabela.listdetail['orderby'] = name + '.' + orderfield + ' asc'
            orderdirection               = 'desc'
        else:
            tabela.listdetail['orderby'] = name + '.' + orderfield + ' desc'
            orderdirection               = 'asc'
        tabela.listdetail['orderfield']  = orderfield
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
                rows  = db(db[tabela.lookups[field][0]][tabela.lookups[field][1][0]].like(value)).select()
                pages = db(db[tabela][field].belongs((eval('row.'+tabela.pks[0]) for row in rows))).select(orderby=db[tabela][field])
                items = []
                for page in pages:
                    args = ''
                    for v in tabela.pks:
                        args += str(eval('page.'+v))
                    lookup = db(eval('db[tabela.lookups[field][0]].'+tabela.pks[0]+'==page[field]')).select()
                    if  query[0] == '':
                        items.append(A(lookup[0][tabela.lookups[field][1]], _href=URL('index', args=(args))))
                    else:
                        qry = ''
                        for qrx in query:
                            qry += (' ' if qry else '') + ('page.' if qrx != 'and' and qry != 'or' else '') + qrx
                        if  eval(qry):
                            items.append(A(lookup[0][tabela.lookups[field][1][0]], _href=URL('index', args=(args))))
            else:
                rows  = db(db[tabela][field].lower().like(value)).select(orderby=db[tabela][field])
                items = []
                for row in rows:
                    args = ''
                    for v in tabela.pks:
                        args += str(eval('row.'+v))
                    if  query[0] == '':
                        items.append(A(row[field], _href=URL('index', args=(args))))
                    else:
                        qry = ''
                        for qrx in query:
                            qry += (' ' if qry else '') + ('row.' if qrx != 'and' and qry != 'or' else '') + qrx
                        if  eval(qry):
                            items.append(A(row[field], _href=URL('index', args=(args))))
        else:
            rows  = db(db[tabela][field].lower().like(value)).select(orderby=db[tabela][field])
            items = []
            for row in rows:
                args = ''
                for v in tabela.pks:
                    args += str(eval('row.'+v))
                if  query[0] == '':
                    items.append(A(row[field], _href=URL('index', args=(args))))
                else:
                    qry = ''
                    for qrx in query:
                        qry += (' ' if qry else '') + ('row.' if qrx != 'and' and qry != 'or' else '') + qrx
                    if  eval(qry):
                        items.append(A(row[field], _href=URL('index', args=(args))))
        return UL(*items).xml()

    def download(self, request, response, filedir=None, filename=None, chunk_size=streamer.DEFAULT_CHUNK_SIZE, attachment=True):
        if  not filedir or not filename:
            return ''
        filedirname = filedir + filename
        response.headers['Content-Type'] = c.contenttype(filedirname)
        if  attachment:
            response.headers['Content-Disposition'] = "attachment; filename=%s" % filename
        return response.stream(filedirname, chunk_size=chunk_size, request=request)

listdetail = listdetail()

# vim: ft=python
