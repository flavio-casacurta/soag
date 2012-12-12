# -*- coding:utf-8
'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''
import os

class Compact:

   def __init__(self, db):
       self.db          = db
       self.parametros  = self.db.parametros
       self.parms       = self.db(self.parametros).select()[0]


   def compact(self, entity, files):
       zipFile = os.path.join( '\\\\'
                             , '127.0.0.1'
                             , 'c$'
                             , self.parms.log
                             , entity + '.zip')
       try:
           os.remove(zipFile)
       except:
           pass
       for lis in files:
           command = '7za u %s %s%s*.*' % (zipFile, lis, os.sep)
           os.system(command)
           command = 'erase /q %s%s*.*' % (lis, os.sep)
           os.system(command)
