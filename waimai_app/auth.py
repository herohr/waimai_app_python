from django.http import JsonResponse

from waimai_app import models
from waimai_app.rd_session import sessions
from waimai_app.restful import FormParser


def authorize(func):
    def _func(self, request):
        u_auth = "authorization"
        v_auth = "authorization_v"
        is_user = True
        au = None
        form = FormParser(request)

        au = au or request.GET.get(u_auth) or form.get(u_auth) or request.META.get("authorization")
        if not au:
            au = request.GET.get(v_auth) or form.get(v_auth)
            is_user = False

        user_id = sessions.get(au)

        if user_id is not None:
            try:
                if is_user:
                    user = models.User.objects.get(id=user_id)
                else:
                    user = models.Vendor.objects.get(id=user_id)
                setattr(request, "user", user)
                return func(self, request)
            except models.User.DoesNotExist or models.Vendor.DoesNotExist:
                pass

        return JsonResponse({
            "reason": "authorize failed"
        }, status=401)

    return _func


def v_authorize(func):
    def _func(self, request):
        v_auth = "authorization_v"
        au = None
        form = FormParser(request)

        au = au or request.GET.get(v_auth) or form.get(v_auth)

        user_id = sessions.get(au)

        if user_id is not None:
            try:
                vendor = models.Vendor.objects.get(id=user_id)
                setattr(request, "vendor", vendor)
                return func(self, request)
            except models.User.DoesNotExist or models.Vendor.DoesNotExist:
                pass

        return JsonResponse({
            "reason": "authorize failed"
        }, status=401)

    return _func