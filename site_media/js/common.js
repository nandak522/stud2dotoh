function ajaxCall(url, params, callType, dataType){
	var successCallback = params['successCallback'];
	var successCallbackParams = params['successCallbackParams'];
	delete params.successCallbackParams;
	delete params.successCallback;
	return $.ajax({
        url:url,
        data:params,
        dataType:dataType,
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
            $('#ajax_status_header').fadeOut(7000);
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

function ajaxPost(url, params, dataType){
    if(!dataType){
       dataType = 'html';
    }
	return ajaxCall(url, params, 'POST', dataType);    
}

function ajaxGet(url, params, dataType){
    if(!dataType){
       dataType = 'html';
    }
	return ajaxCall(url, params, 'GET', dataType);
}

function charCounter(max_count, field_id, status_meter_id){
    var content = $("#"+field_id).val();
    if(content.length <= max_count){
        $("#"+status_meter_id).html("<span class='black_stress'>"+String(max_count-content.length)+" characters left.</span>")
    }else{
        $("#"+status_meter_id).html("<span class='required'>Text Limit Reached</span>")
    }
}
function split(val) {
    return val.split( /,\s*/ );
}
function extractLast(term) {
    return split(term).pop();
}
function autocomplete_bind(element_id, url, anchor){
    if(anchor){
        autocomplete_dict = {
                    minLength:2,
                    search: function(){
                        // custom minLength
                        var term = extractLast(this.value);
                        if (term.length < 2){
                            return false;
                        }
                    },
                    source: function(request, response) {
                        $.getJSON(url, {term:extractLast(request.term)}, response);
                    },
                    focus: function() {
                        // prevent value inserted on focus
                        return false;
                    },
                    select:function(event, ui){
                        window.location = ui.item.value;
                        return false;
                    }
                }


    }else{
        autocomplete_dict = {
                    minLength:2,
                    search: function(){
                        // custom minLength
                        var term = extractLast(this.value);
                        if (term.length < 2){
                            return false;
                        }
                    },
                    source: function(request, response) {
                        $.getJSON(url, {term:extractLast(request.term)}, response);
                    },
                    focus: function() {
                        // prevent value inserted on focus
                        return false;
                    },
                    select:function(event, ui){
                        var terms = split(this.value);//split the existing tag items based on comma or space
                        terms.pop();//pop the latest incompleted word
                        terms.push(ui.item.value);//push the selected value for retrieved tags list
                        terms.push("");
                        this.value = terms.join(",");
                        return false;
                    }
                }

    }
        $(element_id).bind("keydown", function(event){
                    if(event.keyCode === $.ui.keyCode.TAB &&
                        $(this).data("autocomplete").menu.active){
                            event.preventDefault();
                    }
                  }).autocomplete(autocomplete_dict);
}
