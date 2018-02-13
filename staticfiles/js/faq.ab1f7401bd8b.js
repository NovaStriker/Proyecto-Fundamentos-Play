function cargarPreguntas(){
	/*carga de jugadores desde leader.json*/

    $.getJSON("/static/data/faq.json", function(data) {
        $.each(data, function(key, val) {
            var pregunta = $('<div></div>');
            pregunta.attr('class','contenedor-pregunta');
            var h4 = $('<h4></h4>');
            h4.text(val['pregunta']);
            pregunta.append(h4);

            var respuesta = $('<div></div>');
            respuesta.attr('class','contenedor-respuesta'); 
            var p = $('<p></p>');
            p.text(val['respuesta']);
            respuesta.append(p);
            
            $('#seccion-preguntas').append(pregunta);
            $('#seccion-preguntas').append(respuesta);
        });
    });
}


$(window).on('load', function() {

    cargarPreguntas();    

});