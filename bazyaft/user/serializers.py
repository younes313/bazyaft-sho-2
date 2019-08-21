from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Khanevar , Edari , Tegari , Order, OrderHistory


coin_for_invite = 1


class GetFeedBackSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderHistory
        exclude = ("location_x", "location_y" , "pelak_melak", "order_status", "user", "driver", )

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        if instance.driver != None :
            drv = instance.driver.drivermodel
            data = {"two_first":drv.car_palette_two_first, "letter":drv.car_palette_letter, "three_last": drv.car_palette_three_last, "city_code":drv.car_palette_city_code  }
            representation['pelak'] = data
        else:
            representation['pelak'] = ""
        return representation




class GetUserInfoSerializer(serializers.Serializer):

    class Meta:
        model = User

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        representation['username'] = instance.username

        if hasattr(instance , 'khanevar'):
            representation['phone_number'] = instance.khanevar.phone_number
            representation['coins'] = instance.khanevar.coins
            representation['order_history'] = len(OrderHistory.objects.filter(user = instance))
            representation['order_in_progress'] = len(Order.objects.filter(user = instance))
            representation['location'] = instance.khanevar.location
            representation['email'] = instance.email

        if hasattr(instance , 'edari'):
            representation['phone_number'] = instance.edari.phone_number
            representation['coins'] = instance.edari.coins
            representation['order_history'] = len(OrderHistory.objects.filter(user = instance))
            representation['order_in_progress'] = len(Order.objects.filter(user = instance))
            representation['location'] = instance.edari.location
            representation['type'] = instance.edari.type

        if hasattr(instance , 'tegari'):
            representation['phone_number'] = instance.tegari.phone_number
            representation['coins'] = instance.tegari.coins
            representation['order_history'] = len(OrderHistory.objects.filter(user = instance))
            representation['order_in_progress'] = len(Order.objects.filter(user = instance))
            representation['location'] = instance.tegari.location
            representation['type'] = instance.tegari.type


        return representation



class UserEditSerializer(serializers.Serializer):
    username = serializers.CharField(default="" , allow_blank=True)
    password = serializers.CharField(default="" ,allow_blank=True)
    email = serializers.CharField(default="" ,allow_blank=True)
    first_name = serializers.CharField(default="" , allow_blank=True)
    last_name = serializers.CharField(default="" , allow_blank=True)
    phone_number = serializers.CharField(default="" , allow_blank=True)
    location = serializers.CharField(default="" ,allow_blank=True)
    type = serializers.CharField(default="", allow_blank=True)



class GetTokenPhonenumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)


class GetTokenUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    password = serializers.CharField(max_length=256)

class GetTokenEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=256)


class GetTokenPhoneSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    code = serializers.IntegerField()

class UserKhanevarSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):

        return User.objects.create_user( **validated_data)

    def validate(self, data):
        email = data.get("email")

        if len(User.objects.filter(email=email)) > 0:
            raise ValidationError("102")
        # if not email or email=='':
        #     raise ValidationError("105")

        return data


class UserEdariTegariSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):

        return User.objects.create_user( **validated_data)

    def validate(self, data):
        email = data.get("email")

        if len(User.objects.filter(email=email)) > 0:
            raise ValidationError("102")

        return data




class KhanevarEmailRegisterSerializer(serializers.ModelSerializer):
    user = UserKhanevarSerializer()
    moaref_code = serializers.CharField(default='', allow_blank=True)

    class Meta:
        model = Khanevar
        fields = '__all__'

    def validate_phone_number(self, value):
        if value != "":
            if Khanevar.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
            if Edari.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
            if Tegari.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
        return value

    def validate_moaref_code(self, value):
        try:
            if value != '':
                User.objects.get(username=value)
        except:
            raise ValidationError('190')
        return value

    def create(self, validated_data):

        moaref = validated_data.pop('moaref_code')
        if moaref != '':
            usmo = User.objects.get(username=moaref)
            print(5)
            if hasattr(usmo, "khanevar"):
                usmo.khanevar.coins += coin_for_invite
                usmo.khanevar.save()
            elif hasattr(usmo, "edari"):
                usmo.edari.coins += coin_for_invite
                usmo.edari.save()
                print(6)
            elif hasattr(usmo, "tegari"):
                usmo.tegari.coins += coin_for_invite
                usmo.tegari.save()

        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        khanevar = Khanevar.objects.create(user=user,**validated_data)

        return khanevar



