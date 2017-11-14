from django.db import models

# Create your models here.


class Station(models.Model):
    platform = models.CharField("账号", max_length=32, null=True)
    station = models.CharField("站点", max_length=64, null=True)

    def __str__(self):
        return self.station


class Feedback(models.Model):
    date = models.DateField("日期")
    station = models.ForeignKey(Station)
    store = models.CharField("店铺", max_length=64, null=True)
    last_30_days = models.IntegerField("最近30天", null=True)
    last_90_days = models.IntegerField("最近90天", null=True)
    last_12_months = models.IntegerField("最近12个月", null=True)
    lifetime = models.IntegerField("全部", null=True)
    last_day = models.IntegerField("最近1天", null=True)
    last_week = models.IntegerField("最近1周", null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")

    class Meta:
        verbose_name_plural = "Feedback"
        verbose_name = "Feedback"


class FeedbackInfo(models.Model):
    date = models.DateField()
    shop_name = models.CharField(max_length=64, blank=True, null=True)
    last_30_days = models.IntegerField(blank=True, null=True)
    last_90_days = models.IntegerField(blank=True, null=True)
    last_12_months = models.IntegerField(blank=True, null=True)
    lifetime = models.IntegerField(blank=True, null=True)
    last_day = models.IntegerField(blank=True, null=True)
    last_week = models.IntegerField(blank=True, null=True)
    last_month = models.IntegerField(blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    zone = models.CharField(max_length=64, blank=True, null=True)

    def to_dict(self):
        return {"date": self.date, "shop_name": self.shop_name,
                "last_30_days": self.last_30_days, "last_90_days": self.last_90_days,
                "last_12_months": self.last_12_months, "lifetime": self.lifetime,
                "last_day": self.last_day, "last_week": self.last_week,
                "last_month": self.last_month, "create_time": self.create_time,
                "update_time": self.update_time, "zone": self.zone,
                }

    class Meta:
        managed = False
        db_table = 'feedback'


class AmazonRefShopList(models.Model):
    # Field name made lowercase.
    id = models.AutoField(db_column='ID', primary_key=True)
    shop_name = models.CharField(max_length=50, blank=True, null=True)
    shop_url = models.CharField(max_length=255, blank=True, null=True)
    zone = models.CharField(max_length=8, blank=True, null=True)
    brand = models.CharField(max_length=40, blank=True, null=True)
    type = models.CharField(max_length=40, blank=True, null=True)
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'amazon_ref_shop_list'