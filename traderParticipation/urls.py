from django.urls import path
from .views import *

urlpatterns = [
    path('trader/getTrader', traderViewGet.as_view(), name="get-trader"),
]
