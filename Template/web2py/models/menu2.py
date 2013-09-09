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

    response.dtree.menu('menu 1')                    # menu debaixo do menu 0

    response.dtree.aplicacao('menu 1', 'label 1',
                               URL(request.application, 'app 1', 'index'))

    response.dtree.menu('menu 2')                    # menu debaixo do menu 0

    response.dtree.menu('menu 3', parent = 'menu 2') # submenu porque tem parent

    response.dtree.aplicacao('menu 3', 'label 3',
                               URL(request.application, 'app 3', 'index'))


    response.menudtree = response.dtree.html()
