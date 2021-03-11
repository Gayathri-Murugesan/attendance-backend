from django.contrib import admin
from django.urls import path
from . import views
import django.views.decorators.csrf

urlpatterns = [
    path('login/', views.login),
    path('authenticate/', views.authenticate),
    path('attendance/<int:session_id>/<int:course_id>/', views.get_attendance),
    #path('sign-up/', views.sign_up),
    path('sessions/', views.sessions),
    path('profile/', views.profile),
]
