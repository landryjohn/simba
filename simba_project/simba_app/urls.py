from django.urls import path
from django.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'simba_app'

urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', views.index, name='index'),
    path('home/', views.dashboard, name='home'),
    path('users/', views.users, name='users'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/users/', views.get_users)
]

urlpatterns = format_suffix_patterns(urlpatterns)