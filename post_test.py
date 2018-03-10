import json

import requests

authorization = "a97be374-0827-11e8-af17-00163e0ad685"
"{'college': 'SDU', 'sex': 'm', 'user_id': 5, 'age': 11, 'nickname': 'boss'}"

with requests.session() as session:
    resp = session.post('http://localhost:8000/vendors', data={
        "phone": "testtest",
        "password": "qwekqjqlasdasd",
        "email": "sficasd"
    })


print(dir(resp.request))
print(resp.request.body)
print(resp.status_code)
print(json.loads(resp.content.decode()))


