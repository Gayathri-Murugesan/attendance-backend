from django.contrib import admin
from django.urls import path
from . import views
import django.views.decorators.csrf

urlpatterns = [
    path('login/', views.login),
    path('authenticate/', views.authenticate),
    #path('sign-up/', views.sign_up),
    #path('student-home/', views.student_view),
    #path('profile/<str:role>/<int:id>/', views.profile),
]
