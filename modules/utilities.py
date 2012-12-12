# -*- coding: utf-8 -*-

'''
   Created on 07/09/2011
   @author: C&C - HardSoft
'''

from   gluon.html import XML, A, URL
from   gluon      import current
import re
import unicodedata
import os
import platform
import traceback
import base64
import uuid

def web2py_uuid():
    return str(uuid.uuid4())

def change(dic, obj):
    if isinstance(obj, list):
        for n, i in enumerate(obj):
            for k, v in dic.items():
                obj[n] = i.replace(k, v)
                i = obj[n]
    else:
        if isinstance(obj, str):
            for k, v in dic.items():
                obj = obj.replace(k, v)
    return obj

dra = {'\xc3\x80':'À', '\xc3\x81':'Á', '\xc3\x82':'Â', '\xc3\x83':'Ã',
       '\xc3\x84':'Ä', '\xc3\x85':'Å', '\xc3\x86':'Æ', '\xc3\x87':'Ç',
       '\xc3\x88':'È', '\xc3\x89':'É', '\xc3\x8a':'Ê', '\xc3\x8b':'Ë',
       '\xc3\x8c':'Ì', '\xc3\x8d':'Í', '\xc3\x8e':'Î', '\xc3\x8f':'Ï',
       '\xc3\x90':'Ð', '\xc3\x91':'Ñ', '\xc3\x92':'Ò', '\xc3\x93':'Ó',
       '\xc3\x94':'Ô', '\xc3\x95':'Õ', '\xc3\x96':'Ö', '\xc3\x98':'Ø',
       '\xc3\x99':'Ù', '\xc3\x9a':'Ú', '\xc3\x9b':'Û', '\xc3\x9c':'Ü',
       '\xc3\x9d':'Ý', '\xc3\x9e':'Þ', '\xc3\x9f':'ß', '\xc3\xa0':'à',
       '\xc3\xa1':'á', '\xc3\xa2':'â', '\xc3\xa3':'ã', '\xc3\xa4':'ä',
       '\xc3\xa5':'å', '\xc3\xa6':'æ', '\xc3\xa7':'ç', '\xc3\xa8':'è',
       '\xc3\xa9':'é', '\xc3\xaa':'ê', '\xc3\xab':'ë', '\xc3\xac':'ì',
       '\xc3\xad':'í', '\xc3\xae':'î', '\xc3\xaf':'ï', '\xc3\xb0':'ð',
       '\xc3\xb1':'ñ', '\xc3\xb2':'ò', '\xc3\xb3':'ó', '\xc3\xb4':'ô',
       '\xc3\xb5':'õ', '\xc3\xb6':'ö', '\xc3\xb8':'ø', '\xc3\xb9':'ù',
       '\xc3\xba':'ú', '\xc3\xbb':'û', '\xc3\xbc':'ü', '\xc3\xbd':'ý',
       '\xc3\xbe':'þ', '\xc3\xbf':'ÿ'}

def nUni2Uni(txt):
    return change(dra, txt)

#def remover_acentos(txt, codif='latin-1'):
def remover_acentos(txt, codif='cp1252'):

    for k in dra.keys():
        if  k in txt:
            codif='utf-8'
            break

    return unicodedata.normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore')

def safe_str(obj):
    try:
        obj = str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        try:
            obj = unicode(obj).encode('unicode_escape', 'ignore')
            for x in obj:
                if  ord(x) > 255:
                    obj.replace(x, ' ')
        except:
            return ''
    dic = {'\\xc7':'A', '\\xb5':'A', '\\xb7':'A',  '\\x84':'A',
           '\\x90':'E', '\\xd4':'E', '\\xd3':'E',
           '\\xd6':'I', '\\xde':'I', '\\xd8':'I',
           '\\xe5':'O', '\\xe0':'O', '\\x99':'O',
           '\\xe9':'U', '\\xeb':'U', '\\x9a':'U',
           '\\xc6':'a', '\\xa0':'a', '\\x85':'a',  '\\x84':'a',
           '\\xe3':'a', '\\xe1':'a',
           '\\x82':'e', '\\x8a':'e', '\\x89':'e',  '\\xea':'e',
           '\\xe4':'o', '\\xa2':'o', '\\x95':'o',  '\\x94':'o',
           '\\xf3':'o', '\\xf4':'o', '\\xf5':'o',
           '\\xa3':'u', '\\x97':'u', '\\x81':'u',  '\\xfa':'u',
           '\\x87':'c', '\\xe7':'c', '\\r'  :'\r', '\\n'  :'\n'}
    for k, v in dic.items():
        try:
            obj = obj.replace(k, v)
        except:
            break
    return obj

