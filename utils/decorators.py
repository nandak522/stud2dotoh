from django.http import Http404

def is_post(view_function):
    def inner(request, *args, **kwargs):
        if request.method == 'POST':
            return view_function(request, *args, **kwargs)
        raise Http404 
    return inner