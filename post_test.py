import json

import requests

authorization = "a97be374-0827-11e8-af17-00163e0ad685"
"{'college': 'SDU', 'sex': 'm', 'user_id': 5, 'age': 11, 'nickname': 'boss'}"

with requests.session() as session:
    resp = session.post('http://localhost:8000/users/login', data={
        "phone": "testtest",
        "password": "qwekqjql",
        "email": "sficasd"
    })
# d = json.loads(resp.content.decode())
# post_dict = d["form_item"]
#
# with requests.session() as session:
#     ali_resp = session.post("http://sd-project-test.oss-cn-shenzhen.aliyuncs.com", data=post_dict, files={"file": b"fucker"})
#
# print(ali_resp.status_code, ali_resp.content)


print(dir(resp.request))
print(resp.request.body)
print(resp.status_code)
print(json.loads(resp.content.decode()))


