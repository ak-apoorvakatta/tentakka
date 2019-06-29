from django.urls import path
from .views import *

urlpatterns = [
    path('session/setup', tradingSessionViewSetup.as_view(), name="trading-session-set-up"),
    path('session/getData', tradingSessionViewGetData.as_view(), name="trading-session-get-data"),
    path('session/close', tradingSessionViewClose.as_view(), name="trading-session-close"),
]
