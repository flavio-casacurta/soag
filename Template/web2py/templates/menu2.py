# -*- coding: utf-8 -*-

response.title               = T('')
response.cliente             = T('')
response.subtitle            = T('')
response.meta.author         = 'C&C - HardSoft'
response.meta.description    = 'Free and open source full-stack enterprise framework'
response.meta.keywords       = 'web2py, python, framework'
response.meta.generator      = 'Web2py Enterprise Framework'
response.meta.copyright      = 'Copyright 2007-2010'
response.menu                = []
response.dtree               = dtree()
response.etree               = []
response.wtree               = []

if  response.tipoMenu == 'dtree':

@menus
    response.menudtree = response.dtree.html()
