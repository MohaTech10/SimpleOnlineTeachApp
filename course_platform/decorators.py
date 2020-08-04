

from django.http import HttpResponse
from django.shortcuts import redirect, render


def mustLoggedOut(view_function):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper



# to prevent specific object from accessing this view
def allow_objects(in_group=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            group_current_user = None
            if request.user.groups.exists():
                group_current_user = request.user.groups.all()[0].name
            if group_current_user in in_group:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Not Allowed")
        return wrapper
    return decorator



# it just directs, actually it just takes each object to their own page based on their group that belongs to
# but we just put it before the dashboard cuz it will turn them to their page anyway
def if_admin(home_page):
    def wrapper(request, *args, **kwargs):

        current_user_group = None
        if request.user.groups.exists():
            current_user_group = request.user.groups.all()[0].name
        if current_user_group == 'teachers':
            return redirect('teacher')
        elif current_user_group == 'admin':
            return home_page(request, *args, **kwargs)
        elif current_user_group == 'students':
            return redirect('student')

    return wrapper