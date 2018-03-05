from django.db import models


class User(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=32)

    password = models.CharField(max_length=256)

    verified = models.BooleanField(default=False)


class UserInfo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()

    nickname = models.CharField(max_length=64)
    sex = models.CharField(max_length=4)
    age = models.IntegerField()
    college = models.CharField(max_length=64)

    register_time = models.DateTimeField()
    last_login_time = models.DateTimeField()


class ImageStorage(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)

    verified = models.BooleanField(default=False)
    oss_key = models.CharField(max_length=512, null=False)
    create_time = models.DateTimeField()


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=32)

    verify_condition = models.IntegerField(default=0)
    register_time = models.DateTimeField()


class VendorBaseInfo(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    address = models.CharField(max_length=256)
    condition = models.BooleanField(default=False)

    opening_time_day = models.CharField(max_length=64)
    logo_url = models.CharField(max_length=512)
    bulletin = models.CharField(max_length=1024)

    category = models.CharField(max_length=32)
    create_time = models.DateTimeField()


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
