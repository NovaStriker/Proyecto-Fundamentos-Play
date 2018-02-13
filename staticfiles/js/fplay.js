function cargarCarousel(){
	/*carga jugadores al corousel desde leader.json*/

    $.getJSON("/static/data/leader.json", function(data) {
        $.each(data, function(key, val) {
            var item = $('<div></div>');
            if (val["unidad"]=="1"){
                item.attr('class','carousel-item active');
            }else{
                item.attr('class','carousel-item');
            }            
            var container = $('<div></div>');
            container.attr('class','d-flex w-100 h-100 justify-content-center');
            var caption = $('<div></div>');
            caption.attr('class','carousel-caption d-none d-md-block');

            var unidad = $('<h2></h2>');
            unidad.text('Nivel '+val["unidad"]);
            var contenido = $('<div></div>');
            contenido.attr('class','d-flex w-100 justify-content-center align-self-center');
            contenido.attr('id','datos');
            var boton = $('<a></a>');
            boton.attr('class','btn btn-lg btn-primary');
            boton.attr('href','{% url "app:leaderboard" %}');
            boton.attr('role','button');
            boton.text('Ver completo');

            var divImagen = $('<div></div>');
            var imagen = $('<img></img>');
            divImagen.attr('class','p-3'); 
            imagen.attr('class','rounded-circle');            
            imagen.attr('alt','img'+val["unidad"]);      
            imagen.attr('src',val["imagen"]);
            divImagen.append(imagen);


            var divDatos = $('<div></div>');
            divDatos.attr('class','p-3 align-self-center'); 

            var player = $('<h2></h2>');
            player.attr('id','name');
            player.text(val["nombres"]);
            var dias = $('<h3></h3>');
            var tiempo = $('<h3></h3>');
            dias.text(val["dias"]+' días en el primer lugar');
            tiempo.text('Tiempo record: '+val["tiempo"]);
            divDatos.append(player);
            divDatos.append(dias);
            divDatos.append(tiempo);   

            contenido.append(divImagen);
            contenido.append(divDatos); 
            caption.append(unidad);            
            //caption.append($('<p></p>').append(boton));

            container.append(contenido);
            
            /*
            var slideicon = $('<img></img>');
            slideicon.attr('class','first-slide');
            slideicon.attr('src','data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==');
            slideicon.attr('alt','Slide');

            item.append(slideicon);*/
            item.append(container);
            item.append(caption);
            
            $('#itemsCarousel').append(item);
        });
    });
}


$(window).on('load', function() {

    cargarCarousel();    

});