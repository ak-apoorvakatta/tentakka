from django.urls import path
from .views import userViewGet, userViewLogin, userViewRegister

urlpatterns = [
    path('user/get', userViewGet.as_view(), name="user-get"),
    path('user/login', userViewLogin.as_view(), name="user-login"),
    path('user/register', userViewRegister.as_view(), name="user-register")
]