class EdariEmailRegisterSerializer(serializers.ModelSerializer):
    user = UserEdariTegariSerializer()
    moaref_code = serializers.CharField(default='', allow_blank=True)
    class Meta:
        model = Edari
        fields = '__all__'

    def validate_phone_number(self, value):
        if value != "":
            if Khanevar.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
            if Edari.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
            if Tegari.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
        return value

    def validate_moaref_code(self, value):
        try:
            if value != '':
                User.objects.get(username=value)
        except:
            raise ValidationError('190')
        return value


    def create(self, validated_data):
        moaref = validated_data.pop('moaref_code')
        if moaref != '':
            usmo = User.objects.get(username=moaref)
            print(5)
            if hasattr(usmo, "khanevar"):
                usmo.khanevar.coins += coin_for_invite
                usmo.khanevar.save()
            elif hasattr(usmo, "edari"):
                usmo.edari.coins += coin_for_invite
                usmo.edari.save()
                print(6)
            elif hasattr(usmo, "tegari"):
                usmo.tegari.coins += coin_for_invite
                usmo.tegari.save()


        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)

        edari = Edari.objects.create(user=user, **validated_data)
        return edari


class TegariEmailRegisterSerializer(serializers.ModelSerializer):
    user = UserEdariTegariSerializer()
    moaref_code = serializers.CharField(default='', allow_blank=True)
    class Meta:
        model = Tegari
        fields = '__all__'


    def validate_phone_number(self, value):
        if value != "":
            if Khanevar.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
            if Edari.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
            if Tegari.objects.filter(phone_number=value).exists():
                raise ValidationError("120")
        return value

    def validate_moaref_code(self, value):
        try:
            if value != '':
                User.objects.get(username=value)
        except:
            raise ValidationError('190')
        return value

    def create(self, validated_data):
        moaref = validated_data.pop('moaref_code')
        if moaref != '':
            usmo = User.objects.get(username=moaref)
            print(5)
            if hasattr(usmo, "khanevar"):
                usmo.khanevar.coins += coin_for_invite
                usmo.khanevar.save()
            elif hasattr(usmo, "edari"):
                usmo.edari.coins += coin_for_invite
                usmo.edari.save()
                print(6)
            elif hasattr(usmo, "tegari"):
                usmo.tegari.coins += coin_for_invite
                usmo.tegari.save()


        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)

        tegari = Tegari.objects.create(user=user, **validated_data)
        return tegari


class OrderSerializer(serializers.Serializer):
    # user = serializers.HiddenField( default=serializers.CurrentUserDefault() )
    # user = UserKhanevarSerializer()
    location_x = serializers.FloatField(default=0)
    location_y = serializers.FloatField(default=0)

    alminium = serializers.IntegerField(default=0)
    pet = serializers.IntegerField(default=0)
    khoshk = serializers.IntegerField(default=0)
    daftar_ketab = serializers.IntegerField(default=0)
    shishe = serializers.IntegerField(default=0)
    parche = serializers.IntegerField(default=0)
    naan = serializers.IntegerField(default=0)
    sayer = serializers.IntegerField(default=0)

    # kaghaz_moghava = serializers.IntegerField(default=0)
    # felezat = serializers.IntegerField(default=0)
    # ahan_sangin = serializers.IntegerField(default=0)
    # ahan_sabok = serializers.IntegerField(default=0)
    # zayeat_elecronic = serializers.IntegerField(default=0)

    # coins = serializers.IntegerField(default=0)
    # bag = serializers.IntegerField(default=0)
    # money = serializers.IntegerField(default=0)

    pelak_melak = serializers.CharField(default="")
    give_back_type =serializers.CharField(default="")


class OrderDriverSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = "__all__"


    def get_phone_number(self, obj):
        if hasattr(obj.user , 'khanevar'):
            return obj.user.khanevar.phone_number
        if hasattr(obj.user , 'edari'):
            return obj.user.edari.phone_number
        if hasattr(obj.user , 'tegari'):
            return obj.user.tegari.phone_number

    def to_representation(self, instance):

        representation = super().to_representation(instance)

        if instance.driver != None :
            drv = instance.driver.drivermodel
            data = {"two_first":drv.car_palette_two_first, "letter":drv.car_palette_letter, "three_last": drv.car_palette_three_last, "city_code":drv.car_palette_city_code  }
            representation['driver_phone_number'] = drv.phone_number
            representation['pelak'] = data
        else:
            representation['pelak'] = ""
            representation['driver_phone_number'] = ""
        return representation
