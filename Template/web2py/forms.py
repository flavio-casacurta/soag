from gluon.html import XML

class forms():

    def CheckDelete(self):
        ret  = '<tr id="delete_record__row">\r\n'
        ret += '    <td align="RIGHT">\r\n'
        ret += '        <label id="delete_record__label" for="delete_record">Deleta?:</label>\r\n'
        ret += '    </td>\r\n'
        ret += '    <td>\r\n'
        ret += '        <input type="checkbox" id="delete_record" class="delete" name="delete_this_record" />\r\n'
        ret += '    </td>\r\n'
        ret += '</tr>\r\n'
        return XML(ret)
