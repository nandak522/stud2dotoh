from django.http import Http404, HttpResponseRedirect

def is_post(view_function):
    def _wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return view_function(request, *args, **kwargs)
        raise Http404 
    return _wrapper

def is_get(view_function):
    def _wrapper(request, *args, **kwargs):
        if request.method == 'GET':
            return view_function(request, *args, **kwargs)
        raise Http404 
    return _wrapper

def is_ajax(the_function):
    def _wrapper(request, *args, **kwargs):
        if request.is_ajax():
            return the_function(request, *args, **kwargs)
        raise Http404
    return _wrapper
