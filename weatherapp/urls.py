from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('delete/<int:item>/', views.delete_city, name = 'delete'),
]