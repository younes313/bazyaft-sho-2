from django.urls import path
from rest_framework.authtoken import views as views2

from . import views

app_name = 'driver'

urlpatterns = [
    # path('GetOrder', views.GetOrder.as_view() , name='GetOrder'),


    path('GetDriverInfo', views.GetDriverInfo.as_view() , name='GetDriverInfo'),
    path('GetToken', views.GetToken.as_view() , name='GetToken'),
    path('GetCode', views.GetCode.as_view() , name='GetCode'),
    path('History', views.History.as_view() , name='History'),
    path('ConfirmOrEditOrder', views.ConfirmOrEditOrder.as_view() , name='ConfirmOrEditOrder'),
    path('user_login/', views.user_login , name='user_login'),
    path('register/', views.register , name='register'),
    path('GetMyAcceptedOrder', views.GetMyAcceptedOrder.as_view() , name='GetMyAcceptedOrder'),
    path('CancelOrder', views.CancelOrder.as_view() , name='CancelOrder'),
    path('AcceptOrder', views.AcceptOrder.as_view() , name='AcceptOrder'),
    path('GetAllOrders', views.GetAllOrders.as_view() , name='GetAllOrders'),
]
