import hmac

import oss2
import datetime
import base64
import json


_id = "LTAIaNUnqzQf5kdD"
_key = "meEuxqz8GAGtbtuiZhj72C0XPiLgoY"
endpoint = "oss-cn-shenzhen.aliyuncs.com"
bucket_name = "sd-project-test"


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
        path = OSS.path_unified(path)

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

if __name__ == "__main__":
    oss = OSS(_id, _key, bucket_name, endpoint)
    url = oss.sign_url("PUT", "fucket.txt", 6000)
    print(url)
    host = "{}.{}".format(bucket_name, endpoint)
    import socket
    a = socket.socket()
    a.connect((host, 80))

    content = b"fucker"
    a.send("PUT {} HTTP/1.1\r\nHost: {}\r\nContent-Length: {}\r\n\r\n".format(url, host, len(content)).encode() + content)
    print(a.recv(2048))
"""
图片如何储存：
    储存于阿里云OSS
图片分几个种类：
    1：用户刚刚上传的，可见度为用户本身，此类图片有待服务器端验证
    2：验证过的图片，可见度为所有用户
图片储存表：
    id  uploader_id verified oss_key create_time
用户上传图片流程：    
    客户端请求服务端签名，获取表单项，构造请求，并上传至OSS
    客户端上传完成后将成功消息发送给服务端，服务器给出图片的签名URL。
    
"""