from rest_framework import serializers
# from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
# from user.models import Khanevar , Edari , Tegari , Order

from user.models import Order , OrderHistory


class GetDriverInfoSerializer(serializers.Serializer):

    class Meta:
        model = User

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        representation['fullname'] = instance.get_full_name()

        if hasattr(instance , 'drivermodel'):
            representation['phone_number'] = instance.drivermodel.phone_number
            representation['coins'] = instance.drivermodel.coins
            representation['order_history'] = len(OrderHistory.objects.filter(driver = instance))
            representation['order_in_progress'] = len(Order.objects.filter(driver = instance))
            representation["driver_score"] = instance.drivermodel.calculate_driverscore()

        return representation





class HistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderHistory
        fields = "__all__"

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        if instance.driver != None :
            drv = instance.driver.drivermodel
            data = {"two_first":drv.car_palette_two_first, "letter":drv.car_palette_letter, "three_last": drv.car_palette_three_last, "city_code":drv.car_palette_city_code  }
            representation['pelak'] = data
        else:
            representation['pelak'] = ""
        return representation



class OrderHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"



class ConfirmOrEditOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    status_driver = serializers.CharField(default="")
    alminium = serializers.IntegerField(default=0)
    pet = serializers.IntegerField(default=0)
    khoshk = serializers.IntegerField(default=0)
    daftar_ketab = serializers.IntegerField(default=0)
    shishe = serializers.IntegerField(default=0)
    parche = serializers.IntegerField(default=0)
    naan = serializers.IntegerField(default=0)
    sayer = serializers.IntegerField(default=0)
