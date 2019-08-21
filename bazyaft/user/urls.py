from django.urls import path
from rest_framework.authtoken import views as views2

from . import views

app_name = 'user'

urlpatterns = [
    # path('GetOrder', views.GetOrder.as_view() , name='GetOrder'),


    path('GetFeedBack', views.GetFeedBack.as_view() , name='GetFeedBack'),
    path('GetUserInfo', views.GetUserInfo.as_view() , name='GetUserInfo'),
    path('CodeStatus', views.CodeStatus.as_view() , name='CodeStatus'),
    path('History', views.History.as_view() , name='History'),
    path('EditUser', views.EditUser.as_view() , name='EditUser'),
    path('GetMyInProgresOrder', views.GetMyInProgresOrder.as_view() , name='GetMyInProgresOrder'),
    path('CancelOrder', views.CancelOrder.as_view() , name='CancelOrder'),
    path('ConfirmOrCancel', views.ConfirmOrCancel.as_view() , name='ConfirmOrCancel'),
    path('GetOrder', views.GetOrder.as_view() , name='GetOrder'),
    path('GetTokenPhonenumber', views.GetTokenPhonenumber.as_view() , name='GetTokenPhonenumber'),
    path('UserLogout', views.UserLogout.as_view() , name='UserLogout'),
    path('GetMyCoins', views.GetMyCoins.as_view() , name='GetMyCoins'),
    path('GetTokenPhone', views.GetTokenPhone.as_view() , name='GetTokenPhone'),
    path('get-token' , views.GetTokenUsername.as_view() , name = "GetTokenUsername" ) ,
    path('get-token-email', views.GetTokenEmail.as_view() , name='GetTokenEmail'),
    path('TegariEmailRegister', views.TegariEmailRegister.as_view() , name='TegariEmailRegister'),
    path('EdariEmailRegister', views.EdariEmailRegister.as_view() , name='EdariEmailRegister'),
    path('KhanevarEmailRegister', views.KhanevarEmailRegister.as_view(), name='KhanevarEmailRegister'),
]
