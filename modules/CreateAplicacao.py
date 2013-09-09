# -*- coding: utf-8 -*-

'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''

import os, sys
import traceback
import shutil
import uuid
from utils import web2py_uuid
from fileutils import up, w2p_unpack, read_file, write_file

def apath(path='', r=None):
    """
    Builds a path inside an application folder

    Parameters
    ----------
    path:
        path within the application folder
    r:
        the global request object

    """

    opath = up(r.folder)
    while path[:3] == '../':
        (opath, path) = (up(opath), path[3:])
    return os.path.join(opath, path).replace('\\', '/')

def app_create(db, app, request, force=False, key=None, info=False):
    """
    Create a copy of welcome.w2p (scaffolding) app

    Parameters
    ----------
    app:
        application name
    request:
        the global request object

    """
    path = apath(app, request)
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except:
            if info:
                return False, traceback.format_exc(sys.exc_info)
            else:
                return False, None
    elif not force:
        if info:
            return False, "Application exists"
        else:
            return False, None
    try:
        w2p_unpack('welcome.w2p', path)
        for subfolder in [
            'models', 'views', 'controllers', 'databases',
            'modules', 'cron', 'errors', 'sessions', 'cache',
            'languages', 'static', 'private', 'uploads']:
            subpath = os.path.join(path, subfolder)
            if not os.path.exists(subpath):
                os.mkdir(subpath)
        dbt = os.path.join(path, 'models', 'db.py')
        if os.path.exists(dbt):
            data = read_file(dbt)
            data = data.replace('<your secret key>',
                                'sha512:' + (key or web2py_uuid()))
            write_file(dbt, data)

        parms = db(db.parametros.id==1).select()[0]

        templates = os.path.join('\\\\'
                                , '127.0.0.1'
                                , 'c$'
                                , parms.web2py
                                , 'applications'
                                , parms.soag
                                , 'Template'
                                , 'web2py')

        for subfolder in ['controllers', 'languages', 'models', 'modules', 'static', 'views']:
            template = os.path.join(templates, subfolder)
            subpath = os.path.join(path, subfolder)
            shutil.rmtree(subpath)
            shutil.copytree(template, subpath)

#        shutil.copyfile(os.path.join(templates, 'routes.py'), os.path.join(path, 'routes.py'))

        if info:
            return True, None
        else:
            return True, None
    except:
        shutil.rmtree(path)
        if info:
            return False, traceback.format_exc(sys.exc_info)
        else:
            return False, None
