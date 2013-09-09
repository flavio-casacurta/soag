# -*- coding: utf-8 -*-

# -*- coding:utf-8
'''
   Created on 22/10/2011
   @author: C&C - HardSoft
'''
import win32, time
from utilities import *

dic = {'SACL':'IMAG'
      ,'Serviço de Apoio ao Cliente':'Sistema Imaginario'
      ,'Servico de Apoio ao Cliente':'Sistema Imaginario'
      ,'ServicoApoioCliente':'SistemaImaginario'
      }


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

#            self._entitys       = _erwin.entitys
            for k, v in _erwin.entitys.items():
                if  v:
                    if  isinstance(v, list):
                        nv=[]
                        for s in v:
                            nv.append(change(dic, ra(s.encode('cp1252'))))
                        v = nv
                    if  isinstance(v, str):
                        v = change(dic, ra(v.encode('cp1252')))
                self._entitys[k]=v

#            self._attributes    = _erwin.attributes
            for k, v in _erwin.attributes.items():
                if  v:
                    if  isinstance(v, list):
                        nv=[]
                        for s in v:
                            nv.append(change(dic, ra(s.encode('cp1252'))))
                        v = nv
                    if  isinstance(v, str):
                        v = change(dic, ra(v.encode('cp1252')))
                self._attributes[k]=v

#            self._domains       = _erwin.domains
            for k, v in _erwin.domains.items():
                if  v:
                    if  isinstance(v, list):
                        nv=[]
                        for s in v:
                            nv.append(change(dic, ra(s.encode('cp1252'))))
                        v = nv
                    if  isinstance(v, str):
                        v = change(dic, ra(v.encode('cp1252')))
                self._domains[k]=v

#            self._keyGroups     = _erwin.keyGroups
            for k, v in _erwin.keyGroups.items():
                if  v:
                    if  isinstance(v, list):
                        nv=[]
                        for s in v:
                            nv.append(change(dic, ra(s.encode('cp1252'))))
                        v = nv
                    if  isinstance(v, str):
                        v = change(dic, ra(v.encode('cp1252')))
                self._keyGroups[k]=v

#            self._relationShips = _erwin.relationShips
            for k, v in _erwin.relationShips.items():
                if  v:
                    if  isinstance(v, list):
                        nv=[]
                        for s in v:
                            nv.append(change(dic, ra(s.encode('cp1252'))))
                        v = nv
                    if  isinstance(v, str):
                        v = change(dic, ra(v.encode('cp1252')))
                self._relationShips[k]=v

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

            nomelog = self._FisEntidades[entidades]['Name']

            try:
                nomefis = self._FisEntidades[entidades]['Physical_Name']
            except:
                nomefis = \
                  self._FisEntidades[entidades]['User_Formatted_Physical_Name']

            ident = (self._FisEntidades[entidades]['Long_Id'] if 'Long_Id' in
                                         self._FisEntidades[entidades] else '')

            child = (self._FisEntidades[entidades]['Child_Relationships_Ref']
                                                if 'Child_Relationships_Ref' in
                                         self._FisEntidades[entidades] else '')

            order = (self._FisEntidades[entidades]['Attributes_Order_Ref']
                                               if 'Attributes_Order_Ref' in
                                         self._FisEntidades[entidades] else '')

            parent = (self._FisEntidades[entidades]['Parent_Relationships_Ref']
                                               if 'Parent_Relationships_Ref' in
                                         self._FisEntidades[entidades] else '')


            self._entidadeColunas[nomefis] = []

            for colunas in self._colunas:

                attrs = {}

                coluna = self._colunas[colunas]

                if  ident and 'Dependent_Objects_Ref' in coluna and \
                                      coluna['Dependent_Objects_Ref'] == ident:
                    attrs['nomeLogico'] = coluna['User_Formatted_Name']

                    if  ('Physical_Name' in coluna.keys() and
                         coluna['Physical_Name'].upper() != '%DOMAINNAME'):
                        attrs['nomeFisico'] = coluna['Physical_Name']
                    else:
                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

#                    try:
#                        attrs['nomeFisico'] = coluna['Physical_Name']
#                    except:
#                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

                    if  self.__existe__(self._entidadeColunas[nomefis], attrs['nomeFisico']):
                        continue
                    attrs['dataType'] = coluna['Physical_Data_Type']
                    if  'Column_Order' in coluna:
                        attrs['ordem'] = '{:>05}'.format(coluna['Column_Order'])
                    else:
                        attrs['ordem'] = '{:>05}'.format(coluna['Attribute_Order'])
                    attrs['definicao'] = coluna['Definition']
                    attrs['pk'] = self.isPk(nomelog, coluna['Name'])
                    attrs['fk'] = self.getFk(coluna['Parent_Attribute_Ref'])
                    attrs['null'] = True \
                                if coluna['Null_Option_Type'] == '0' else False
                    self._entidadeColunas[nomefis].append(attrs)

                elif child and 'Parent_Relationship_Ref' in coluna and \
                                    coluna['Parent_Relationship_Ref'] == child:
                    attrs['nomeLogico'] = coluna['User_Formatted_Name']

                    if  ('Physical_Name' in coluna.keys() and
                         coluna['Physical_Name'].upper() != '%DOMAINNAME'):
                        attrs['nomeFisico'] = coluna['Physical_Name']
                    else:
                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

