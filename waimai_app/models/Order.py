from django.db import models


class Order(models.Model):
    user_id = models.IntegerField(null=False)
    vendor_id = models.IntegerField(null=False)
    address_id = models.IntegerField(null=False)

    order_items = models.CharField(max_length=1024, default="[]", verbose_name="订单项id列表")

    prime = models.FloatField(null=False, default=0, verbose_name="价格")

    prime_at_least = models.FloatField(verbose_name="最终用户支付价格")

    create_time = models.DateTimeField(verbose_name="订单创建时间", null=False)
    pay_time = models.DateTimeField(verbose_name="订单付款时间")
    vendor_ensure_time = models.DateTimeField(verbose_name="商家确认时间")
    ensure_time = models.DateTimeField(verbose_name="用户确认时间")