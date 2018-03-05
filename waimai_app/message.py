import json

import requests as http_request
from django.http import JsonResponse

from public_models import User
from waimai_app import restful
from waimai_app.models import VerifyMessage

LOCAL_URL = "http://localhost:8808/msg"


def send_message(phone_number, code):
    resp = http_request.post(LOCAL_URL, data={
        "phone_number": str(phone_number),
        "code": str(code)
    })
    return json.loads(resp.content.decode())

    content = "{'Code': 'Ok', 'RequestId': 'BA64CD9A-131A-4E9D-B6CA-EFE3DA132FA9', 'Message': 'Ok'}"


class MessageAPI(restful.RESTFul):
    def post(self, request):
        # POST方法用户客户端请求给用户发送验证码
        phone_number = request.POST.get("phone_number")
        client_id = request.POST.get("client_id")

        if len(phone_number) != 11:
            return JsonResponse({
                "reason": "phone_number is not allow"
            })

        if client_id:
            pass

        pass

    def put(self, request):
        """PUT 用于改变客户及短信验证状态"""
        form = restful.FormParser(request)
        phone_number = form.get("phone_number")
        code = form.get("code")
        request_id = form.get("request_id")

        if request_id is None:
            pass
        message = VerifyMessage.objects.get(request_id=request_id)
        if message.code == code:
            message.verified = True
            try:
                user = User.objects.get(phone=phone_number)
                user.verified = True
                message.save()
                user.save()

            except User.DoesNotExist:
                pass