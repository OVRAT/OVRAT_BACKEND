from django.urls import path
from .views import *

urlpatterns = [
    path('register_user_daniel', register_user_daniel),
    path("api_home", api_home),
    path("update_profile/", update_profile),
    path("change_password/", change_password),
    path("reset_password_get_token/", reset_password_get_token),
    path("reset_password_confirm/<uidb64>/<token>/", reset_password_confirm),
    path('users/', user_list, name='user-list'),
    path('categories/', category_list, name='category-list'),
    path('courses/', course_list, name='course-list'),
    path('courses/<int:pk>/', course_detail, name='course-detail'),
    path('lessons/', lesson_list, name='lesson-list'),
    path('lessons/<int:pk>/', lesson_detail, name='lesson-detail'),
    path('quizzes/', quiz_list, name='quiz-list'),
    path('quizzes/<int:pk>/', quiz_detail, name='quiz-detail'),
    path('questions/', question_list, name='question-list'),
    path('questions/<int:pk>/', question_detail, name='question-detail'),
    path('enrollments/', enrollment_list, name='enrollment-list'),
    path('enrollments/<int:pk>/', enrollment_detail, name='enrollment-detail'),
]
