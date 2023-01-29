from django.core.exceptions import PermissionDenied


def user_is_employer(function):
    def wrap(request, *args, **kwargs):

        if request.user.role == "employer":
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap


def user_is_jobseeker(function):
    def wrap(request, *args, **kwargs):

        if request.user.role == "jobseeker":
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
