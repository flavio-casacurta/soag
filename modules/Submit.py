# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import os
from Aplicacao import *
from Empresa   import *
from EditV     import *

class Submit:

   def __init__(self, db, log, cAppl=None, userName=None):
       self.db            = db
       self.log           = log
       self.cAppl         = cAppl or 0
       self.aplicacao     = Aplicacao(self.db, self.cAppl)
       self.applId        = self.aplicacao.getApplId()
       self.applName      = self.aplicacao.getApplName()
       self.contratante   = self.aplicacao.getContratante()
       self.grupo         = self.aplicacao.getGrupo()
       self.analista      = self.aplicacao.getAnalista()
       glog               = self.aplicacao.getGlog()
       self.parametros    = self.db.parametros
       self.parms         = self.db(self.parametros).select()[0]
       if glog:
           self.glog = '1'
       else:
           self.glog = '0'
       self.empresa       = Empresa(self.db, self.aplicacao.getEmpresaId()).getNome()
       self.userName      = userName or 'SOAG USER ADMIN'

   def submit(self, properties):
       dic                = {}
       dic['cAppl']       = str(self.cAppl)
       dic['log_error']   = self.log
       dic['empresa']     = self.empresa
       dic['applId']      = self.applId
       dic['applName']    = self.aplicacao.getApplName()
       dic['author']      = self.userName
       dic['contratante'] = self.contratante
       dic['grupo']       = self.grupo
       dic['analista']    = self.analista
       dic['glog']        = self.glog
       dic['ERROCICS']    = self.applId + '9999'
       dic['ERRODB2']     = self.applId + '9999'
       dic['ERROMOD']     = self.applId + '9999'
       dic['ERROLIV']     = self.applId + '9999'
       dic['soag']        = self.parms.soag
       editV(self.db, dic)
       command   = 'KEDITW32 %s(profile soag framesize min' % properties
       os.system(command)
