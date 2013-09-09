jQuery(function($){
   $(".telefone").mask("(99) 9999-9999");
   $(".cpf").mask("999.999.999-99");
   $(".cnpj").mask("999.999.999/9999-99");
   $(".cep").mask("9999-9999");
   $(".data").mask("99/99/9999");
   $(".hora").mask("99:99");
});

function popupw(url,topw,leftw,heightw,widthw) {
  newwindow=window.open(url,'_blank','top='+topw+',left='+leftw+',height='+
                              heightw+',width='+widthw+',location=no,menubar=no,status=no,toolbar=no,scrollbars=yes,resizable=yes');
  if (window.focus) {
      newwindow.focus();
  }
  return false;
}

function popupr(url,topw,leftw,heightw,widthw) {
  newwindow=window.open(url,'_blank','top='+topw+',left='+leftw+',height='+
                              heightw+',width='+widthw+',location=no,menubar=no,status=no,toolbar=no,scrollbars=yes,resizable=yes');
  if (window.focus) {
      newwindow.focus();
  }
  window.opener.location.reload(true);
  return false;
}

function ajaxList(url,id) {
    jQuery.ajax({type: "POST", url: url, success: function(ret) {
        jQuery('#'+id).html(ret);
    }});
    return false;
}

function ajaxCall(m,f,c) {
    if(!confirm('Tem certeza que deseja ' + m)) {
        return false;
    }
    jQuery.ajax({type: "POST", url: f, success: function(msg) {
        if(msg != '') alert(msg);
        window.open(c,'_self');
    }});
}

function ajaxProc(sender, nome, vai, volta)
{
    jQuery("#imgProgress_"+nome).show();
    jQuery(sender).text("Processando...");
    jQuery.ajax({type: "POST", url: vai, success: function(msg) {
        jQuery("#imgProgress_"+nome).hide();
        if(msg != null && msg != 'None') alert(msg);
        window.open(volta,'_self');
    }});
}
