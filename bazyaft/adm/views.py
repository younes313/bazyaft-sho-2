from django.shortcuts import render
from rest_framework.generics import ListAPIView ,CreateAPIView
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes



# Create your views here.

from .serializers import ItemsSerializer
from .models import Items


@permission_classes((AllowAny,))
class ReInitializeItems(APIView):

    def post(self, request, format=None):
        Items.objects.all().delete()

        Items.objects.create(name="alminium", name_farsi="آلومینیوم")
        Items.objects.create(name="pet", name_farsi="پلاستیک")
        Items.objects.create(name="khoshk", name_farsi="خشک")
        Items.objects.create(name="daftar_ketab", name_farsi="دفتر و کتاب")
        Items.objects.create(name="shishe", name_farsi="شیشه")
        Items.objects.create(name="parche", name_farsi="پارچه")
        Items.objects.create(name="naan", name_farsi="نان")
        Items.objects.create(name="sayer", name_farsi="سایر")


@permission_classes((AllowAny,))
class DriverHasUpdate(APIView):
    last_version = '1.1'
    is_forced = False
    def post(self, request, format=None):
        try:
            version = request.data['version']
        except:
            return Response({'status':False, 'error':"170"}, status=status.HTTP_200_OK)  #incorrect input

        if version == self.last_version:
            return Response({'status':True, 'need_update':False}, status=status.HTTP_200_OK)
        else:
            return Response({'status':True, 'need_update':True, 'is_forced':self.is_forced}, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class UserHasUpdate(APIView):
    last_version = '1.1'
    is_forced = False
    def post(self, request, format=None):
        try:
            version = request.data['version']
        except:
            return Response({'status':False, 'error':"170"}, status=status.HTTP_200_OK)  #incorrect input

        if version == self.last_version:
            return Response({'status':True, 'need_update':False}, status=status.HTTP_200_OK)
        else:
            return Response({'status':True, 'need_update':True, 'is_forced':self.is_forced}, status=status.HTTP_200_OK)


@permission_classes((AllowAny,))
class GetImage(APIView):

    def get(self, request, format=None):
        id = request.data['id']
        try:
            item = Items.objects.get(id=id)
            return HttpResponse(item.image, content_type="image/png")
        except:
            return Response({"status":False}, status=status.HTTP_201_CREATED)


class ItemsList(ListAPIView):

    serializer_class = ItemsSerializer
    permission_classes = (AllowAny,)
    queryset = Items.objects.all()



class ItemCreate(CreateAPIView):


    serializer_class = ItemsSerializer
    permission_classes = (AllowAny,)

    def post(self, request):

        serializer = ItemsSerializer(data=request.data)
        if serializer.is_valid():

            # Save request image in the database
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
