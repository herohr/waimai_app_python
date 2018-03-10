from django.db import models


# 食品
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    vendor_id = models.IntegerField(null=False)

    name = models.CharField(max_length=64, null=False, verbose_name="菜名")
    category = models.CharField(max_length=64)

    prime = models.FloatField(null=False, verbose_name="价格")
    info = models.CharField(max_length=256, verbose_name="详细信息")

    img_url = models.CharField(max_length=512, verbose_name="首页小图")
    big_img_url = models.CharField(max_length=512, verbose_name="主页大图")

    rate = models.IntegerField(verbose_name="好评率", default=0)
    sales = models.IntegerField(verbose_name="销量", default=0)