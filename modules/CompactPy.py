# -*- coding:utf-8
'''
   Created on 29/01/2012
   @author: C&C - HardSoft
'''
import sys, os, traceback
from DirFileList import *
from zipfile     import ZipFile

class Compact:

   def __init__(self, db):
       self.db          = db
       self.parametros  = self.db.parametros
       self.parms       = self.db(self.parametros).select()[0]

   def compact(self, entity, files):
       fileZip          = '%s%s.zip' % (self.parms.log, entity)
       try:
           os.remove(fileZip)
       except:
           erro = traceback.format_exc()
       zip              = ZipFile(fileZip, mode='w')
       for lis in files:
           dirFileList  = DirFileList()
           dirFileList.setDirFileList(lis)
           fileList     = dirFileList.getDirFileList()
           for f in fileList:
               zip.write(f)
               try:
                   os.remove(f)
               except:
                   erro = traceback.format_exc()
       zip.close()
