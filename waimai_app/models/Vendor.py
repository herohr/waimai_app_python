from django.db import models


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=32)
    password = models.CharField(max_length=256, null=True)

    verify_condition = models.IntegerField(default=0)
    register_time = models.DateTimeField()


class VendorBaseInfo(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_id = models.IntegerField(null=False)

    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=32)
    address = models.CharField(max_length=256)
    condition = models.BooleanField(default=False)

    opening_time_day = models.CharField(max_length=64)
    logo_url = models.CharField(max_length=512)
    bulletin = models.CharField(max_length=1024)

    category = models.CharField(max_length=32)
    create_time = models.DateTimeField()


class VendorAuthInfo(models.Model):
    vendor_id = models.IntegerField(null=False)

    vendor_responsible_person_name = models.CharField(null=False, verbose_name="负责人名", max_length=32)
    vendor_responsible_person_ID = models.CharField(null=False, verbose_name="负责人身份证", max_length=64)
    vendor_responsible_person_ID_imageID = models.IntegerField(verbose_name="负责人身份证照片ID")
    vendor_license_imageID = models.IntegerField(verbose_name="营业执照照片ID")

