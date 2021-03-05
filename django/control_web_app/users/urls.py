from django.urls import path

from django.urls import path, include

from .views import register

app_name = 'users'
urlpatterns = [
    # root path for this django app is [devices]
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    # path('logout/', logout, name='logout')
]