

$(window).on('load',function(){
	$('#dismiss').on('click',function(){
	    var LOCAL_URL = "/teachers/question/dimiss/"+$('#qid').html()+"/";
	    $("#form").attr("action",LOCAL_URL);
	    $('#form').submit();


    });

    $('#save').on('click',function(){
	    var LOCAL_URL = "/teachers/question/save/"+$('#qid').html()+"/";
	    $("#form").attr("action",LOCAL_URL);
	    $('#form').submit();


    });
})