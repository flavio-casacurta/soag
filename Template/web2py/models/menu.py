# coding: utf8

class dtree(object):

    def __init__(self):

        self.versao = 1.0

        self.clean()

    def clean(self):

        self.idx = 0

        self.menus = []

    def menu(self, label, parent=''):

        self.idx += 1

        if  not parent:

            self.menus.append([self.idx, 0, label, ''])

        else:

            idx = 0

            for x in self.menus:

                if  x[2] == parent:

                    idx = x[0]

                    break

            self.menus.append([self.idx, idx, label, ''])

    def aplicacao(self, menu, label, url):

        self.idx += 1

        idx = 0

        for x in self.menus:

            if  x[2] == menu:

                idx = x[0]

                break

        self.menus.append([self.idx, idx, label, url])

    def html(self):

        if  not self.menus: return ''

        dt   = '<div class="dtree"> '

        dt  += '<script type="text/javascript"> '

        dt  += "d = new dTree('d', '" + URL(request.application, 'static', \
                               'menu/dtree/images/').replace('//','/') + "'); "

        dt  += "d.add(0,-1,'Menu'); "

        for x in self.menus:

            dt += "d.add(" + str(x[0]) + "," + str(x[1]) + ",'"  + \
                                                   x[2]  + "','" + \
                                                   x[3]  + "');"

        dt += 'd.draw(); '

        dt += '</script> '

        dt += '</div>'

        return XML(dt)

class etree():

    def __init__(self):
        self.versao = 1.0

    def menu(self, opcoes=[]):
        if  not response.etree:
            return ''
        if (auth.user) and (auth.has_membership(1, auth.user.id, \
                'Administrador')):
            qtde   = len(opcoes) + 1
            etree  = "<div class='titulo_menu'>"  + '&nbsp;' * 4 + \
                        "<a href=\"javascript:void(escondediv('%s',%s))\" " \
                                % (1, qtde)
            etree += "class='link_menu'>web2py</a></div> "
            etree += "<div id='mdiv1' style='display:none'> "
            etree += "<table border='0'> "
            etree += "<tr><td class='itens_menu'>"  + '&nbsp;' * 4 + \
                        "<a href='%s' class='link_smenu'>%s</a></td></tr> " % \
                            (URL('admin', 'default', 'index'), 'Sistema')
            etree += "<tr><td class='itens_menu'>"  + '&nbsp;' * 4 + \
                        "<a href='%s' class='link_smenu'>%s</a></td></tr> " % \
                            (URL(request.application, 'appadmin', 'index'), \
                                'Aplicação')
            etree += "<tr><td class='itens_menu'>"  + '&nbsp;' * 4 + \
                        "<a href='%s' class='link_smenu'>%s</a></td></tr> " % \
                            (URL('admin',             'default',   'design', \
                                args=[request.application]), 'Design')
            etree += "<tr><td class='itens_menu'>"  + '&nbsp;' * 4 + \
                        "<a href='%s' class='link_smenu'>%s</a></td></tr> " % \
                            (URL(request.application, 'appadmin',  'state'), \
                                'State')
            etree += "<tr><td class='itens_menu'>"  + '&nbsp;' * 4 + \
                        "<a href='%s' class='link_smenu'>%s</a></td></tr> " % \
                            (URL(request.application, 'appadmin',  'ccache'), \
                                'Cache')
            etree += "</table> "
            etree += "</div>"
            idx    = 1
        else:
            qtde   = len(opcoes)
            idx    = 0
            etree  = ''
        for opcs in opcoes:
            idx   += 1
            etree += "<div class='titulo_menu'>"  + '&nbsp;' * 4 + \
                        "<a href=\"javascript:void(escondediv('%s',%s))\" " \
                                % (idx, qtde, opcs[0])
            etree += "class='link_menu'>%s</a></div> "
            etree += "<div id='mdiv%s' style='display:none'> " % idx
            etree += "<table border='0'> "
            for opc in opcs[1]:
                etree += "<tr><td class='itens_menu'>"  + '&nbsp;' * 4 + \
                            "<a href='%s' class='link_smenu'>%s" \
                                    % (opc[1], opc[0])
                etree += "</a></td></tr> "
            etree += "</table> "
            etree += "</div>"
        return XML(etree)

class wtree():

    def __init__(self):
        self.versao = 1.0

    def menu(self, opcoes=[]):
        if  not response.wtree:
            return ''
        wtree  = '<div id="menu">\n'
        wtree += '    <script type="text/javascript">\n'
        idmenu = 0
        if  (auth.user) and \
            (auth.has_membership(1, auth.user.id, 'Administrador')):
            idmenu += 1
            wtree  += '    var m%s = new MenuWin("menu","%s",false,"%s");\n' \
                            % (idmenu, 'mm%s' % idmenu, \
                                URL(request.application, \
                                    'static', 'menu/wtree/'))
            wtree  += '    m%s.setTitle("web2py");\n' % idmenu
            wtree  += '    m%s.setItens("Sistema",  "%s",null,"%s");\n' % \
                        (idmenu, URL('admin', 'default', 'index'), \
                            URL(request.application, 'static', \
                                'menu/wtree/ofolder.gif'))
            wtree  += '    m%s.setItens("Aplicação","%s",null,"%s");\n' % \
                        (idmenu, URL(request.application, 'appadmin', \
                            'index'), \
                                URL(request.application, 'static', \
                                    'menu/wtree/ofolder.gif'))
            wtree  += '    m%s.setItens("Design", "%s",null,"%s");\n' % \
                        (idmenu, URL('admin', 'default', 'design', \
                            args=[request.application]), \
                                URL(request.application, 'static', \
                                    'menu/wtree/ofolder.gif'))
            wtree  += '    m%s.setItens("State", "%s",null,"%s");\n' % \
                        (idmenu, URL(request.application, 'appadmin', \
                            'state'),  \
                                URL(request.application, 'static', \
                                    'menu/wtree/ofolder.gif'))
            wtree  += '    m%s.setItens("Cache", "%s",null,"%s");\n' % \
                        (idmenu, URL(request.application, 'appadmin', \
                            'ccache'), \
                                URL(request.application, 'static', \
                                    'menu/wtree/ofolder.gif'))
        for opcs in opcoes:
            idmenu += 1
            wtree  += '    var m%s = new MenuWin("menu","%s",false,"%s");\n' \
                        % (idmenu, 'mm%s' % idmenu, URL(request.application, \
                            'static', 'menu/wtree/'))
            wtree  += '    m%s.setTitle("%s");\n' % (idmenu, opcs[0])
            for opc in opcs[1]:
                wtree += '    m%s.setItens("%s","%s",null,"%s");\n' % \
                            (idmenu, opc[0], opc[1], URL(request.application, \
                                'static', 'menu/wtree/ofolder.gif'))
        wtree += '    </script>\n'
        wtree += '</div>\n'
        return XML(wtree)
