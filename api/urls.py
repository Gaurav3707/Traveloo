
from django.urls import path
from .views import *

app_name = 'api'

urlpatterns = [
    #Auth
    path('auth/user/signup/', UserSignUpView.as_view(), name='user-sign-up'),
]