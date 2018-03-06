from django.utils import timezone

from waimai_app.models import Vendor, VendorBaseInfo, VerifyMessage
from waimai_app import restful
from django.http import JsonResponse
from waimai_app.auth import authorize
from waimai_app.rd_session import sessions
from waimai_app.restful import FormParser


class UserAPI(restful.RESTFul):
    def post(self, request):
        form = FormParser(request)
        pw = form.get("password")
        request_id = form.get("request_id")
        if not 8 < len(pw) < 64:
            return JsonResponse({
                "reason": "password too long or too short"
            }, status=400)

        try:
            verify_message = VerifyMessage.objects.get(request_id=request_id)
        except VerifyMessage.DoesNotExist:
            return JsonResponse({
                "reason": "request_id wrong"
            }, status=404)

        if verify_message.verified is not True:
            return JsonResponse({
                "reason": "request not verified"
            }, status=403)

        query_set = Vendor.objects.filter(phone=verify_message.phone_number)
        if len(query_set) != 0:
            return JsonResponse({
                "reason": "phone already exist"
            }, status=400)

        new_user = Vendor(phone=verify_message.phone_number, password=pw, verified=False)

        new_user.save()

        return JsonResponse({}, status=200)

    def put(self, request):
        pass


class UserInfoAPI(restful.RESTFul):
    @authorize
    def get(self, request):
        get_id = request.GET.get("id") or request.user.id
        try:
            vendor = VendorBaseInfo.objects.get(user_id=get_id)
        except VendorBaseInfo.DoesNotExist:
            return JsonResponse({
                "reason": "Vendor's info does not exist"
            }, status=404)

        return JsonResponse({
            "vendor_id": vendor.vendor_id,
            "name": vendor.name,
            "address": vendor.address,
            "condition": vendor.condition,
            "logo_url": vendor.logo_url,
            "bulletin": vendor.bulletin,
            "category": vendor.category
        }, status=200)

    @authorize
    def post(self, request):
        form = FormParser(request)
        try:
            VendorBaseInfo.objects.get(vendor_id=request.user.id)
            return JsonResponse({
                "reason": "The user's info already exist"
            }, status=400)
        except VendorBaseInfo:
            dic = {
                "name": form.get("name"),
                "phone": form.get("phone"),
                "address": form.get("address"),
                "category": form.get("category"),
                "create_time": timezone.now()
            }

            for k, v in dic.items():
                if v is None:
                    return JsonResponse({
                        "reason": "{} is required".format(k)
                    }, status=400)

            vendor_info = VendorBaseInfo(
                **dic
            )
            vendor_info.save()

            return JsonResponse({}, status=200)

    @authorize
    def put(self, request):
        form = FormParser(request)
        vendor_info = VendorBaseInfo.objects.get(vendor_id=request.user.id)

        form_dict = {
            "name": form.get("name"),
            "address": form.get("address"),
            "logo_url": form.get("logo_url"),
            "bulletin": form.get("bulletin"),
            "category": form.get("category"),
            "opening_time_day": form.get("opening_time_day"),
            "phone": form.get("phone")
        }

        changed = {}
        for k, v in form_dict.items():
            if v is not None:
                changed[k] = v

        for key, val in changed.items():
            if val[0] is not None:
                vendor_info.__setattr__(key, val[0])

        vendor_info.save()
        return JsonResponse({"changed": changed}, status=200)


userAPI = UserAPI()
user_info_API = UserInfoAPI()


def login(request):
    if request.method == "POST":
        form = FormParser(request)
        phone = form.get("phone")
        password = form.get("password")

        if phone is None or password is None:
            return JsonResponse({
                "reason": "Need phone or password",
            }, status=400)

        try:
            result = Vendor.objects.get(phone=phone, password=password)
        except Vendor.DoesNotExist:
            return JsonResponse({
                "reason": "Username or password wrong!",
            }, status=400)

        uuid = sessions.create_session(_id=result.id)
        resp = JsonResponse({
            "authorization": uuid,
            "user_id": result.id
        }, status=200)
        resp.set_cookie("sessionID", uuid)
        return resp

    else:
        return JsonResponse({}, status=405)
