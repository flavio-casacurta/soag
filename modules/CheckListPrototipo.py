# -*- coding:utf-8
'''
   Created on 12/09/2011
   @author: C&C - HardSoft
'''
import sys

class CheckListPrototipo:

    def __init__(self, db, cAppl=None):
        self.db        = db
        self.cAppl     = cAppl or 0
        self.checkListPrototipo = self.db.checkListPrototipo

        try:
            self.query               = self.db(self.checkListPrototipo.codigoAplicacao==cAppl).select()
            self.aplicacao           = self.query[0].aplicacao
            self.model               = self.query[0].model
            self.database            = self.query[0].database
            self.menus               = self.query[0].menus
            self.controllers         = self.query[0].controllers
            self.users               = self.query[0].users
            self.mensagens           = self.query[0].mensagens
        except:
            self.aplicacao           = False
            self.model               = False
            self.database            = False
            self.menus               = False
            self.controllers         = False
            self.users               = False
            self.mensagens           = False

    def getAplicacao(self):
        return self.aplicacao

    def getModel(self):
        return self.model

    def getDatabase(self):
        return self.database

    def getMenus(self):
        return self.menus

    def getControllers(self):
        return self.controllers

    def getUsers(self):
        return self.users

    def getMensagens(self):
        return self.mensagens
