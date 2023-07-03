from django.urls import path
from .views import *

urlpatterns = [
    path('register_user_daniel', register_user_daniel),
    path("api_home", api_home,)
]
