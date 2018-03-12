import json

import requests
from file_store import FileStore

_id = "LTAIaNUnqzQf5kdD"
_key = "meEuxqz8GAGtbtuiZhj72C0XPiLgoY"
endpoint = "oss-cn-shenzhen.aliyuncs.com"
bucket_name = "sd-project-test"

authorization = "a97be374-0827-11e8-af17-00163e0ad685"
"{'college': 'SDU', 'sex': 'm', 'user_id': 5, 'age': 11, 'nickname': 'boss'}"

print(bucket_name, endpoint)
fs = FileStore(_id, _key, bucket_name, endpoint)

form = fs.get_upload_form("fuck.txt", "fucker/")

print(repr(form["host"]))
print(form["form_item"]["OSSAccessKeyId"])
with requests.session() as session:
    resp = session.post("http://" + form['host'], data=form["form_item"], files={"file": b"fucker"})



print(dir(resp.request))
print(resp.request.body)
print(resp.content)
print(resp.status_code)
print(json.loads(resp.content.decode()))


