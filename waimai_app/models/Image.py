from django.db import models


class ImageStorage(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)

    verified = models.BooleanField(default=False)
    oss_key = models.CharField(max_length=512, null=False)
    create_time = models.DateTimeField()
