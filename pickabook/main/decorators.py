from functools import wraps
from django.http import Http404


def xhr_required(function=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.POST.get('is_xhr') or request.GET.get('is_xhr'):
                return view_func(request, *args, **kwargs)
            else:
                raise Http404()
        return _wrapped_view
    if function:
        return decorator(function)
    return decorator
