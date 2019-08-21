from django import forms
from driver.models import DriverModel
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    class Meta():
        model = User
        fields = [ 'first_name' , 'last_name' ,]


class DriverSignupForm(forms.ModelForm):

    class Meta():
        model = DriverModel
        fields = [
            "national_code",
            "phone_number",
            "car_certificate_number",
            "car_name",
            "car_palette_two_first",
            "car_palette_letter",
            "car_palette_three_last",
            "car_palette_city_code",
            "profile_pic",

        ]
