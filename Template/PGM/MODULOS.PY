from utilities import *

dic = {'@ERR_LOCAL' : 'ER21'
      ,'@LABEL'     : '5100'
      ,'@MODULO'    : 'MODL1000'}

template = open(r'C:\web2py\applications\soagDes2\Template\PGM\modulo.cbl').read()
proc = change(dic, template)

dic = {'@ERR_LOCAL' : 'ER22'
      ,'@LABEL'     : '5200'
      ,'@MODULO'    : 'MODL2000'}

proc += change(dic, template)

pgm = open(r'C:\web2py\applications\soagDes2\Template\PGM\3YYY.CBL').read()
pgm = pgm.replace('@PROCS', proc)

dic = {'@APPLID'    : 'APP1'
      ,'@ERROCICS'  : 'ER99'
      ,'@PGMIDI'    : 'P01'}

pgm = change(dic, pgm)

pgm = insAster72(pgm)

pgmw = open(r'C:\web2py\applications\soagDes2\Template\PGM\3YYYW.CBL','w')

pgmw.write(pgm)

