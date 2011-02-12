function close_answering(question_id){
    confirm_close = confirm('Are you sure you want to close answering ? Other people will not be able to give their answers from now on!');
    if(confirm_close){
        ajaxPost('/questions/closeanswering/', {'question_id':question_id, 'successCallback':show_closed_answering});
    }
}

function accept_answer(question_id, answer_id){
    ajaxPost('/questions/'+question_id+'/acceptanswer/', {'answer_id':answer_id, 'successCallback':show_accepted_answer});
}

function show_closed_answering(response){
    $('#give_answer_section').html(response);
    $('#ajax_status_header').text('Closed Answering!');
    //$('#ajax_status_header').fadeOut(5000);
}

function show_accepted_answer(response){
    $('#all_answers').html(response);
    $('#ajax_status_header').text('Done!');
    $('#ajax_status_header').fadeOut(5000);
}