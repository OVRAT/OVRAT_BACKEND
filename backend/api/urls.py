from django.urls import path
from .views import *

urlpatterns = [
    path('register_user_daniel', register_user_daniel),
    path("api_home", api_home),
    path("update_profile/", update_profile),
    path("change_password/", change_password),
    path("reset_password_get_token/", reset_password_get_token),
    path("reset_password_confirm/<uidb64>/<token>/", reset_password_confirm)
]
