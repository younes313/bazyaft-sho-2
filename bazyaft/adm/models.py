from django.db import models
from django.contrib.auth.models import User

from user.models import Order , OrderHistory

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=128)
    name_farsi = models.CharField(max_length=128 , null=True)
    image = models.ImageField(upload_to='media/images/')


class FeedBack(models.Model):
    order = models.ForeignKey(OrderHistory, on_delete=models.SET_NULL ,null=True)
    user = models.ForeignKey(User,related_name="user_feedback", on_delete=models.SET_NULL ,null=True)
    driver = models.ForeignKey(User,related_name="driver_feedback", on_delete=models.SET_NULL , null=True)
    driver_score = models.FloatField(default=0)
    app_score = models.FloatField(default=0)
    suggest = models.TextField(blank=True)
