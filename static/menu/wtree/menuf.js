jQuery.noConflict();

MenuWin = function(p,id,s,dirimgs)
{
 	var obj = this; // refer�ncia ao pr�prio objeto MenuWin
 	var st = (typeof s != 'undefined' && s != null) ? s : false;
	var parent = document.getElementById(p); // objeto que ser� o container do menu
	var menu = document.createElement("div"); // o menu
	menu.setAttribute("id",id);
	menu.setAttribute((document.all)?"className":"class","menuWin");
	
	var header = document.createElement("span"); // cabe�alho do menu
	header.setAttribute((document.all)?"className":"class","menuWin-header");
	var headerText = null;
	
	var images = new Array(new Image(),new Image());
	images[0].src = dirimgs+"arrow_up.gif";
	images[1].src = dirimgs+"arrow_down.gif";
	
	var arrow = document.createElement("img"); // imagem para retrair e extender o menu
	arrow.setAttribute("alt","");
	arrow.setAttribute("title","");
	arrow.setAttribute("src",images[0].src);
	arrow.onclick = function()
	{
		if(this.getAttribute("src").indexOf("up") > -1)
		{
			this.setAttribute("src",images[1].src);
			jQuery("#"+body.getAttribute("id")).animate({height: "hide",opacity: "hide"},"slow");
		}
		else
		{
			this.setAttribute("src",images[0].src);
			jQuery("#"+body.getAttribute("id")).animate({height: "show",opacity: "show"},"slow");
		}
	}
	
	var arrowContainer = document.createElement("span"); // container da imagem que retrai e extende o menu
	arrowContainer.setAttribute((document.all)?"className":"class","menuWin-arrow");
	arrowContainer.appendChild(arrow);
	
	menu.appendChild(arrowContainer);
	menu.appendChild(header);
	
	var body = document.createElement("ul"); // corpo do menu
	body.setAttribute("id","menuWin-body-"+id);
	body.setAttribute((document.all)?"className":"class","menuWin-body");
	
	obj.state = function()
	{
		body.style.display = "none";
		arrow.setAttribute("src",images[1].src);
	};
	
	// fun��o para setar o cabe�alho do menu
	this.setTitle = function(t)
	{
		headerText = document.createTextNode(t);
		header.appendChild(headerText);
	};
	
	// fun��o para setar os itens do menu
	// recebe como par�metros o texto, o link, o target e a imagem do item
	this.setItens = function(t,a,tg,i)
	{
		var li = document.createElement("li");
		var link = document.createElement("a");
		var img = document.createElement("img");
		var imgContainer = document.createElement("div");
			
		if(i != null)
		{
			img.setAttribute("alt","");
			img.setAttribute("title","");
			img.setAttribute("src",i);
			imgContainer.appendChild(img);
		}
		
		link.appendChild(imgContainer);
		
		link.setAttribute("href",a);
		if(tg != null) link.setAttribute("target",tg);
		link.appendChild(document.createTextNode(t));
		
		li.appendChild(link);
		
		body.appendChild(li);
	};

	// esta fun��o extende o container da image que retrai e extende o menu,
	// para manter alinhado o texto dos itens do menu.
	this.heightLine = function()
	{
		var linhas = body.getElementsByTagName("li");
		for(i = 0; i < linhas.length; i++)
		{
			while(linhas[i].getElementsByTagName("div")[0].offsetHeight < linhas[i].offsetHeight)
			linhas[i].getElementsByTagName("div")[0].style.height = linhas[i].offsetHeight+"px";
		}
	};
	
	// fun��o para inserir na tela o menu
	this.draw = function()
	{
		if(headerText == null)
		{
			headerText = document.createTextNode("Menu");
			header.appendChild(headerText);
		}
		menu.appendChild(body);
		parent.appendChild(menu);
		
		obj.heightLine();
		if(st) obj.state();
	};
	
};
