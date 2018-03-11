from django.http import JsonResponse
from waimai_app.restful import RESTFul, FormParser
from waimai_app.auth import authorize
from waimai_app.models import UserAddress


class UserAddressAPI(RESTFul):
    @authorize
    def get(self, request):
        form = FormParser(request)
        user_id = form.get("user_id")
        if user_id:
            if str(user_id) != str(request.user.id):
                return JsonResponse({
                    "reason": "your id is not equals user_id",
                    "code": "ACCESS_DENIED_CROSS"
                }, status=405)
            addresses = UserAddress.objects.filter(user_id=request.user.id).all()

            addresses_resp = []
            for i in addresses:
                addresses_resp.append({
                    "school": i.school,
                    "name": i.receiver,
                    "phone": i.receiver_phone,
                    "location": i.location
                })

            return JsonResponse({
                "user_addresses": addresses_resp
            }, status=200)

        address_id = form.get('address_id')
        if address_id:
            pass

    @authorize
    def post(self, request):
        form = FormParser(request)
        name = form.get("name")
        phone = form.get("phone")
        location = form.get("location")
        school = form.get("school")

        if name and phone and location and school:
            if request.is_from_user:
                address = UserAddress(
                    user_id=request.user.id,
                    receiver=name,
                    receiver_phone=phone,
                    location=location,
                    school=school)
                address.save()
                return JsonResponse({}, status=200)

        else:
            return JsonResponse({
                "reason": "form_item required",
                "code": "FORM_ITEM_LACK"
            }, status=400)
