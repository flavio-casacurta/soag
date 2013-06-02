parms = db(db.parametros.id==1).select()[0]
tmplt = os.path.join( '\\\\','127.0.0.1','c$',parms.web2py,'applications',parms.soag,'Template','PROG') + os.sep
