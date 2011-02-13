function ajaxCall(url, params, callType){
	var successCallback = params['successCallback'];
	var successCallbackParams = params['successCallbackParams'];
	delete params.successCallbackParams;
	delete params.successCallback;
	return $.ajax({
        url:url,
        data:params,
        type:callType,
        success: function(response){
            if(successCallback){
            	if(successCallbackParams){
            		successCallback(successCallbackParams, response);
            	}else{
            		successCallback(response);
            	}
            }
            $('#ajax_status_header').text('Done');
            $('#ajax_status_header').fadeOut(5000);
        },
        beforeSend:function(){
        	if(callType === 'GET'){
        		$('#ajax_status_header').text('Retrieving...');	
        	}else{
        		$('#ajax_status_header').text('Processing...');
        	}
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

function ajaxPost(url,params){
	return ajaxCall(url, params, 'POST');    
}

function ajaxGet(url, params){
	return ajaxCall(url, params, 'GET');
}

function charCounter(max_count, field_id, status_meter_id){
    var content = $("#"+field_id).val();
    if(content.length <= max_count){
        $("#"+status_meter_id).html("<span class='black_stress'>"+String(max_count-content.length)+" characters left.</span>")
    }else{
        $("#"+status_meter_id).html("<span class='required'>Text Limit Reached</span>")
    }
}