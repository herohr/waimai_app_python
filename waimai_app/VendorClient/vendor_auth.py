from django.utils import timezone

from waimai_app.models import Vendor, VendorBaseInfo, VerifyMessage, ImageStorage, VendorAuthInfo
from waimai_app import restful
from django.http import JsonResponse
from waimai_app.auth import authorize
from waimai_app.rd_session import sessions
from waimai_app.restful import FormParser
from waimai_app.image import get_url
from waimai_app.auth import authorize
from waimai_app.file_store import FileStore
from django.conf import settings

vendorAuthFileStore = FileStore.get_storage(settings.OSS_VENDOR_AUTH_BUCKET_NAME, FileStore.PRIVATE)

class VendorAuthAPI(restful.RESTFul):
    @authorize
    def get(self, request):
        form = FormParser(request)
        vendor_id = form.get("vendor_id")
        if not vendor_id:
            return JsonResponse({
                "reason": "vendor_id is required",
                "code": "FORM_ITEM_LACK"
            }, status=400)
        try:
            auth_info = VendorAuthInfo.objects.get(vendor_id=int(vendor_id))

        except VendorAuthInfo.DoesNotExist:
            return JsonResponse({
                "reason": "vendor's auth_info not found",
                "code": "AUTH_INFO_NOT_FOUND"
            }, status=404)

        image_id = auth_info.vendor_license_imageID

        try:
            image = .objects.get(id=image_id)
            url, _ = get_url(image.id, image.oss_key)

            return JsonResponse({
                "name": auth_info.vendor_responsible_person_name,
                "id_number": auth_info.vendor_responsible_person_ID,
                "licence_url": auth_info.url2
            })

        except ImageStorage.DoesNotExist:
            return JsonResponse({
                "reason": "server error",
                "code": "SERVER_ERROR"
            }, status=500)

    @authorize
    def post(self, request):
        form = FormParser(request)

        person_name = form.get("person_name")
        person_ident = form.get("person_id")






        ident_image_id = form.get("id_image_id")
        license_image_id = form.get("licence_image_id")

        if not (person_ident or person_name or ident_image_id or license_image_id):
            return JsonResponse({
                "reason": "form item required",
                "code": "FORM_ITEM_LACK"
            }, status=400)

        try:
            image_1 = ImageStorage.objects.get(id=int(ident_image_id))
            image_2 = ImageStorage.objects.get(id=int(license_image_id))
            if image_1.verified and image_2.verified:
                auth_info = VendorAuthInfo(
                    checked=False,
                    vendor_responsible_person_name=person_name,
                    vendor_responsible_person_ID=person_ident,
                    vendor_responsible_person_ID_imageID=ident_image_id,
                    vendor_license_imageID=license_image_id)
                auth_info.save()
                return JsonResponse({}, status=200)

            else:
                return JsonResponse({
                    "reason": "the image you upload is not verified",
                    "code": "IMAGE_NOT_VERIFIED"
                }, status=400)

        except ImageStorage.DoesNotExist:
            return JsonResponse({
                "reason": "image_id not exist",
                "code": "IMAGE_ID_NOT_EXIST"
            }, status=404)

        except ValueError:
            return JsonResponse({
                "reason": "illegal form item",
                "code": "FORM_ITEM_ILLEGAL"
            }, status=400)
