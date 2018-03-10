from django.db import models


class ImageStorage(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)

    bucket = models.CharField(max_length=64)
    endpoint = models.CharField(max_length=128)

    img_height = models.IntegerField()
    img_width = models.IntegerField()
    img_format = models.CharField(max_length=32)
    img_size = models.IntegerField(null=False)

    verified = models.BooleanField(default=False)
    oss_key = models.CharField(max_length=512, null=False)
    create_time = models.DateTimeField()

