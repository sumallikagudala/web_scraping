from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.all_scrping_data, name='scraping'),
    path('get_time/', views.get_time, name='get_time')
]