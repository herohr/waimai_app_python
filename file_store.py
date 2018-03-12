import hmac
from django.conf import settings
import oss2
import datetime
import base64
import json
from waimai_app.models import FileStorage


class OSS:
    def __init__(self, access_id, access_key, bucket_name, endpoint):
        self._access_ID = access_id
        self._access_key = access_key
        self._bucket_name = bucket_name
        self._endpoint = endpoint  # 设置OSS基本常量

        self.auth = oss2.Auth(access_id, access_key)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)  # 连接到OSS

    def sign_url(self, method, path, expires, headers=None, params=None):
        path = OSS.path_unified(path)

        return self.bucket.sign_url(method, path, expires, headers, params)  # 签名URL

    def policy(self, expires, path, filename=None, length_range=None, redirect_to=None, status=None):  # 签名POST表单

        now = datetime.datetime.now()
        expiration = now + datetime.timedelta(seconds=int(expires))
        expiration = expiration.isoformat() + "Z"  # 设置ISO format时间

        conditions = []
        if filename is not None:  # 指定文件名
            conditions.append(["eq", "$key", path + filename])
        if length_range is not None:
            conditions.append(["content-length-range", length_range[0], length_range[1]])

        if redirect_to is not None:  # 指定成功重定向
            conditions.append(["eq", "$success_action_redirect", redirect_to])
        if status is not None:  # 指定成功状态码
            conditions.append(["eq", "$success_action_status", str(status)])

        dic = {
            "expiration": expiration,
            "conditions": conditions
        }

        json_dic = json.dumps(dic)
        policy = base64.b64encode(json_dic.encode())
        signature = hmac.new(key=self._access_key.encode(), msg=policy, digestmod="sha1").digest()
        signature = base64.encodebytes(signature)  # 这里只能使用encodebytes方法
        return policy.decode(), signature.decode().strip()

    @staticmethod
    def path_unified(path):
        if path.startswith("/"):
            path = path[1:]
        return path


class FileStore:
    PRIVATE = 0
    PUBLIC_READ = 1
    PUBLIC_RW = 2

    def __init__(self, _id, _key, bucket_name, endpoint, router=None, control_lever=PUBLIC_RW, expires=600, with_db=True):
        print(bucket_name, endpoint)
        self.bucket_name = bucket_name
        self.endpoint = endpoint
        self.id = _id
        self.key = _key
        self.router = router
        self.control_lever = control_lever
        self.expires = expires
        self.oss = OSS(access_id=_id, access_key=_key, bucket_name=bucket_name, endpoint=endpoint)

        self.with_db = with_db

    def get_upload_form(self, filename, root="/", max_size=1024**3, user_id=None):
        print(root+filename)
        file_id = None
        if self.with_db:
            if not user_id:
                raise Exception("if with_db user_id is required")
            file = FileStorage(user_id=user_id,
                               bucket=self.bucket_name,
                               endpoint=self.endpoint,
                               verified=False,
                               oss_key=root+filename)
            file.save()

            file_id = file.id

        policy, signature = self.oss.policy(600, root, filename, length_range=(0, max_size), status=200)
        form = {
            "form_item": {
                "OSSAccessKeyId": self.id,
                "policy": policy,
                "Signature": signature,
                "key": root+filename,
                "success_action_status": 200,
            },
            "max_size": max_size,
            "host": "{}.{}".format(self.bucket_name, self.endpoint),
            "method": "post",
            "file_id": file_id if self.with_db else None
        }
        return form



"""
上传文件模块
文件储存于阿里云OSS，分别位于不同的bucket，不同的bucket下还有不同的文件夹。
不同的bucket具有不同的访问权限，但基本都是私有写。

下载：
对于公共读，直接传递URL就可以了。
对于私有读，进行URL签名就可以了。

上传：
上传的文件具有不同的类型，有些是文件，有些是图片，我们把他们统一看成文件。
文件储存于OSS需要给出bucket，目录，文件名。
对于应用来说，每个文件都要有关联信息，比如说是谁上传的，干什么用的。

"""


