from django.urls import path
from .views import *

urlpatterns = [
    path('user/invest', userParticipationViewInvest.as_view(), name="user-invest"),
]
