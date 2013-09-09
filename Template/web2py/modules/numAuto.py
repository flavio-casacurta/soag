# -*- coding: utf-8 -*-
'''
   Created on 17/06/2013
   @author: C&C - HardSoft
'''
def numAuto(db, campo, where):
    query =  db(where).select(campo.max())
    qmx   = query[0]._extra[eval("'MAX({})'".format(str(campo)))]
    return qmx + 1 if qmx else 1
