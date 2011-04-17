function settings(settings_type_id, responseText){
	$('#'+settings_type_id+'_settings').html(responseText);
}

function save_personal_settings(form_name){
	var form = document.forms[form_name];
	var slug = '';
	if(form.slug){
		slug = form.slug.value;
	}
	var csrfmiddlewaretoken = form.csrfmiddlewaretoken.value;
	ajaxPost('/settings/personal/', {'name':form.name.value, 'slug':slug, 'new_password':form.new_password.value, 'csrfmiddlewaretoken':csrfmiddlewaretoken, 'successCallback':settings, 'successCallbackParams':'personal'});
	form.save_personal_settings_button.value = 'Saved';
}

function save_acad_settings(form_name){
	var form = document.forms[form_name];
	form.save_acad_settings_button.value = 'Saved';
	var csrfmiddlewaretoken = form.csrfmiddlewaretoken.value;
	ajaxPost('/settings/acad/', {'branch':form.branch.value, 'college':form.college.value, 'start_year':form.start_year.value, 'end_year':form.end_year.value, 'aggregate':form.aggregate.value, 'csrfmiddlewaretoken':csrfmiddlewaretoken, 'successCallback':settings, 'successCallbackParams':'acad'});
}

function save_workinfo_settings(form_name){
	var form = document.forms[form_name];
	form.save_workinfo_settings_button.value = 'Saved';
	var csrfmiddlewaretoken = form.csrfmiddlewaretoken.value;
	ajaxPost('/settings/workinfo/', {'workplace':form.workplace.value, 'designation':form.designation.value, 'years_of_exp':form.years_of_exp.value, 'csrfmiddlewaretoken':csrfmiddlewaretoken, 'successCallback':settings, 'successCallbackParams':'workinfo'});
}

function get_acad_settings(){
       ajaxGet('/settings/acad/', {'successCallback':settings, 'successCallbackParams':'acad'});
}

function get_workinfo_settings(){
       ajaxGet('/settings/workinfo/', {'successCallback':settings, 'successCallbackParams':'workinfo'});
}