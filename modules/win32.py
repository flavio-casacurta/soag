# -*- coding:utf-8
'''
   Created on 22/10/2011
   @author: C&C - HardSoft
'''

import win32com.client as win32c, traceback, pdb

class Erwin(object):

    def __init__(self, arquivo):

        self.erwin         = None
        self.modelo        = None
        self.entitys       = {}
        self.attributes    = {}
        self.domains       = {}
        self.keyGroups     = {}
        self.relationShips = {}
        self.erro          = {}
        
        #pdb.set_trace()

        try:
            self.erwin = win32c.DispatchEx('Python.Erwin')
        except:
            try:
                win32c.pythoncom.CoInitialize()
                self.erwin = win32c.DispatchEx('Python.Erwin')
            except:
                msgsErrors = {}
                erros = traceback.format_exc()
                if  erros:
                    idx = 0
                    for erro in erros.split('\n'):
                        if  len(erro) > 1:
                            idx += 1
                            msgsErrors[idx] = erro
                    self.erro = {'retorno': False,
                                 'flash': 'Erro loading erwin',
                                 'labelErrors': 'Erro: Python.Erwin',
                                 'msgsErrors': msgsErrors}

        if  not self.erro:
            dispatch = eval(self.erwin.Dispatch(arquivo))
            if  dispatch['retorno']:
                self.entitys       = eval(self.erwin.getEntitys())
                self.attributes    = eval(self.erwin.getAttributes())
                self.domains       = eval(self.erwin.getDomains())
                self.keyGroups     = eval(self.erwin.getKeyGroups())
                self.relationShips = eval(self.erwin.getRelationShips())
            else:
                self.erro = dispatch
