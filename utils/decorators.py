from django.http import Http404

def is_post(view_function):
    def inner(request, *args, **kwargs):
        if request.method == 'POST':
            return view_function(request, *args, **kwargs)
        raise Http404 
    return inner

def is_get(view_function):
    def inner(request, *args, **kwargs):
        if request.method == 'GET':
            return view_function(request, *args, **kwargs)
        raise Http404 
    return inner

def is_ajax(the_function):
    def _is_ajax(request, *args, **kwargs):
        if request.is_ajax():
            return the_function(request, *args, **kwargs)
        raise Http404
    return _is_ajax