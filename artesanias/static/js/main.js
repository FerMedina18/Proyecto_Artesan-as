$(document).ready(function(){
    $('.sidemenu li:has(ul)').click(function(e){
        e.preventDefault();

        if($(this).hasClass('active')){
            $(this).removeClass('active');
            $(this).children('ul').slideUp();
        }else{
            $('.sidemenu li ul').slideUp();
            $('.sidemenu li').removeClass('active');
            $(this).addClass('active');
            $(this).children('ul').slideDown();
        }
    });

    $('.sidemenu li ul a').click(function(){
         window.location.href = $(this).attr("href");
    });

    $('.menu').on('click', clickAction);

	$('.close-btn').on('click', clickAction);

	$('.fade-bg').on('click', clickAction);

	function clickAction(){
		$('.sidenav').toggleClass('active');
        $('.fade-bg').toggleClass('active');
	}

    $(window).resize(function(){
        if($(document).width() > 725){
            $('.sidemenu li:has(ul)').removeClass('active');
            $('.sidemenu li:has(ul)').children('ul').slideUp();
            $('.sidenav').removeClass('active');
            $('.fade-bg').removeClass('active');

            $('.catg ul li').removeClass('active');
            $('.catg ul li').slideUp();
        }
    });

    $('.submenu .catg .boton').click(function(e){
        e.preventDefault(); 
    });

    $('.fade-sm').click(function(){
        $('.catg ul li').removeClass('active');
        $('.catg ul li').slideUp();
        $('.fade-sm').removeClass('active');
    });

    $('.submenu .catg a').click(function(){
        if($('.catg ul li').hasClass('active')){
            $('.catg ul li').removeClass('active');
            $('.catg ul li').slideUp();
            $('.fade-sm').removeClass('active');
        }else{
            $('.catg ul li').addClass('active');
            $('.fade-sm').addClass('active');
        }
    });

    /* regresar arriba */
    mbutton = document.getElementById("mbutton");

    window.onscroll = function(){scrollFunction()};

    function scrollFunction(){
        if (document.body.scrollTop > 90 || document.documentElement.scrollTop > 90){
            mbutton.style.display = "block";
        }else{
            mbutton.style.display = "none";
        }
    }
    
    $('#mbutton').on('click', totop);

    function totop(){
        document.body.scrollTop = 0;

        document.documentElement.scrollTop = 0;
    }

    $('#imageperfiluc').on('change', validarImagen);

    /* validar imagenes */
    function validarImagen(){
        var archivo = document.getElementById("imageperfiluc");
        var fileName = document.getElementById("imageperfiluc").value;
        var idxDot = fileName.lastIndexOf(".") + 1;
        var extFile = fileName.substr(idxDot, fileName.length).toLowerCase();
        if (extFile=="jpg" || extFile=="jpeg" || extFile=="png"){

            if(archivo.files && archivo.files[0]){
                var ver = new FileReader();

                ver.onload=function(e){
                    document.getElementById('visualizar').innerHTML =
                    '<embed src="'+e.target.result+'" width="200" height="200" style="border-radius:50%; margin-top:40px;">';
                }
                ver.readAsDataURL(archivo.files[0]);
            }
        }else{
            alert("Solo se permite archivos cuya extensión sean jpg, png o jpeg");
        }   
    }
});