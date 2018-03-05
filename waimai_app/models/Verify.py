from django.db import models


class VerifyMessage(models.Model):
    request_id = models.CharField(primary_key=True, max_length=64)

    phone_number = models.CharField(max_length=12, null=False)
    code = models.CharField(max_length=32)
    message = models.CharField(max_length=64)

    verified = models.BooleanField(default=False)
    send_time = models.DateTimeField()


class VerifyCodeStore(models.Model):
    id = models.CharField(max_length=128, primary_key=True)
    oss_url = models.CharField(max_length=1024)
    local_path = models.CharField(max_length=1024)

    code = models.CharField(max_length=8)


class VerifyCodeCache(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=128)

    relative_msg = models.CharField(max_length=128)
