from django.urls import path
from . import views

urlpatterns = [
    path('', views.writers_dashboard, name='index'),
]