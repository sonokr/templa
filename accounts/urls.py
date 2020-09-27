from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('adv/', views.account_delete_view, name='adelete'),
    path('settings/', views.settings, name='settings'),
    path('<str:sid>/', views.profile, name='profile'),
    path('abukuma/<int:pk>/', views.abukuma, name='abukuma'),    
]
