import Sqlalchemy
sqa = Sqlalchemy.Sqlalchemy(db, cAppl=2, info=True)
resp, engine = sqa.tryEngine()

load = sqa.load(database=True)

prc = {'entitys':sqa.getEntitys()
      ,'columns':sqa.getColumns()
      ,'entitysColumns':sqa.getEntitysColumns()}

picke = os.path.join( '\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', 'soag', 'private', 'sqlalchemy.pickle')
Sqlalchemy.pic(prc,picke)


import Sqlalchemy
sqa = Sqlalchemy.Sqlalchemy(db, cAppl=3, info=True)

picke = os.path.join( '\\\\', '127.0.0.1', 'c$', 'web2py', 'applications', 'soag', 'private', 'sgdb_5.pickle')
pck=Sqlalchemy.unPic(picke)
load = sqa.load(picke=pck)
