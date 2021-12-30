from django.urls import path
from . import views

app_name = 'simba_app'

urlpatterns = [
    path('', views.index, name='index')
]