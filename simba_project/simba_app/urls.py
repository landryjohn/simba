from django.urls import path
from django.urls import include
from . import views

app_name = 'simba_app'

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', views.index, name='index'),
    path('home/', views.dashboard, name='home'),
]