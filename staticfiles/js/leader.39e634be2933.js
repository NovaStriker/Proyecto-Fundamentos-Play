function cargarLeader(){
	/*carga de jugadores desde leader.json*/

    $.getJSON("/static/data/leader.json", function(data) {
        $.each(data, function(key, val) {
            var fila = $('<div></div>');
            fila.attr('class','d-flex justify-content-around p-0');
            fila.attr('id','player');

            var divImagen = $('<div></div>');
            var imagen = $('<img></img>');
            var overlay = $('<div></div>');
            var texto = $('<div></div>');
            divImagen.attr('class','col-sm-3 item-center pt-3'); 
            imagen.attr('class','rounded-circle');
            imagen.attr('id','imgLeader');   
            imagen.attr('alt','img'+val["unidad"]);      
            imagen.attr('src',val["imagen"]);
            overlay.attr('class','overlay');
            texto.attr('class','text');
            texto.text('NIVEL '+val["unidad"]);
            overlay.append(texto);
            divImagen.append(imagen);
            

            var contenido = $('<div></div>');
            var player = $('<h3></h3>');
            var datos = $('<div></div>');
            contenido.attr('class','col-sm-8 align-self-center');
            player.attr('class','');
            player.text(val["nombres"]);
            datos.attr('class','d-flex');
            var dias = $('<h4></h4>');
            var tiempo = $('<h4></h4>');
            dias.text(val["dias"]+' días');
            dias.attr('class','col-sm-4 dias');
            tiempo.text('Tiempo: '+val["tiempo"]);
            tiempo.attr('class','col-sm-8 tiempo');
            datos.append(dias);
            datos.append(tiempo);
            contenido.append(player);
            contenido.append(datos);  

            divImagen.append(overlay); 

            fila.append(divImagen);
            fila.append(contenido);
            
            $('#leaderboard').append(fila);
        });
    });
}


$(window).on('load', function() {

    cargarLeader();    

});