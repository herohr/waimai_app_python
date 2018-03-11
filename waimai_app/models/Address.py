from django.db import models


class UserAddress(models.Model):
    user_id = models.IntegerField()
    school = models.CharField(max_length=256)
    location = models.CharField(max_length=1024)
    receiver = models.CharField(max_length=32)
    receiver_phone = models.CharField(max_length=11)