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
    last_30_days = models.IntegerField("最近30天",null=True)
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
