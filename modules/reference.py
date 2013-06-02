from Entidades import Entidades
entidades = Entidades(db, cAppl=1)
retEntidade = entidades.selectEntidadesBycodigoAplicacao()
entidades = retEntidade[1]

from ForeignKeys import ForeignKeys
foreignKeys = ForeignKeys(db)

lisWrite = []
dicRefer = {}

for entidade in entidades:
    dicForeignKeys = foreignKeys.selectForeignKeysByCodigoEntidade(entidade.id)
    dicRefer[entidade.id]=list(set([dicForeignKeys[k][0] for k in dicForeignKeys]))

while len(dicRefer) > 0:
    lisKeys = sorted(dicRefer.keys())
    for k in lisKeys:
        if  not dicRefer[k]:
            lisWrite.append(k)
            del dicRefer[k]
    remove = 0
    for ent in lisWrite:
        for k in dicRefer.keys():
            if  ent in dicRefer[k]:
                dicRefer[k].remove(ent)
                remove = 1
    if  not remove:
        for ent in dicRefer.keys():
            if  ent in dicRefer[ent]:
                    dicRefer[ent].remove(ent)

