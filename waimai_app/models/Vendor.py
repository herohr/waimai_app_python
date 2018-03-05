from django.db import models


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