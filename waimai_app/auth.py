from django.http import JsonResponse

from waimai_app import models
from waimai_app.rd_session import sessions
from waimai_app.restful import FormParser


def authorize(func):
    def _func(self, request):
        u_auth = "authorization"
        v_auth = "authorization_v"
        au = None
        form = FormParser(request)
        au = au or request.GET.get(u_auth) or \
             form.get(u_auth)
        if not au:
            au = request.GET.get(v_auth) or form.get(v_auth)

        user_id = sessions.get(au)
        user = None


        if user_id is not None:
            try:
                user = models.User.objects.get(id=user_id)
                setattr(request, "user", user)
                return func(self, request)
            except models.User.DoesNotExist:
                pass

        return JsonResponse({
            "reason": "authorize failed"
        }, status=401)

    return _func
