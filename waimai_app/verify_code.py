import random
import uuid

from django.http import JsonResponse
from django.utils import timezone

from waimai_app.models import VerifyCodeStore, VerifyCodeCache, VerifyMessage
from waimai_app import restful
from waimai_app import auth


LOCAL_URL = "http://localhost:8808/msg"


def send_message(phone_number, code):
    # resp = http_request.post(LOCAL_URL, data={
    #     "phone_number": str(phone_number),
    #     "code": str(code)
    # })
    #
    # return json.loads(json.loads(resp.content.decode()))


    # 测试
    print(phone_number, code)
    return {'Code': 'OK',
            'RequestId': uuid.uuid1(),
            'Message': 'OK'}


class VerifyCodeAPI(restful.RESTFul):
    def get(self, request):
        # def sync():
        #     with open("verify_code.txt", "r") as file:
        #         content = file.readlines()
        #         for i in content:
        #             _id, code, local_path = i.split()
        #             root = "http://verifyimagexw.oss-cn-hangzhou.aliyuncs.com/"
        #             new_code = VerifyCodeStore(id=_id, oss_url=root+_id, local_path=local_path, code=code)
        #             new_code.save()
        #
        # sync()

        line = random.randint(0, 10000)
        verify_code = VerifyCodeStore.objects.raw(
            "select * from waimai_app_verifycodestore limit {},1;".format(line))
        verify_code = verify_code[0]

        r_uuid = uuid.uuid1()
        _code = VerifyCodeCache(uuid=verify_code.id, relative_msg=r_uuid)
        _code.save()

        return JsonResponse({
            "img_url": verify_code.oss_url,
            "rdm_code": r_uuid  # 这里把新UUID作为混淆，防止用固定uuid逃避验证
        }, status=200)

    def post(self, request):
        form = restful.FormParser(request)
        phone_number = form.get("phone_number")
        code = form.get("code")
        rdm_code = form.get("rdm_code")

        try:
            code_cache = VerifyCodeCache.objects.get(relative_msg=rdm_code)
        except VerifyCodeCache.DoesNotExist:
            return JsonResponse({
                "reason": "Your rdm_code is wrong"
            }, status=404)

        try:
            code_store = VerifyCodeStore.objects.get(id=code_cache.uuid)
        except VerifyCodeStore.DoesNotExist:
            return JsonResponse({
                "reason": "unknown wrong"
            }, status=500)

        if code_store.code.lower() == code.lower():
            message_code = random.randint(10000, 99999)
            resp = send_message(phone_number, message_code)
            print(resp)
            if resp["Code"] != "OK":
                if resp["Code"] == "isv.BUSINESS_LIMIT_CONTROL":
                    return JsonResponse({
                        "reason": "isv.BUSINESS_LIMIT_CONTROL",
                        "code": "isv.BUSINESS_LIMIT_CONTROL"
                    }, status=400)

                return JsonResponse({
                    "reason": "error at sending message, error code: {}".format(resp["Code"])
                }, status=404)

            verify_message = VerifyMessage(
                request_id=resp["RequestId"],
                message=resp["Message"],
                phone_number=phone_number,
                code=message_code,
                send_time=timezone.now()
            )

            verify_message.save()

            return JsonResponse({
                "request_id": resp["RequestId"]
            }, status=200)
        else:
            return JsonResponse({
                "reason": "error verify code"
            }, status=403)


class MessageAPI(restful.RESTFul):

    def put(self, request):
        form = restful.FormParser(request=request)

        request_id = form.get("request_id")
        code = form.get("code")
        if code is None:
            return JsonResponse({
                "reason": "code required",
                "code": "FORM_ITEM_LACK"
            }, status=400)

        if request_id is not None:
            try:
                message = VerifyMessage.objects.get(request_id=request_id)
            except VerifyMessage.DoesNotExist:
                return JsonResponse({
                    "reason": "wrong request_id"
                }, status=404)

            if str(code) == message.code:
                message.verified = True
                message.save()

                return JsonResponse({

                }, status=200)

            else:
                return JsonResponse({
                    "reason": "wrong code"
                }, status=400)

        else:
            return JsonResponse({
                "reason": "request_id is required",
                "code": "FORM_ITEM_LACK"
            }, status=400)


verify_code_API = VerifyCodeAPI()
message_API = MessageAPI()
