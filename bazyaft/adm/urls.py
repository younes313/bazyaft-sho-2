from django.urls import path


from . import views

app_name = 'adm'

urlpatterns = [
    # path('GetImage', views.GetImage.as_view() , name='GetImage'),



    path('DriverHasUpdate', views.DriverHasUpdate.as_view() , name='DriverHasUpdate'),
    path('UserHasUpdate', views.UserHasUpdate.as_view() , name='UserHasUpdate'),
    path('GetImage', views.GetImage.as_view() , name='GetImage'),

    path('ItemCreate', views.ItemCreate.as_view() , name='ItemCreate'),

    path('ItemsList', views.ItemsList.as_view() , name='ItemsList'),


]
