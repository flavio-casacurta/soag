# -*- coding: utf-8 -*-

# -*- coding:utf-8
'''
   Created on 22/10/2011
   @author: C&C - HardSoft
'''
import win32, time

class Erwin():

    def __init__(self):

        self._entitys         = {}
        self._LogEntidades    = {}
        self._FisEntidades    = {}
        self._attributes      = {}
        self._colunas         = {}
        self._domains         = {}
        self._dominios        = {}
        self._keyGroups       = {}
        self._chaves          = []
        self._relationShips   = {}
        self._relacoes        = {}
        self._entidadeColunas = {}

    def load(self, arquivo='', picke=''):

        t0 = time.time()

        print ' '
        print 'Loading ...'

        if  arquivo:
            _erwin = win32.Erwin(arquivo)
            if  _erwin.erro:
                return _erwin.erro
            self._entitys       = _erwin.entitys
            self._attributes    = _erwin.attributes
            self._domains       = _erwin.domains
            self._keyGroups     = _erwin.keyGroups
            self._relationShips = _erwin.relationShips

        if  picke:
            self._entitys       = picke['entitys']
            self._attributes    = picke['attributes']
            self._domains       = picke['domains']
            self._keyGroups     = picke['keyGroups']
            self._relationShips = picke['relationShips']

        self.__setDominios__()
        self.__setChaves__()
        self.__setRelacoes__()
        self.__setEntidades__()
        self.__setColunas__()
        self.__setEntidadeColunas__()

        print '        Tempo corrido:', time.time() - t0

        return {'retorno': True,
                'flash': 'loading erwin ok',
                'labelErrors': 'ok: AllFusionERwin.SCAPI',
                'msgsErrors': ''}

    def __setDominios__(self):

        for erwinDomain in self._domains:

            attrs = {}

            for key in self._domains[erwinDomain]:

                k = key.split(' = ')[0]
                v = key.split(' = ')[1]

                attrs[k] = True if v == 'True'  else False \
                                if v == 'False' else v

            self._dominios[attrs['Long_Id']] = attrs

    def __setChaves__(self):

        for erwinKey in self._keyGroups:

            attrs = {}

            keys = self._keyGroups[erwinKey]

            for key in keys:

                k = key.split(' = ')[0]
                v = key.split(' = ')[1]

                if  k == 'Name' and len(attrs) > 1:
                    if  not 'Attribute_Ref' in attrs:
                        attrs['Attribute_Ref'] = ''
                    self._chaves.append(attrs)
                    attrs = {}

                attrs[k] = True if v == 'True'  else False \
                                if v == 'False' else v

            if  not 'Attribute_Ref' in attrs:
                attrs['Attribute_Ref'] = ''

            self._chaves.append(attrs)

    def __setRelacoes__(self):

        for erwinRelationShip in self._relationShips:

            attrs = {}

            for key in self._relationShips[erwinRelationShip]:

                k = key.split(' = ')[0]
                v = key.split(' = ')[1]

                attrs[k] = True if v == 'True'  else False \
                                if v == 'False' else v

            self._relacoes[attrs['Long_Id']] = attrs

    def __setEntidades__(self):

        for erwinEntity in self._entitys:

            attrs = {}

            for entity in self._entitys[erwinEntity]:

                k = entity.split(' = ')[0]
                v = entity.split(' = ')[1]

                attrs[k] = True if v == 'True'  else False \
                                if v == 'False' else v

            if  not 'Name' in attrs:
                attrs['Name'] = ''

            if  not 'Physical_Name' in attrs:
                attrs['Physical_Name'] = ''

            if  not 'Name_Qualifier' in attrs:
                attrs['Name_Qualifier'] = ''

            if  not 'Entity.Physical.CentroCusto' in attrs:
                attrs['Entity.Physical.CentroCusto'] = ''

            if  not 'Entity.Physical.NumeroTabela' in attrs:
                attrs['Entity.Physical.NumeroTabela'] = ''

            if  not 'Parent_Relationships_Ref' in attrs:
                attrs['Parent_Relationships_Ref'] = ''

            self._LogEntidades[attrs['Name']] = attrs
            self._FisEntidades[attrs['Physical_Name']] = attrs

    def __setColunas__(self):

        for erwinAttribute in self._attributes:

            attrs = {}

            for attribute in self._attributes[erwinAttribute]:

                k = attribute.split(' = ')[0]
                v = attribute.split(' = ')[1]

                attrs[k] = True if v == 'True'  else False \
                                if v == 'False' else v

                if  k == 'Definition' and len(attrs) > 1:
                    domain = self.getDominios(attrs['Parent_Domain_Ref'])
                    if  attrs['Name'].upper() == '%AttDomain'.upper():
                        if  'User_Formatted_Name' in attrs and \
                            attrs['User_Formatted_Name'].upper() != '%AttDomain'.upper():
                            attrs['Name'] = attrs['User_Formatted_Name']
                        else:
                            if  domain:
                                attrs['Name'] = domain['Name']
                                attrs['User_Formatted_Name'] = domain['Name']
                            else:
                                attrs['Name'] = ''
                                attrs['User_Formatted_Name'] = ''
                    if  attrs['Physical_Name'].upper() == '%ColDomain'.upper():
                        if  'User_Formatted_Physical_Name' in attrs and \
                            attrs['User_Formatted_Physical_Name'].upper() != \
                                                                  '%ColDomain'.upper():
                            attrs['Physical_Name'] = \
                                          attrs['User_Formatted_Physical_Name']
                        else:
                            if  domain:
                                attrs['Physical_Name'] = \
                                                        domain['Physical_Name']
                                attrs['User_Formatted_Physical_Name'] = \
                                                        domain['Physical_Name']
                            else:
                                attrs['Physical_Name'] = ''
                                attrs['User_Formatted_Physical_Name'] = ''
                    if  not 'Parent_Attribute_Ref' in attrs:
                        attrs['Parent_Attribute_Ref'] = ''
                    if  not 'Parent_Relationship_Ref' in attrs:
                        attrs['Parent_Relationship_Ref'] = ''
                    if  not 'Definition' in attrs:
                        if  'Comment' in attrs:
                            attrs['Definition'] = attrs['Comment']
                        else:
                            attrs['Definition'] = ''
                            attrs['Comment'] = ''
                    if  not 'Attribute_Order' in attrs:
                        attrs['Attribute_Order'] = ''
                    self._colunas[attrs['Long_Id']] = attrs
                    attrs = {}

            domain = self.getDominios(attrs['Parent_Domain_Ref'])

            if  attrs['Name'].upper() == '%AttDomain'.upper():
                if  'User_Formatted_Name' in attrs and \
                                  attrs['User_Formatted_Name'].upper() != '%AttDomain'.upper():
                    attrs['Name'] = attrs['User_Formatted_Name']
                else:
                    if  domain:
                        attrs['Name'] = domain['Name']
                        attrs['User_Formatted_Name'] = domain['Name']
                    else:
                        attrs['Name'] = ''
                        attrs['User_Formatted_Name'] = ''

            if  attrs['Physical_Name'].upper() == '%ColDomain'.upper():
                if  'User_Formatted_Physical_Name' in attrs and \
                    attrs['User_Formatted_Physical_Name'].upper() != '%ColDomain'.upper():
                    attrs['Physical_Name'] = \
                                          attrs['User_Formatted_Physical_Name']
                else:
                    if  domain:
                        attrs['Physical_Name'] = domain['Physical_Name']
                        attrs['User_Formatted_Physical_Name'] = \
                                                        domain['Physical_Name']
                    else:
                        attrs['Physical_Name'] = ''
                        attrs['User_Formatted_Physical_Name'] = ''

            if  not 'Parent_Attribute_Ref' in attrs:
                attrs['Parent_Attribute_Ref'] = ''

            if  not 'Parent_Relationship_Ref' in attrs:
                attrs['Parent_Relationship_Ref'] = ''

            if  not 'Definition' in attrs:
                if  'Comment' in attrs:
                    attrs['Definition'] = attrs['Comment']
                else:
                    attrs['Definition'] = ''
                    attrs['Comment'] = ''

            if  not 'Attribute_Order' in attrs:
                attrs['Attribute_Order'] = ''

            self._colunas[attrs['Long_Id']] = attrs

    def __setEntidadeColunas__(self):

        for entidades in self._FisEntidades:

            ident   = self._FisEntidades[entidades]['Long_Id']
            nomelog = self._FisEntidades[entidades]['Name']
            nomefis = self._FisEntidades[entidades]['Physical_Name']
            order   = self._FisEntidades[entidades]['Attributes_Order_Ref']

            self._entidadeColunas[nomefis] = []

            attrs = {}

            for colunas in self._colunas:

                coluna = self._colunas[colunas]

                if  coluna['Long_Id'] == order or \
                    coluna['Dependent_Objects_Ref'] == ident:
                    attrs['nomeLogico'] = coluna['User_Formatted_Name']
                    attrs['nomeFisico'] = \
                                         coluna['User_Formatted_Physical_Name']
                    attrs['dataType'] = coluna['Physical_Data_Type']
                    attrs['ordem'] = '{:>05}'.format(coluna['Attribute_Order'])
                    attrs['definicao'] = coluna['Definition']
                    attrs['pk'] = self.isPk(nomelog, coluna['Name'])
                    attrs['fk'] = self.getFk(coluna['Parent_Attribute_Ref'])
                    attrs['null'] = True \
                                if coluna['Null_Option_Type'] == '0' else False
                    self._entidadeColunas[nomefis].append(attrs)
                    attrs = {}

    def getAttributes(self):

        return self._attributes

    def getDomains(self):

        return self._domains

    def getEntitys(self):

        return self._entitys

    def getKeyGroups(self):

        return self._keyGroups

    def getRelationShips(self):

        return self._relationShips

    def getMaxSequencia(self, cpo):

        ret = 0

        for entidades in self._FisEntidades:

            entidade = self._FisEntidades[entidades]

            try:
                seq = int(entidade['Entity.Physical.%s' % cpo])
            except:
                seq = 0

            if  seq > ret:
                ret = seq

        return ret

    def getEntityPhysical(self):

        ret = []

        for entidades in self._FisEntidades:

            entidade = self._FisEntidades[entidades]

            for k in entidade:

                if  k.startswith('Entity.Physical'):
                    x = k.split('Entity.Physical.')[1]
                    if  not ret.count(x):
                        ret.append(x)

        return ret

    def getEntidades(self, entidade=''):

        if  entidade:
            try:
                return self._LogEntidades[entidade]
            except:
                try:
                    return self._FisEntidades[entidade]
                except:
                    return {}
        else:
            ret = []
            for key in self._FisEntidades:
                ret.append(self._FisEntidades[key])
            return ret

    def getColunas(self, coluna='', parent=''):

        if  coluna:
            try:
                return self._colunas[coluna]
            except:
                return {}

        if  parent:
            ret = []
            for key in self._colunas:
                col = self._colunas[key]
                if  col['Parent_Relationship_Ref'] == parent:
                    ret.append(col)
            return ret

        ret = []

        for key in self._colunas:
            ret.append(self._colunas[key])

        return ret

    def getDominios(self, domain=''):

        if  domain:
            try:
                return self._dominios[domain]
            except:
                return {}
        else:
            ret = []
            for key in self._dominios:
                ret.append(self._dominios[key])
            return ret

    def getChaves(self, coluna='', parent=''):

        ret = []

        if  coluna:
            for key in self._chaves:
                if  key['Name'] == coluna:
                    ret.append(key)

        if  parent:
            for key in self._chaves:
                if  key['Attribute_Ref'] == parent:
                    ret.append(key)

        return ret

    def getRelacoes(self, relacao=''):

        if  relacao:
            try:
                return self._relacoes[relacao]
            except:
                return {}
        else:
            ret = []
            for key in self._relacoes:
                ret.append(self._relacoes[key])
            return ret

    def getEntidadeColunas(self, entidade):

        try:
            colunas = self._entidadeColunas[entidade]
        except:
            return []

        dic = {}

        for c in colunas:

            dic[c['ordem']] = {'nomeLogico': c['nomeLogico'], \
                               'nomeFisico': c['nomeFisico'], \
                               'dataType'  : c['dataType'], \
                               'pk'        : c['pk'], \
                               'fk'        : c['fk'], \
                               'null'      : c['null'], \
                               'definicao' : c['definicao']}

        keys = dic.keys()

        keys.sort()

        ret = [dic[key] for key in keys]

        return ret

    def isPk(self, entidade, coluna):

        ret = False

        chaves = self.getChaves(coluna=coluna)

        for chave in chaves:
            owner = chave['Owner_Path'].split('.')
            if  len(owner) > 2:
                if  owner[1] == entidade and owner[2].startswith('XPK'):
                    ret = True

        return ret

    def getFk(self, parent):

        ret = []

        chaves = self.getChaves(parent=parent)

        for chave in chaves:
            owner = chave['Owner_Path'].split('.')
            if  len(owner) > 2:
                if   owner[2].startswith('XPK') and len(chaves) > 1:
                    continue
                ent = self.getEntidades(owner[1])
                ret.append([chave['Physical_Name'], ent['Physical_Name']])

        return ret

    def formata(self, obj):

        try:
            obj = str(obj)
        except UnicodeEncodeError:
            # obj is unicode
            try:
                obj = unicode(obj).encode('unicode_escape', 'ignore')
                for x in obj:
                    if  ord(x) > 255:
                        obj.replace(x, ' ')
            except:
                return ''

        dic = {'\\xc7':'A', '\\xb5':'A', '\\xb7':'A',  '\\x84':'A',
               '\\x90':'E', '\\xd4':'E', '\\xd3':'E',
               '\\xd6':'I', '\\xde':'I', '\\xd8':'I',
               '\\xe5':'O', '\\xe0':'O', '\\x99':'O',
               '\\xe9':'U', '\\xeb':'U', '\\x9a':'U',
               '\\xc6':'a', '\\xa0':'a', '\\x85':'a',  '\\x84':'a',
               '\\xe3':'a', '\\xe1':'a', '\\xe2':'a',
               '\\x82':'e', '\\x8a':'e', '\\x89':'e',  '\\xea':'e',
               '\\xe4':'o', '\\xa2':'o', '\\x95':'o',  '\\x94':'o',
               '\\xf3':'o', '\\xf4':'o', '\\xf5':'o',
               '\\xa3':'u', '\\x97':'u', '\\x81':'u',  '\\xfa':'u',
               '\\x87':'c', '\\xe7':'c', '\\r'  :'\r', '\\n'  :'\n'}

        for k, v in dic.items():
            try:
                obj = obj.replace(k, v)
            except:
                break

        return obj.replace('<', '').replace('>', '').replace('/', '')

    def repEntidades(self):

        entidades = self.getEntidades()

        f1 = open(r'c:\\erwin\\repEntidades\\entidades.html', 'w')

        f1.write('<html>')
        f1.write('Total de Entidades: %s<br/><br/>' % len(entidades))

        f1.write('<table border="1" width="100%">')
        f1.write('<tr>')
        f1.write('<td>Nome Logico</td>')
        f1.write('<td>Nome Fisico</td>')
        f1.write('<td>Qualificador</td>')
        f1.write('</tr>')

        for entidade in entidades:

            f1.write('<tr>')

            nomeLogico   = entidade['Name']
            nomeFisico   = entidade['Physical_Name']
            qualificador = entidade['Name_Qualifier']

            f1.write('<td>%s</td>' % nomeLogico)
            f1.write('<td>%s</td>' % nomeFisico)
            f1.write('<td>%s</td>' % qualificador)
            f1.write('</tr>')

        f1.write('</table></html>')

        f1.close()

        return True

    def repColunas(self):

        colunas = self.getColunas()

        f1 = open(r'c:\\erwin\\repColunas\\colunas.html', 'w')

        f1.write('<html>')
        f1.write('Total de Colunas: %s<br/><br/>' % len(colunas))

        f1.write('<table border="1" width="100%">')
        f1.write('<tr>')
        f1.write('<td>Nome Logico</td>')
        f1.write('<td>Nome Fisico</td>')
        f1.write('<td>Data Type</td>')
        f1.write('<td>Definicao</td>')
        f1.write('</tr>')

        for coluna in colunas:

            nomeLogico = coluna['User_Formatted_Name']
            nomeFisico = coluna['User_Formatted_Physical_Name']
            dataType   = coluna['Logical_Data_Type']
            definicao  = coluna['Definition']

            f1.write('<tr>')
            f1.write('<td>%s</td>' % nomeLogico)
            f1.write('<td>%s</td>' % nomeFisico)
            f1.write('<td>%s</td>' % dataType)
            f1.write('<td>%s</td>' % definicao)
            f1.write('</tr>')

        f1.write('</table></html>')

        f1.close()

        return True

    def repEntidadeColunas(self, entidade):

        entidades = self.getEntidades(entidade)

        if  not entidades: return []

        if  isinstance(entidades, dict): entidades = [entidades]

        for entidade in entidades:

            entcols = self.getEntidadeColunas(entidade['Physical_Name'])

            arquivo = u'c:\\erwin\\repEntidadeColunas\\%s.html' % \
                                        self.formata(entidade['Physical_Name'])

            f1 = open(arquivo, 'w')

            f1.write('<html>')
            f1.write('<table border="1" width="100%">')

            pv = True

            for entcol in entcols:

                if  pv:
                    f1.write('<tr>')
                    f1.write('<td>Nome Logico</td>')
                    f1.write('<td>Nome Fisico</td>')
                    f1.write('<td>Data Type</td>')
                    f1.write('<td>PK</td>')
                    f1.write('<td>FK</td>')
                    f1.write('<td>Null</td>')
                    f1.write('<td>Definicao</td>')
                    f1.write('</tr>')
                    pv = False

                f1.write('<tr>')
                f1.write('<td>%s</td>' % self.formata(entcol['nomeLogico']))
                f1.write('<td>%s</td>' % self.formata(entcol['nomeFisico']))
                f1.write('<td>%s</td>' % self.formata(entcol['dataType']))
                f1.write('<td>%s</td>' % self.formata(entcol['pk']))
                f1.write('<td>%s</td>' % self.formata(entcol['fk']))
                f1.write('<td>%s</td>' % self.formata(entcol['null']))
                f1.write('<td>%s</td>' % self.formata(entcol['definicao']))
                f1.write('</tr>')

            f1.write('</table></html>')

            f1.close()

        return True
