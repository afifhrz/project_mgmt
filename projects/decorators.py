from django.http import HttpResponseForbidden

def user_is_gm_or_agm(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name__in=['General Manager', 'Assistant General Manager']).exists():
            return HttpResponseForbidden("You are not authorized to view this page")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
