from rest_framework import serializers

from .models import Items, FeedBack



class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = ['id','name','name_farsi']

#
# class FeedBackSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = FeedBack
#         fields = []
