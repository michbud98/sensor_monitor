"""control_web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from main_menu.views import home_view
from basic_values.views import basic_values_view
from room_control.views import sensor_list_view, sensor_create_view, sensor_remove_view, sensor_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('basic_values/', basic_values_view, name='basic_values'),
    path('sensor_list/', sensor_list_view, name='sensor_list'),
    path('sensor_create/<str:sensor_id>', sensor_create_view, name='sensor_create'), # TODO find how to remove this unnecessary url route
    path('sensor_create/<str:sensor_id>/<str:hostname>', sensor_create_view, name='sensor_create'),
    path('sensor_remove/<str:sensor_id>', sensor_remove_view, name='sensor_remove'),
    path('sensor_detail/<str:sensor_id>', sensor_detail_view, name='sensor_detail'),
]
