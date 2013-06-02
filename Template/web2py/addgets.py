# coding: utf8

from gluon.html import INPUT, TEXTAREA, XML, URL

class addgets():

    def telefone(self, field, value):
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="telefone",
                     _value=value,
                     requires=field.requires)

    def cpf(self, field, value):
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="cpf",
                     _value=value,
                     requires=field.requires)

    def cnpj(self, field, value):
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="cnpj",
                     _value=value,
                     requires=field.requires)

    def cep(self, field, value):
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="cep",
                     _value=value,
                     requires=field.requires)

    def data(self, field, value):
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="data",
                     _value=value,
                     requires=field.requires)

    def hora(self, field, value):
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="hora",
                     _value=value,
                     requires=field.requires)

    def textarea(self, field, value):
        try:
            rows = field.rows
        except:
            rows = '20'
        try:
            cols = field.cols
        except:
            cols = '45'
        try:
            width = field.width
        except:
            width = '95%'
        try:
            height = field.height
        except:
            height = '110px'
        try:
            disabled = field.disabled
        except:
            disabled = False
        return TEXTAREA(_name=field.name,
                        _id="%s_%s" % (field._tablename, field.name),
                        _class="text",
                         value=value,
                        _rows=rows,
                        _cols=cols,
                        _style="width:%s;height:%s" % (width, height),
                        _disabled=disabled,
                        requires=field.requires)

    def text(self, field, value):
        try:
            width = field.width
        except:
            width = '89%'
        try:
            uppercase = field.uppercase
        except:
            uppercase = False
        try:
            mascara = field.mascara
        except:
            mascara = None
        try:
            maxlength = field.maxlength
        except:
            maxlength = 100
        try:
            readonly = field.readonly
        except:
            readonly = False
        try:
            disabled = field.disabled
        except:
            disabled = False
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="string",
                     _type="text",
                     _maxlength=maxlength,
                     _value=value.upper() \
                            if value and uppercase else value if value else '',
                     _style="width:%s" % (width),
                     _onkeypress=XML("mascara(this, '" + mascara + "')") \
                                                            if mascara else "",
                     _disabled=disabled,
                     _readonly=readonly,
                     requires=field.requires)

    def uploadswf(self, field, value, download_url=None):
        try:
            parm     = field.parm
        except:
            parm     = 0
        try:
            uploader = field.uploader
        except:
            uploader = URL(('uploader/%s' % parm) if parm else 'uploader')
        ret  = '<div class="fieldset flashswf" id="fsUploadProgress">'
        ret += '<span class="legend">Uploads</span>'
        ret += '</div>'
        ret += '<div id="divStatus" style="margin-left: 2px; font-size: 9pt; '
        ret += 'height: 19px;">0 Uploads</div>'
        ret += '<div style="padding-left: 3px;">'
        ret += '<span id="spanButtonPlaceHolder"></span>'
        ret += '<input id="btnCancel" type="button" value="Cancela Uploads"'
        ret += ' onclick="swfu.cancelQueue();" disabled="disabled" style="marg'
        ret += 'in-left: 2px; font-size: 8pt; height: 23px;" />'
        ret += '</div>'
        ret += '<script type="text/javascript">'
        ret += 'var swfu;'
        ret += 'window.onload = function() {'
        ret += 'var settings = {'
        ret += 'flash_url : "%s",' % URL('static', 'images/swfupload.swf')
        ret += 'upload_url: "%s",' % uploader
        ret += 'file_size_limit : "100 MB",'
        ret += 'file_types : "*.*",'
        ret += 'file_types_description : "Todos Arquivos",'
        ret += 'file_upload_limit : 100,'
        ret += 'file_queue_limit : 0,'
        ret += 'custom_settings : {'
        ret += 'progressTarget : "fsUploadProgress",'
        ret += 'cancelButtonId : "btnCancel"'
        ret += '},'
        ret == 'debug: false,'
        ret += 'button_image_url: "%s",' % URL('static', 'images/swf.png')
        ret += 'button_width: 61,'
        ret += 'button_height: 22,'
        ret += 'button_placeholder_id: "spanButtonPlaceHolder",'
        ret += 'file_queued_handler : fileQueued,'
        ret += 'file_queue_error_handler : fileQueueError,'
        ret += 'file_dialog_complete_handler : fileDialogComplete,'
        ret += 'upload_start_handler : uploadStart,'
        ret += 'upload_progress_handler : uploadProgress,'
        ret += 'upload_error_handler : uploadError,'
        ret += 'upload_success_handler : uploadSuccess,'
        ret += 'upload_complete_handler : uploadComplete,'
        ret += 'queue_complete_handler : '
        ret += 'function queueComplete(numFilesUploaded) {'
        ret += 'var status = document.getElementById("divStatus");'
        ret += 'status.innerHTML = numFilesUploaded + " file" + (numFilesUploa'
        ret += 'ded === 1 ? "" : "s") + " uploaded.";'
        ret += 'window.location="%s";' % URL('index')
        ret += '}'
        ret += '};'
        ret += 'swfu = new SWFUpload(settings);'
        ret += '};'
        ret += ('</script>')
        return ret

    def upload(self, field, value, download_url=None):
        try:
            width = field.width
        except:
            width = '95%'
        try:
            campo = field.campo
        except:
            campo = None
        return INPUT(_name=field.name,
                     _id="%s_%s" % (field._tablename, field.name),
                     _class="upload",
                     _type="file",
                     _style="width:%s" % width,
                     _onchange=\
                     XML("cpo=document.forms[0].%s.value;" % field.name     + \
                         "cpo=cpo.split('.')[0];"                           + \
                         "if(cpo.search('fakepath')>-1)cpo=cpo.substr(12);" + \
                         "document.forms[0].%s.value=cpo;" % campo),
                     requires=field.requires)

    def timestamp(self, field, value):
        if  value:
            value = str(value)
            ret = "%s/%s/%s - %s" % (value[8:10], value[5:7], value[0:4], \
                                                          value[11:len(value)])
        else:
            ret = ""
        return ret

    def datafmt(self, field, value):
        if  value:
            return "%s/%s/%s" % (value[8:10], value[5:7], value[0:4])
        else:
            return ""

    def horafmt(self, field, value):
        if  value:
            return "%s" % value[11:len(value)]
        else:
            return ""

    def select(self, field, value):
        try:
            options = field.options
        except:
            options = []
        try:
            defaultOptions = field.defaultOptions
        except:
            defaultOptions = []
        try:
            disabled = field.disabled
        except:
            disabled = False
        ret = 'SELECT('
        idx = 0
        for option in options:
            ret += (',' if idx else '') + "'" + option + "'"
            idx += 1
        if  value:
            ret += (',' if ret <> 'SELECT(' else '') + "value='" + value + "'"
        else:
            if  defaultOptions:
                ret += (',' if ret <> 'SELECT(' else '') + "value='" + \
                                                           defaultOptions + "'"
            else:
                if  options:
                    ret += (',' if ret <> 'SELECT(' else '') + "value='" + \
                                                               options[0] + "'"
        ret += (',' if options else '') + "_name='" + field.name + \
                              "',_id='%s_%s',_disabled=%s)" % \
                                       (field._tablename, field.name, disabled)
        return eval(ret)

    def selectdb(self, field, value):
        try:
            lookup = field.lookup
        except:
            lookup = []
        if  not lookup:
            return ''
        try:
            where   = field.where
        except:
            where   = []
        if  not where:
            where   = [lookup[0][lookup[1]].id>0,'id','id']
        elif  len(where) == 1:
              where = [where[0], 'id', 'id']
        elif  len(where) == 2:
              where = [where[0], where[1], 'id']
        try:
            filtros = field.filtro
        except:
            filtros = []
        try:
            joins   = field.join
        except:
            joins   = []
        try:
            lkpwheres  = lookup[0](where[0]).select()
            lkplookups = lookup[0](lookup[0][lookup[1]]).select()
        except:
            try:
                lkpwheres  = lookup[0](lookup[0][lookup[1]]).select()
                lkplookups = lkpwheres
            except:
                return 'Erro selectdb (1)'
        try:
            submit    = field.submit
        except:
            submit    = False
        try:
            distinct  = field.distinct
        except:
            distinct  = False
        try:
            width     = field.width
        except:
            width     = ''
        try:
            selecione = field.selecione
        except:
            selecione = True
        if  selecione:
            options = [[0, '-- Selecione --']]
        else:
            options = []
        for lkpwhere in lkpwheres:
            append = False
            for lkplookup in lkplookups:
                append = False
                if  lkpwhere[where[1]] == lkplookup[where[2]]:
                    append = True
                    for filtro in filtros:
                        if  len(filtro) > 3:
                            try:
                                if  not eval("lkpwhere['%s'] %s %s %s" % \
                                                (filtro[0], filtro[3], \
                                                        filtro[1], filtro[2])):
                                    append = False
                                    break
                            except:
                                try:
                                    if  not eval("lkpwhere[%s] %s %s %s" % \
                                                    (filtro[0], filtro[3], \
                                                        filtro[1], filtro[2])):
                                        append = False
                                        break
                                except:
                                    return 'Erro selectdb (2)'
                        else:
                            try:
                                if  not eval("lkpwhere['%s'] %s %s" % \
                                            (filtro[0], filtro[1], filtro[2])):
                                    append = False
                                    break
                            except:
                                try:
                                    if  not eval("lkpwhere[%s] %s %s" % \
                                            (filtro[0], filtro[1], filtro[2])):
                                        append = False
                                        break
                                except:
                                    return 'Erro selectdb (3)'
                    for join in joins:
                        try:
                            joindb = lookup[0](lookup[0][join[0]].id==\
                                                    lkpwhere[join[1]]).select()
                        except:
                            append = False
                            break
                        if  not joindb:
                            break
                        for join2 in join[2]:
                            if  not joindb[0][join2[0]] == join2[1]:
                                append = False
                                break
                    break
            if  append:
                options.append([lkpwhere[where[1]], lkplookup[lookup[2]]])
        if  submit:
            ret = "<select name='%s' id='%s_%s' %s onChange=\"%s\">" % \
                                               (field.name, field._tablename, \
                    field.name, 'style=\'width: %s\'' % width \
                        if width else '', \
                        XML("jQuery('#action').attr('value','submit');"    + \
                            "jQuery(document.forms).each(function(){this." + \
                            "submit();});"))
        else:
            ret = "<select name='%s' id='%s_%s' %s>" % (field.name, \
                    field._tablename, field.name, \
                    'style=\'width: %s\'' % width if width else '')
        option1 = ''
        for option in options:
            if  distinct:
                if  option[1] <> option1:
                    option1 = option[1]
                    if  int(option[0]) == int(value or 0):
                        ret += "<option value='%s' selected='selected'>%s" % \
                                    (option[0], option[1]) + "</option>"
                    else:
                        ret += "<option value='%s'>%s</option>" % \
                                    (option[0], option[1])
            else:
                if  int(option[0]) == int(value or 0):
                    ret += "<option value='%s' selected='selected'>%s" % \
                                    (option[0], option[1]) + "</option>"
                else:
                    ret += "<option value='%s'>%s</option>" % \
                                    (option[0], option[1])
        ret += '</select>'
        return XML(ret)

addgets = addgets()