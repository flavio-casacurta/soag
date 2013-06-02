# -*- coding: utf-8 -*-

import win32com.client as win32, traceback, pdb

class Erwin:
    """The Erwin object exposed via COM
    """
    _public_methods_   = ['Dispatch', 'getEntitys', 'getAttributes',
                          'getDomains', 'getKeyGroups', 'getRelationShips']

    _public_attrs_     = ['versao']
    _reg_verprogid_    = "Python.Erwin.1.0"
    _reg_progid_       = "Python.Erwin"
    _reg_desc_         = "Python Erwin"
    _reg_clsid_        = "{C066C837-F820-4BC1-BA19-6C6B6708CA68}"
    # import pythoncom
    # pythoncom.CreateGuid()
    # IID('{C066C837-F820-4BC1-BA19-6C6B6708CA68}')
    _reg_class_spec_   = "win32com.servers.pythonErwin.Erwin"

    def __init__(self):
        
        # pdb.set_trace()

        try:
            self.erwin = win32.dynamic.Dispatch('AllFusionERwin.SCAPI')
        except:
            self.erwin = None

        self.entitys       = {}
        self.attributes    = {}
        self.domains       = {}
        self.keyGroups     = {}
        self.relationShips = {}

        self.versao = 1.0

    def _safe_str_(self, obj):

        try:
            obj = str(obj)
        except:
            # obj is unicode
            try:
                obj = '%s'.decode('cp1252', 'ignore').\
                                               encode('cp1252', 'ignore') % obj
                for x in obj:
                    if  ord(x) > 255:
                        obj.replace(x, ' ')
            except:
                obj = ''

        return obj

    def Dispatch(self, arquivo):

        try:
            modelo   = self.erwin.PersistenceUnits.Add(arquivo)
            sessions = self.erwin.Sessions
            session  = sessions.Add()
            session.Open(modelo)
            modelObjects = session.ModelObjects
            for modelObject in modelObjects:
                if  modelObject.ClassName.startswith('Entity'):
                    if  not self.entitys.has_key(modelObject.Name):
                        self.entitys[modelObject.Name] = []
                elif  modelObject.ClassName.startswith('Attribute'):
                    if  not self.attributes.has_key(modelObject.Name):
                        self.attributes[modelObject.Name] = []
                elif  modelObject.ClassName.startswith('Domain'):
                    if  not self.domains.has_key(modelObject.Name):
                        self.domains[modelObject.Name] = []
                elif  modelObject.ClassName.startswith('Key'):
                    if  not self.keyGroups.has_key(modelObject.Name):
                        self.keyGroups[modelObject.Name] = []
                elif  modelObject.ClassName.startswith('Relationship'):
                    if  not self.relationShips.has_key(modelObject.Name):
                        self.relationShips[modelObject.Name] = []
                else:
                    continue
                item  = modelObjects.Item(modelObject.ObjectId)
                props = item.Properties
                for idx in range(0, props.Count-1):
                    if  modelObject.ClassName.startswith('Entity'):
                        k = self._safe_str_(props[idx])
                        try:
                            v = self._safe_str_(props[idx].Value)
                        except:
                            v = ''
                        self.entitys[modelObject.Name].\
                                                     append('%s = %s' % (k, v))
                        continue
                    if  modelObject.ClassName.startswith('Attribute'):
                        k = self._safe_str_(props[idx])
                        try:
                            v = self._safe_str_(props[idx].Value)
                        except:
                            v = ''
                        self.attributes[modelObject.Name].\
                                                     append('%s = %s' % (k, v))
                        continue
                    if  modelObject.ClassName.startswith('Domain'):
                        k = self._safe_str_(props[idx])
                        try:
                            v = self._safe_str_(props[idx].Value)
                        except:
                            v = ''
                        self.domains[modelObject.Name].\
                                                     append('%s = %s' % (k, v))
                        continue
                    if  modelObject.ClassName.startswith('Key'):
                        k = self._safe_str_(props[idx])
                        try:
                            v = self._safe_str_(props[idx].Value)
                        except:
                            v = ''
                        self.keyGroups[modelObject.Name].\
                                                     append('%s = %s' % (k, v))
                        continue
                    if  modelObject.ClassName.startswith('Relationship'):
                        k = self._safe_str_(props[idx])
                        try:
                            v = self._safe_str_(props[idx].Value)
                        except:
                            v = ''
                        self.relationShips[modelObject.Name].\
                                                     append('%s = %s' % (k, v))
                        continue
            session.Close()
            return str({'retorno': True})
        except:
            msgsErrors = {}
            erros = traceback.format_exc()
            if  erros:
                idx = 0
                for erro in erros.split('\n'):
                    if  len(erro) > 1:
                        idx += 1
                        msgsErrors[idx] = erro
                return str({'retorno': False,
                            'flash': 'Erro loading erwin',
                            'labelErrors': 'Erro: Python.PersistenceUnits',
                            'msgsErrors': msgsErrors})

    def getEntitys(self):

        return str(self.entitys)

    def getAttributes(self):

        return str(self.attributes)

    def getDomains(self):

        return str(self.domains)

    def getKeyGroups(self):

        return str(self.keyGroups)

    def getRelationShips(self):

        return str(self.relationShips)

def Register():
    import win32com.server.register
    return win32com.server.register.UseCommandLine(Erwin)

if __name__=='__main__':
    print "Registering COM server..."
    Register()
