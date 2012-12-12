import cPickle as pickle

def pic(obj,fil):
    f = open(fil, 'wb')
    pickle.dump(obj, f)
    f.close

def unPic(fil):
    f = open(fil, 'rb')
    return pickle.load(f)
