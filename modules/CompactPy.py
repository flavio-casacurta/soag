# -*- coding:utf-8
'''
   Created on 29/01/2012
   @author: C&C - HardSoft
'''
import sys, os, traceback
from DirFileList import *
import zipfile
try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

class Compact:

    def __init__(self, db):
        self.db = db
        self.parametros = self.db.parametros
        self.parms = self.db(self.parametros).select()[0]

    def compact(self, entity, files):
        fileZip = os.path.join('\\\\'
                              ,'127.0.0.1'
                              ,'c$'
                              ,self.parms.log
                              ,'{}.zip'.format(entity))
        try:
            os.remove(fileZip)
        except:
            pass
        zip = zipfile.ZipFile(fileZip, mode='w')
        if  isinstance(files, str):
            files = files.split()
        for lis in files:
            dirFileList = DirFileList()
            dirFileList.setDirFileList(lis)
            fileList = dirFileList.getDirFileList()
            for file in fileList:
                arcname = os.path.basename(file)
                zip.write(file, arcname=arcname, compress_type=compression)
                try:
                    os.remove(file)
                except:
                    pass
        zip.close()
