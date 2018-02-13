
$('#login').on('click', function() {
    $('#modalRegister').modal('hide');
    $('#modalLogin').modal('show');
});

$('#register').on('click', function() {
    $('#modalLogin').modal('hide');
    $('#modalRegister').modal('show');
});

$('#login1').on('click', function() {    
    $('#modalRegister').modal('hide');
    $('#modalLogin').modal('show');    
});

$('#register1').on('click', function() {
    $('#modalLogin').modal('hide');
    $('#modalRegister').modal('show');
});