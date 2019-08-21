from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout
# ####################
from .forms import DriverSignupForm , UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from random import randint
######################
from .serializers import *
from user.models import Order , OrderHistory
from user.serializers import OrderSerializer
from user.serializers import OrderDriverSerializer
from user.views import send_sms
from .models import DriverModel



@permission_classes((permissions.IsAuthenticated,))
class GetDriverInfo(APIView):

    def get(self, request, format=None):
        serializer = GetDriverInfoSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((permissions.IsAuthenticated,))
class History(APIView):

    def get(self, request, format=None):
        serializer = HistorySerializer(OrderHistory.objects.filter(driver=request.user) , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes((permissions.AllowAny,))
class GetToken(APIView):
    def LessThanOneMinute(self, now, generated_time):
        # if generated_time.year == now.year and generated_time.month == now.month and generated_time.day == now.day and generated_time.hour == now.hour:
        #     if generated_time.minute == now.minute:
        #         return True
        #     elif (now.minute - generated_time.minute) == 1  and  (now.second < generated_time.second):
        #         return True
        # return False
        if generated_time.year == now.year and generated_time.month == now.month and generated_time.day == now.day and generated_time.hour == now.hour:
            if  now.minute - generated_time.minute < 5:
                return True
            elif (now.minute - generated_time.minute) == 1  and  (now.second < generated_time.second):
                return True
        return False

    def post(self, request, format=None):
        try:
            phone_number = request.data['phone_number']
            code = request.data['code']
        except:
            dic = { "status":False , "error" : "170"  }
            return Response(dic, status = status.HTTP_200_OK) #incorrect input

        try:
            driver = DriverModel.objects.get(phone_number=phone_number )
            if self.LessThanOneMinute(timezone.now() , driver.code_time ):

                if driver.code == int(code):
                    token , _ = Token.objects.get_or_create(user=driver.user)
                    return Response({"status":True, "token":token.key})
            else:
                return Response( {"status":False , "error" : "140"} , status = status.HTTP_200_OK)  #code is expired
        except:
            pass
        return Response ( {"status":False , "error" : "700"} , status = status.HTTP_200_OK) # wrong number or code





@permission_classes((permissions.AllowAny,))
class GetCode(APIView):

    def post(self, request, format=None):
        try:
            username = request.data['phone_number']
            password = request.data['national_code']
        except:
            dic = { "status":False , "error" : "170"  }
            return Response(dic, status = status.HTTP_200_OK) #incorrect input

        user = authenticate(request=request, username=username, password=password)
        if not (user and hasattr(user, 'drivermodel') ):
            dic = { "status":False , "error" : "171"    }   # incorrect phone_number or national_code
            return Response(dic, status = status.HTTP_200_OK)

        #generate and send code
        code = randint(100000 , 999999)
        user.drivermodel.code = code
        user.drivermodel.code_time = timezone.now()
        send_sms(user.drivermodel.phone_number, code)
        user.drivermodel.save()

        # token , _ = Token.objects.get_or_create(user=user)
        return Response({"status":True, "code":code, }, status=status.HTTP_200_OK)




###############################
def index(request):
    return render(request,'driver/index.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def special(request):
    return HttpResponse("You are logged in !")

@login_required
@user_passes_test(lambda u: u.is_superuser)
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
@user_passes_test(lambda u: u.is_superuser)
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = DriverSignupForm(data=request.POST)
        if profile_form.is_valid() and user_form.is_valid() :
            user = user_form.save(commit=False)
            user.username = profile_form.cleaned_data['phone_number']
            user.set_password(profile_form.cleaned_data['national_code'])
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = DriverSignupForm()
    return render(request,'driver/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active and user.is_superuser:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Only superuser can login")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'driver/login.html', {})


###############################3

class ConfirmOrEditOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = ConfirmOrEditOrderSerializer(data=request.data)

        if serializer.is_valid():
            # try:
            data = serializer.data
            order = Order.objects.get(id = data['order_id'] )
            if serializer.data['status_driver'] == 'edit':
                data.pop('status_driver' , None)
                data.pop('order_id', None)
                if data['alminium'] != 0 :
                        order.alminium = data['alminium']
                if data['pet'] != 0 :
                        order.alminium = data['pet']
                if data['khoshk'] != 0 :
                        order.alminium = data['khoshk']
                if data['daftar_ketab'] != 0 :
                        order.alminium = data['daftar_ketab']
                if data['shishe'] != 0 :
                        order.alminium = data['shishe']
                if data['parche'] != 0 :
                        order.alminium = data['parche']
                if data['naan'] != 0 :
                        order.alminium = data['naan']
                if data['sayer'] != 0 :
                        order.alminium = data['sayer']
                order.save()
            # order = order[0]
            dic = {"status":True}
            # dic.update(serializer.data)
            if hasattr(order.user , "khanevar"):
                coins = order.calculate_coins()
                total_coins = order.user.khanevar.coins + coins
                order.coins = coins
                if order.give_back_type == "coin":
                    order.save()
                    order.user.khanevar.coins += coins
                    order.user.khanevar.save()
                    dic.update({"coins": order.coins})
                elif order.give_back_type == "bag":
                    order.bag = total_coins // 10
                    order.save()
                    order.user.khanevar.coins = total_coins - order.bag * 10
                    order.user.khanevar.save()
                    dic.update({"coins": order.coins})
                    dic.update({"bag": order.bag})

            elif hasattr(order.user , "edari"):
                print(1)
                if order.give_back_type == "money":
                    print(2)
                    order.money = order.calculate_money()
                    order.save()
                    dic.update({"money": order.money})

            elif hasattr(order.user , "tegari"):
                print(1)
                if order.give_back_type == "money":
                    print(2)
                    order.money = order.calculate_money()
                    order.save()
                    dic.update({"money": order.money})

            order.order_status = "done"
            order.save()

            order.driver.drivermodel.coins += order.calculate_sum()
            order.driver.drivermodel.save()

            ser = OrderHistorySerializer(order)
            ser = ser.data
            usr = User.objects.get(id=ser['user'])
            ser.pop("user" , None)
            drv = User.objects.get(id = ser['driver'])
            ser.pop("driver" , None)
            ser.pop("id" , None)


            his = OrderHistory.objects.create(user=usr, driver=drv, **ser)
            # Order.objects.get(id = his.id).delete()

            order.delete()

            return Response(dic, status=status.HTTP_200_OK)

            # except:
                # return Response({"status":False, "error":"165"}, status=status.HTTP_200_OK) # incorrect order_id
        else:
            return Response({"status":False, "error":"169"}, status=status.HTTP_200_OK) # order_id is required


class GetMyAcceptedOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = OrderDriverSerializer(Order.objects.filter(driver=request.user) , many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)


class AcceptOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        if len(Order.objects.filter(driver=request.user)) >= 20:
            return Response( {"status":False, "error":"167" }  ,status=status.HTTP_200_OK)
        try:
            id = request.data['id']
            try:
                order = Order.objects.get(id=id)
                order.driver = request.user
                order.order_status = "accepted"
                order.save()
                return Response( {"status":True, }  ,status=status.HTTP_200_OK)
            except:
                return Response( {"status":False, "error":"165" }  ,status=status.HTTP_200_OK)
        except:
            return Response( {"status":False, "error":"166" }  ,status=status.HTTP_200_OK)


class CancelOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # print (request.user.user)
        # try:
        id = request.data['id']
        # try:
        order = Order.objects.get(id=id)
        if request.user.drivermodel.coins > 5 :
            request.user.drivermodel.coins -= 5
        else:
            request.user.drivermodel.coins = 0
        request.user.drivermodel.save()
        order.driver = None
        order.order_status = "in queue"
        order.save()
        return Response( {"status":True, }  ,status=status.HTTP_200_OK)
        # except:
        return Response( {"status":False, "error":"165" }  ,status=status.HTTP_200_OK)
        # except:
        return Response( {"status":False, "error":"166" }  ,status=status.HTTP_200_OK)


class GetAllOrders (APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get(self, request, format=None):

        serializer = OrderDriverSerializer( Order.objects.filter(order_status="in queue") , many=True)
        # if serializer.is_valid():
        return Response(serializer.data , status=status.HTTP_200_OK)

        # else:
        return Response(serializer.errors  , status=status.HTTP_400_BAD_REQUEST)
