from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name = 'home'),
    path('my-schedule/', views.my_schedule, name = 'my_schedule'),
    path('register/', views.register_view, name = 'register'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('schedule/', views.schedule_view, name = 'schedule'),
    path('open-positions/', views.open_positions, name = 'open_positions'),
    path('profile/', views.profile_view, name = 'profile'),
    path('admin/roles/', views.manage_roles, name = 'manage_roles'),
    path('settings/', views.settings_view, name = 'settings'),
    path('homily-import/', views.homily_import_view, name = 'homily_import'),
]