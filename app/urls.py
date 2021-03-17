from django.contrib import admin
from django.urls import path
from . import views
import django.views.decorators.csrf

urlpatterns = [
    path('login/', views.login),
    path('authenticate/', views.authenticate),
    path('attendance/course/<int:course_id>/session/<int:session_id>/', views.get_attendance),
    path('attendance/faculty/course/<int:course_id>/session/<int:session_id>/', views.get_faculty_attendance),
    #path('sign-up/', views.sign_up),
    path('sessions/', views.sessions),
    path('profile/', views.profile),
]
