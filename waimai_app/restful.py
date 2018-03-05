from django.http import JsonResponse, QueryDict


class RESTFul:
    def __init__(self, model_name="Default"):
        self.name = model_name

    def router(self, methods=()):
        views = {}
        for i in methods:
            method = getattr(self, i.lower(), None)
            if callable(method):
                views[i] = method

        def _func(request):
            handler = views.get(request.method)
            if callable(handler):
                return handler(request)
            else:
                return RESTFul.method_not_allow()
        return _func

    @staticmethod
    def method_not_allow():
        return JsonResponse({}, status=405)

    def get(self, request):
        return self.method_not_allow()

    def post(self, request):
        return self.method_not_allow()

    def put(self, request):
        return self.method_not_allow()

    def delete(self, request):
        return self.method_not_allow()


class FormParser:
    def __init__(self, request):
        self.request = request
        if hasattr(request, "form"):
            self.query_dict = request.form
        else:
            self.query_dict = self.to_query_dict()

    def to_query_dict(self):
        return QueryDict(self.request.body, encoding=self.request.encoding)

    def get(self, key, default=None):
        return self.query_dict.get(key, default=default)

    # def get_one(self, key, default=None):
    #     val = self.query_dict.get(key, default)
    #     if val is None:
    #         return None
    #     else:
    #         if len(val) > 0:
    #             return val[0]
    #         else:
    #             return None
