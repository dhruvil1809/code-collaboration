from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('verify-email', views.verify_email, name='verify_email'),
    path('reset-password/<str:email>', views.reset_password, name='reset_password'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_view, name='logout'),
]

