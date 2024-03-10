from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index,name='index'),
    path('graph/', views.graph,name='graph'),
    path('login/', views.loginn,name='login'),
    #path('data_view/', views.data_view,name='data_view'),
   
]
