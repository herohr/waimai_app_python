from waimai_app.models import Vendor, VendorBaseInfo
from django.http import JsonResponse
from waimai_app.restful import RESTFul, FormParser
from waimai_app.auth import authorize


class VendorAPI(RESTFul):
    @authorize
    def get(self, request):
        form = FormParser(request)

        school = form.get("most_popular_from")
        page = form.get("page")  #  一页十个
        if school and page:
            try:
                vendors = VendorBaseInfo.objects.filter(school=school).order_by("sales").reverse()
                index = int(page)*10
                vendors = vendors[index:index+10]
            except IndexError:
                return JsonResponse({
                    "reason": "this page has no vendor",
                    "code": "QUERY_INDEX_OUT"
                }, status=404)
            except ValueError:
                return JsonResponse({
                    "reason": "form_item page invalid",
                    "code": "FORM_ITEM_INVALID"
                }, status=401)

            return JsonResponse({
                "vendors": [{
                    "name": i.name,
                    "school": i.school,
                    "condition": i.condition,
                    "opening_time_day": i.opening_time_day,
                    "logo_url": i.logo_url,
                    "bulletin": i.bulletin,
                    "sales": i.sales,
                    "category": i.category
                } for i in vendors],
                "order_by": "sales"
            }, status=200)
