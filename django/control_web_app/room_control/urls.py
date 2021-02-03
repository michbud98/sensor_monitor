from django.urls import path

from .views import room_list_view

urlpatterns = [
    # root path for this django app is [rooms]
    path('', room_list_view, name='room_list'),
    
]