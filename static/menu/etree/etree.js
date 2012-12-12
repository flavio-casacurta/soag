c=0
du="";

function setCookie(c_name,value){
  //alert('Name: ' + c_name + ' - Value: ' + value);
  document.cookie=c_name+'='+value+'; path=/';
}
function getCookie(c_name){
  var re=new RegExp(c_name+'=[^;]+','i');
  if (document.cookie.match(re)){
      //alert('Name: ' + c_name + ' - Value: ' + document.cookie.match(re)[0].split('=')[1]);
      return document.cookie.match(re)[0].split('=')[1];
  }
  //alert('Name: ' + c_name + ' - Value: ""');
  return '';
}
function escondediv(dv,n){
   setCookie('etree_item',dv);
   setCookie('etree_qtde',n);
   for(i=1;i<=n;i++){           
       if(i==dv ){
           if(du!=dv){
              document.getElementById('mdiv'+i).style.display="inline"
              du=dv
           }else{
              du=""
              document.getElementById('mdiv'+i).style.display="none"
           }
       }else{
           document.getElementById('mdiv'+i).style.display="none"                                 
       }                
    }       
}
function reveza(qq){
  document.getElementById(qq).className="itens_menu_r"
}
function volta(qq){
  document.getElementById(qq).className="itens_menu"
}