def safe_string(obj):

    try:
        obj = str(obj)
    except:
        # obj is unicode
        try:
            obj = '%s'.decode('cp1252', 'ignore').\
                                               encode('cp1252', 'ignore') % obj
            for x in obj:
                if  ord(x) > 128:
                    obj.replace(x, ' ')
        except:
            obj = ''

    return obj

wordsRe = re.compile(r'\w+', re.UNICODE)

def words(args):
    return wordsRe.findall(args)

def word(texto, idx):
    return words(texto)[idx]

def txtAbrev(txt, lgt):
    txt=remover_acentos(txt)
    for w in words(txt):
        if len(txt) <= lgt:
            break
        if w+' '  in txt:
            txt=txt.replace(w+' ',w[0:3]+'.')
        else:
            txt=txt.replace(w,w[0:3]+'.')
    return txt[0:lgt]

def insAster72(txt):
    ts=''
    tl=txt.split('\n')
    for l in tl:
         if l[6:7] == '*':
             if len(l) < 72:
                 l+=(' '*(71-len(l))+'*')
         ts+=l+'\n'
    return ts

def Capitalize(string, N=2):

    if  not string:
        return ''

    words  = string.split()
    result = words[0].capitalize() if words else ''

    if  words: del(words[0])

    for word in words:
        if len(word) > N:
            if word[1] == "'":
                result += ' ' + word[:2].lower() + word[2:].capitalize()
            else:
                result += ' ' + word.capitalize()
        else:
            result += ' ' + word

    return result

def Select(db, name=None, table=None, fields=[], prefix=None, \
               todos='', lookups={}, masks=[], filtro='',     \
               distinct=False, orderby='', value=0, width='', \
               submit=True):

    if  not db or not name or not table or not fields: return ''

    if  not filtro:
        rows = db(db[table]).select(orderby=fields[1] \
                                    if not orderby else orderby)
    else:
        rows = db(filtro).select(orderby=fields[1] \
                                    if not orderby else orderby)

    options = [[0, '-- Selecione --']]

    if  todos:
        options.append([999999, all])

    for row in rows:
        if  masks:
            if  not masks[0]:
                expr0 = row[fields[0]]
            else:
                expr0 = eval("'(%s) %s' % (row['" + masks[0][0] + \
                                         "'], row['" + masks[0][1] + "'])")
            if  not masks[1]:
                expr1 = row[fields[1]]
            else:
                expr1 = eval("'(%s) %s' % (row['" + masks[1][0] + \
                                         "'], row['" + masks[1][1] + "'])")
        else:
            expr0 = row[fields[0]]
            expr1 = row[fields[1]]
        if  lookups:
            if  lookups.has_key(fields[1]):
                expr1 = db(db[lookups[fields[1]][0]].id==expr1).\
                                         select()[0][lookups[fields[1]][1]]
        options.append([expr0, expr1])

    if  submit:
        ret = "<select name='%s' id='%s_%s' %s onChange=\"%s\">" % \
                      (name, (prefix if prefix else table), name,
              'style=\'width: %s\'' % width if width else '', \
                      XML("jQuery('#action').attr('value','submit');" + \
                          "jQuery(document.forms).each(function()"    + \
                          "{this.submit();});"))
    else:
        ret = "<select name='%s' id='%s_%s' %s>" % \
                    (name, (prefix if prefix else table), name, \
                            'style=\'width: %s\'' % width if width else '')

    antx  = ''

    for option in options:
        if  distinct:
            if  option[1] <> antx:
                antx = option[1]
                if  int(option[0]) == int(value):
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])
        else:
            if  int(option[0]) == int(value):
                ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                ret += "</option>"
            else:
                ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])

    ret += '</select>'

    return ret

