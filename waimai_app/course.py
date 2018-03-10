from collections import defaultdict

from waimai_app.restful import RESTFul, FormParser
from waimai_app.auth import authorize, v_authorize
from waimai_app.models.Course import Course
from django.http import JsonResponse


class CourseAPI(RESTFul):
    @authorize
    def get(self, request):
        form = FormParser(request)
        course_id = form.get("course_id")
        if course_id is not None:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return JsonResponse({
                    "reason": "course_id not found"
                }, status=404)

        vendor_id = form.get("vendor_id")
        if vendor_id is not None:
            courses = Course.objects.filter(vendor_id=vendor_id).all()
            results = [{
                "course_id": i.id,
                "name": i.name,
                "prime": i.prime,
                "info": i.info,
                "img_url": i.url,
                "big_img_url": i.url,
                "rate": i.rate,
                "sales": i.sales
            } for i in courses]

            return JsonResponse(results, status=200)

        return JsonResponse({
            "reason": "no limitation"
        }, status=400)

    @v_authorize
    def post(self, request):
        form = FormParser(request)
        require_dict = {
            "name": form.get("name"),
            "course_id": form.get("course_id"),
            "prime": form.get("prime"),
            "info": form.get("info"),
        }
        for k, v in require_dict.items():
            if v is None:
                return JsonResponse({
                    "reason": "form item {} is required".format(k)
                }, status=403)
        new_course = Course(**require_dict)
        new_course.save()
        return JsonResponse({
            "course_id": new_course.id
        }, status=200)

    @v_authorize
    def put(self, request):
        form = FormParser(request)
        items = {
            "id": form.get("course_id"),
            "vendor_id": request.vendor.id,
            "prime": form.get("prime"),
            "category": form.get("category"),
            "info": form.get("info"),
            "img_url": form.get("img_url"),
            "big_img_url": form.get("big_img_url")
        }
        try:
            course = Course.objects.get(id=items["id"])
        except Course.DoesNotExist:
            return JsonResponse({
                "reason": "course not found"
            }, status=404)

        _ = {course.__setattr__(k, v) for k, v in items.items() if v is not None}

        return JsonResponse({}, status=200)

course_API = CourseAPI()
