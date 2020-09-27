from django.urls import path

from . import views

app_name = 'tweet_template'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('explore/', views.explore, name='explore'),
    path('<int:pk>/delete/', views.delete_template, name='t_delete'),
]