def SelectString(name='', options=[], default='', width='', submit=False):

    if  not name or not options:
        return ''

    if  submit:
        ret = "<select name='%s' id='%s' %s onChange=\"%s\">" % \
                    (name, name, 'style=\'width: %s\'' % width  \
                        if width else '', \
                            XML("jQuery('#action').attr('value',"   + \
                                "'submit');jQuery(document.forms)." + \
                                "each(function(){this.submit();});"))
    else:
        ret = "<select name='%s' id='%s' %s>" % \
               (name, name, 'style=\'width: %s\'' % width if width else '')

    for option in options:

        if  isinstance(option, list):
            if  isinstance(option[0], int):
                if  int(option[0]) == int(default):
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])
            else:
                if  option[0] == default:
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                     (option[0], option[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                     (option[0], option[1])
        else:
            opt = [option, option]
            if  isinstance(opt[0], int):
                if  int(opt[0]) == int(default):
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                           (opt[0], opt[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                           (opt[0], opt[1])
            else:
                if  opt[0] == default:
                    ret += "<option value='%s' selected='selected'>%s" % \
                                                           (opt[0], opt[1])
                    ret += "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                                           (opt[0], opt[1])

    ret += '</select>'

    return ret

def buttons(executes):

    ret = ''

    for execute in executes:

        if  len(execute) == 2:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button',_href=URL(execute[1])))

        if  len(execute) == 3:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+'\',\'290\',\'280\',\'650\');')))

        if  len(execute) == 4:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+ '\',\''+execute[3]+\
                            '\',\'280\',\'650\');')))

        if  len(execute) == 5:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+ '\',\''+execute[3]+'\',\''+execute[4]+\
                            '\',\'650\');')))
        if  len(execute) == 6:
            ret += ('&nbsp;' if ret else '') + \
                str(A(current.T(execute[0]),_class='button', \
                    _onclick=XML('popupw(\'' +URL(execute[1])+'\',\''+\
                        execute[2]+'\',\''+execute[3]+'\',\''+execute[4]+\
                            '\',\''+execute[5]+'\');')))

    return ret

def System(obj, parms):

    try:
        os.system('%s %s' % (obj, parms))
    except:
        return traceback.format_exc()

def repeat(char=' ', times=0):

    ret = ''

    for idx in xrange(0, times):
        ret += char

    return ret

def copyFile(argv1, argv2):

    try:

        with open(argv2, 'w') as f1:

            with open(argv1)  as f2:

                for line in f2:
                    f1.write(line)

        return [True, []]

    except:
        return [False, traceback.format_exc()]

def stringList(string, fatia, header):

    ret = ''

    while string:

        if (string[fatia:fatia+1] == ',' or string[fatia-1:fatia]) and \
           (string[fatia:fatia+1] <> ' '):
            idx = fatia
            tmp = ''
            while idx > 0 and string[idx-1:idx] <> ' ' and \
                  string[idx-1:idx] <> ',':
                  tmp  = string[idx-1:idx] + tmp
                  idx -= 1
            linha    = (header if ret else '') + string[0:idx]
            string   = string[idx:]
        else:
            linha  = (header if ret else '') + string[0:fatia]
            string   = string[fatia:]

        ret += ('\n' if ret else '') + linha

    return ret

def buttonsAjax(buttons):

    ret = ''

    if  buttons:
        for button in buttons:
            ret += ('&nbsp;&nbsp;&nbsp;' if not ret else '&nbsp;') + \
                        str(A(current.T(button[0]),_class='button',_onClick=\
                            XML("ajaxCall('%s','%s','%s');" % \
                                (button[1], button[2], button[3]))))

    return ret

def buttonsDownload(buttons):

    ret = ''

    if  buttons:
        for button in buttons:
            ret += (('&nbsp;&nbsp;&nbsp;' if not ret else '&nbsp;') +
                        str(A(button[0],_class='button',_href=URL(button[1]))))

    return ret

def CryptFileName(tabela, campo, arquivo):

    filename         = os.path.basename(arquivo.replace('/', os.sep).\
                                                         replace('\\', os.sep))
    m                = re.compile('\.(?P<e>\w{1,5})$').search(filename)
    extension        = m and m.group('e') or 'txt'
    uuid_key         = web2py_uuid().replace('-', '')[-16:]
    encoded_filename = base64.b16encode(filename).lower()
    newfilename      = '%s.%s.%s.%s' % \
                                    (tabela, campo, uuid_key, encoded_filename)
    newfilename      = newfilename[:(511 - len(extension))] + '.' + extension
    return newfilename
