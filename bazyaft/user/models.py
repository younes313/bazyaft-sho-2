# from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Order(models.Model):
    values = {
        "alminium" : 1000,
        "pet": 2000,
        "khoshk": 3000,
        "daftar_ketab": 4000,
        "shishe": 5000,
        "parche": 6000,
        "naan": 7000,

    }


    user = models.ForeignKey(User,related_name="user", on_delete=models.SET_NULL ,null=True)
    driver = models.ForeignKey(User,related_name="driver", on_delete=models.SET_NULL , null=True)
    location_x = models.FloatField(default=0)
    location_y = models.FloatField(default=0)

    alminium = models.IntegerField(default=0)
    pet = models.IntegerField(default=0)
    khoshk = models.IntegerField(default=0)
    daftar_ketab = models.IntegerField(default=0)
    shishe = models.IntegerField(default=0)
    parche = models.IntegerField(default=0)
    naan = models.IntegerField(default=0)
    sayer = models.IntegerField(default=0)

    # kaghaz_moghava = models.IntegerField(default=0)
    # felezat = models.IntegerField(default=0)
    # ahan_sangin = models.IntegerField(default=0)
    # ahan_sabok = models.IntegerField(default=0)
    # zayeat_elecronic = models.IntegerField(default=0)

    coins = models.IntegerField(default=0)
    bag = models.IntegerField(default=0)
    money = models.IntegerField(default=0)

    pelak_melak = models.TextField(blank=True)
    give_back_type = models.CharField(max_length=20 , default="")
    order_status = models.CharField(max_length=20 , default="not confirmed")

    date_created = models.DateTimeField(auto_now_add = True)

    def calculate_sum(self):
        # + self.kaghaz_moghava + self.felezat + self.ahan_sangin + self.ahan_sabok + self.zayeat_elecronic
        sum = self.alminium +self.pet + self.khoshk + self.daftar_ketab + self.shishe + self.parche + self.naan +self.sayer
        return sum

    def calculate_coins(self):
        # + self.kaghaz_moghava + self.felezat + self.ahan_sangin + self.ahan_sabok + self.zayeat_elecronic
        # sum = self.alminium +self.pet + self.khoshk + self.daftar_ketab + self.shishe + self.parche + self.naan +self.sayer
        return self.calculate_sum() * 5

    def calculate_money(self):
        sum = self.alminium * self.values['alminium'] +self.pet * self.values['pet'] + self.khoshk * self.values['khoshk'] + self.daftar_ketab * self.values['daftar_ketab'] + self.shishe * self.values['shishe'] + self.parche * self.values['parche'] + self.naan * self.values['naan']
        return sum


#
# class OrderHistory(models.Model):
#     id = models.IntegerField(primary_key=True)
#     data_done = models.DateTimeField(auto_now_add = True)

class OrderHistory(models.Model):
    user = models.ForeignKey(User,related_name="user_history", on_delete=models.SET_NULL ,null=True)
    driver = models.ForeignKey(User,related_name="driver_history", on_delete=models.SET_NULL , null=True)
    location_x = models.FloatField(default=0)
    location_y = models.FloatField(default=0)

    alminium = models.IntegerField(default=0)
    pet = models.IntegerField(default=0)
    khoshk = models.IntegerField(default=0)
    daftar_ketab = models.IntegerField(default=0)
    shishe = models.IntegerField(default=0)
    parche = models.IntegerField(default=0)
    naan = models.IntegerField(default=0)
    sayer = models.IntegerField(default=0)

    # kaghaz_moghava = models.IntegerField(default=0)
    # felezat = models.IntegerField(default=0)
    # ahan_sangin = models.IntegerField(default=0)
    # ahan_sabok = models.IntegerField(default=0)
    # zayeat_elecronic = models.IntegerField(default=0)

    coins = models.IntegerField(default=0)
    bag = models.IntegerField(default=0)
    money = models.IntegerField(default=0)

    pelak_melak = models.TextField(blank=True)
    give_back_type = models.CharField(max_length=20 , default="")
    order_status = models.CharField(max_length=20 , default="not confirmed")

    date_created = models.DateTimeField(auto_now_add = True)
    data_done = models.DateTimeField(auto_now_add = True)



class Khanevar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True)
    is_email_confirmed = models.BooleanField(default=False)
    is_number_confirmed = models.BooleanField(default=False)
    location = models.TextField(blank=True)
    code = models.IntegerField(default=0)
    code_time = models.DateTimeField(default=timezone.now )




class Edari(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,blank=True)
    coins = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True)
    is_email_confirmed = models.BooleanField(default=False)
    is_number_confirmed = models.BooleanField(default=False)
    location = models.TextField(blank=True)
    code = models.IntegerField(default=0)
    code_time = models.DateTimeField(default=timezone.now)




class Tegari(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,blank=True)
    coins = models.PositiveIntegerField(default=0)
    phone_number = models.CharField(max_length=20, blank=True)
    is_email_confirmed = models.BooleanField(default=False)
    is_number_confirmed = models.BooleanField(default=False)
    location = models.TextField(blank=True)
    code = models.IntegerField(default=0)
    code_time = models.DateTimeField(default=timezone.now )
