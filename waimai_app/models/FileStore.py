from django.db import models


class FileStorage(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.CharField(max_length=128)

    bucket = models.CharField(max_length=64)
    endpoint = models.CharField(max_length=128)

    img_height = models.IntegerField()
    img_width = models.IntegerField()
    file_format = models.CharField(max_length=32)
    file_size = models.IntegerField(null=False)

    verified = models.BooleanField(default=False)
    oss_key = models.CharField(max_length=512, null=False)
    create_time = models.DateTimeField()