#                    try:
#                        attrs['nomeFisico'] = coluna['Physical_Name']
#                    except:
#                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

                    if  self.__existe__(self._entidadeColunas[nomefis], attrs['nomeFisico']):
                        continue
                    attrs['dataType'] = coluna['Physical_Data_Type']
                    if  'Column_Order' in coluna:
                        attrs['ordem'] = '{:>05}'.format(coluna['Column_Order'])
                    else:
                        attrs['ordem'] = '{:>05}'.format(coluna['Attribute_Order'])
                    attrs['definicao'] = coluna['Definition']
                    attrs['pk'] = self.isPk(nomelog, coluna['Name'])
                    attrs['fk'] = self.getFk(coluna['Parent_Attribute_Ref'])
                    attrs['null'] = True \
                                if coluna['Null_Option_Type'] == '0' else False
                    self._entidadeColunas[nomefis].append(attrs)

                elif order and 'Long_Id' in coluna and coluna['Long_Id'] == order:
                    attrs['nomeLogico'] = coluna['User_Formatted_Name']

                    if  ('Physical_Name' in coluna.keys() and
                         coluna['Physical_Name'].upper() != '%DOMAINNAME'):
                        attrs['nomeFisico'] = coluna['Physical_Name']
                    else:
                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

#                    try:
#                        attrs['nomeFisico'] = coluna['Physical_Name']
#                    except:
#                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

                    if  self.__existe__(self._entidadeColunas[nomefis], attrs['nomeFisico']):
                        continue
                    attrs['dataType'] = coluna['Physical_Data_Type']
                    if  'Column_Order' in coluna:
                        attrs['ordem'] = '{:>05}'.format(coluna['Column_Order'])
                    else:
                        attrs['ordem'] = '{:>05}'.format(coluna['Attribute_Order'])
                    attrs['definicao'] = coluna['Definition']
                    attrs['pk'] = self.isPk(nomelog, coluna['Name'])
                    attrs['fk'] = self.getFk(coluna['Parent_Attribute_Ref'])
                    attrs['null'] = True \
                                if coluna['Null_Option_Type'] == '0' else False
                    self._entidadeColunas[nomefis].append(attrs)


            for colunas in self._colunas:

                attrs = {}

                coluna = self._colunas[colunas]
                if  parent and 'Parent_Relationship_Ref' in coluna and \
                                   coluna['Parent_Relationship_Ref'] == parent:

                    attrs['nomeLogico'] = coluna['User_Formatted_Name']

                    if  ('Physical_Name' in coluna.keys() and
                         coluna['Physical_Name'].upper() != '%DOMAINNAME'):
                        attrs['nomeFisico'] = coluna['Physical_Name']
                    else:
                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

#                    try:
#                        attrs['nomeFisico'] = coluna['Physical_Name']
#                    except:
#                        attrs['nomeFisico'] = coluna['User_Formatted_Physical_Name']

                    if  self.__existe__(self._entidadeColunas[nomefis], attrs['nomeFisico']):
                        continue
                    attrs['dataType'] = coluna['Physical_Data_Type']
                    if  'Column_Order' in coluna:
                        attrs['ordem'] = '{:>05}'.format(coluna['Column_Order'])
                    else:
                        attrs['ordem'] = '{:>05}'.format(coluna['Attribute_Order'])
                    if  self.__ordem__(self._entidadeColunas[nomefis], attrs['ordem']):
                        continue
                    attrs['definicao'] = coluna['Definition']
                    attrs['pk'] = self.isPk(nomelog, coluna['Name'])
                    attrs['fk'] = self.getFk(coluna['Parent_Attribute_Ref'])
                    attrs['null'] = True \
                                if coluna['Null_Option_Type'] == '0' else False
                    self._entidadeColunas[nomefis].append(attrs)


    def __existe__(self, colunas, coluna):

        ret = False

        for col in colunas:
            if  col['nomeFisico'] == coluna:
                ret = True
                break

        return ret

    def __ordem__(self, colunas, ordem):

        ret = False

        for col in colunas:
            if  col['ordem'] == ordem:
                ret = True
                break

        return ret

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

            dic[c['ordem']] = {'nomeLogico': c['nomeLogico'],
                               'nomeFisico': c['nomeFisico'],
                               'dataType'  : c['dataType'],
                               'pk'        : c['pk'],
                               'fk'        : c['fk'],
                               'null'      : c['null'],
                               'definicao' : c['definicao']}

        ret = [dic[key] for key in sorted(dic.keys())]

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
                if  not  ent:
                    continue
                ret.append([chave['Physical_Name'], ent['Physical_Name']])

        return ret
