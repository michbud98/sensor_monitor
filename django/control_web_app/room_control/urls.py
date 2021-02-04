from django.urls import path

from .views import room_list_view, room_create_view

urlpatterns = [
    # root path for this django app is [rooms]
    path('', room_list_view, name='room_list'),
    path('room_create', room_create_view, name='room_create'),
    
]