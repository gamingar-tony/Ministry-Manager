from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name = 'home'),
    path('my-schedule/', views.my_schedule, name = 'my_schedule'),
    path('register/', views.register_view, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('schedule/', views.schedule_view, name = 'schedule'),
]