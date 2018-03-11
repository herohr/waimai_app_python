import json

from django.http import JsonResponse
from waimai_app.restful import RESTFul, FormParser
from waimai_app.models import Order, Course
from waimai_app.auth import authorize


class OrderAPI(RESTFul):
    @authorize
    def post(self, request):
        form = FormParser(request)

        order_items = form.get("order_items")
        prime = 0
        if isinstance(order_items, list):
            for i in order_items:
                try:
                    course = Course.objects.get(id=int(i))
                except ValueError:
                    return JsonResponse({
                        "reason": "course id illegal",
                        "code": "INVALID_FORM"
                    }, status=400)
                except Order.DoesNotExist:
                    return JsonResponse({
                        "reason": "course not found",
                        "code": "COURSE_NOT_FOUND"
                    }, status=404)

                prime += course.prime

            pass

    @authorize
    def get(self, request):
        form = FormParser(request)

        order_id = form.get("order_id")
        if not order_id:
            return JsonResponse({
                "reason": "form_item order_id required",
                "code": "FORM_ITEM_LACK"
            }, status=400)

        try:
            order = Order.objects.get(id=int(order_id))
        except Order.DoesNotExist:
            return JsonResponse({
                "reason": "order not found",
                "code": "ORDER_NOT_FOUND"
            }, status=404)
        except ValueError:
            return JsonResponse({
                "reason": "order_id must be int",
                "code": "INVALID_FORM_ITEM"
            }, status=401)

        return JsonResponse({
            "order_id": order.id,
            "vendor_id": order.vendor_id,
            "prime_at_least": order.prime_at_least,
            "create_time": order.create_time,
            "pay_time": order.pay_time,
            "vendor_insure_time": order.vendor_ensure_time,
            "ensure_time": order.ensure_time,
            "order_item_id_list": json.loads(order.order_items),
            "address_id": order.address_id
        })

