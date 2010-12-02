function ajaxPost(url,params){
    $.ajax({
        url:url,
        data:params,
        type:'POST',
        success: function(response){
            if(params['successCallback']){
                params['successCallback'](response);
            }else{
                $('#ajax_status_header').text('Done');
                $('#ajax_status_header').fadeOut(5000);
            }
        },
        beforeSend:function(){
            $('#ajax_status_header').text('Processing...');
            $('#ajax_status_header').show();
        },
        error: function(response){
            if(params['errorCallback']){
                params['errorCallback'](response);
            }else{
                $('#ajax_status_header').text('Error. Please Try Again!');
                $('#ajax_status_header').show();
            }
        }
    });
}
