function openModal() {
  document.getElementById('myModal').style.display = "block";
}

function closeModal() {
  document.getElementById('myModal').style.display = "none";
}

var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("demo");
  var captionText = document.getElementById("caption");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
  captionText.innerHTML = dots[slideIndex-1].alt;
}


function cargarGaleria() {
  $.getJSON("data/gallery.json", function(data) {
    var i = 1;
    $.each(data, function(key, val) {
      var divImg = $('<div></div>');
      divImg.attr('class','column');
      var img = $('<img></img>');
      img.attr('src',val['imagen']);
      img.attr('onclick','openModal();currentSlide('+i+')');
      img.attr('class','hover-shadow');
      divImg.append(img);

      var divSlide = $('<div></div>');
      divSlide.attr('class','mySlides');
      var imagen = $('<img></img>');  
      imagen.attr('src',val['imagen']);
      imagen.attr('style','width: 100%');
      var divText = $('<div></div>');
      divText.attr('class','numbertext');
      divText.text(i+' / '+data.length);
      divSlide.append(divText);
      divSlide.append(imagen);
      i++;
      $('#thumbnails').append(divImg);
      $('#idContent').append(divSlide);
    });
    var prev = $('<a></a>');
    prev.attr('onclick','plusSlides(-1)');
    prev.text('&#10094;');
    var next = $('<a></a>');
    next.attr('onclick','plusSlides(1)');
    next.text('&#10095;');

    var capt = $('<div></div>');
    capt.attr('class','caption-container');
    var pc = $('<p></p>');
    pc.attr('id','caption');
    capt.append(pc);

    $('#idContent').append(prev);
    $('#idContent').append(next);
    $('#idContent').append(capt);
  });
}

$('window').on('load', function () {
  cargarGaleria();
});