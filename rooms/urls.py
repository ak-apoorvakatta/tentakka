from django.urls import path
from .views import *

urlpatterns = [
    path('room/setActiveRooms', roomViewSetActiveRooms.as_view(), name="get-active-rooms"),
    path('room/getActiveRooms', roomViewGetActiveRooms.as_view(), name="get-active-rooms"),
    path('room/getInActiveRooms', roomViewGetInActiveRooms.as_view(), name="get-in-active-rooms"),
    path('room/getTargetRoom', roomViewGetTargetRoom.as_view(), name="get-target-rooms"),
    path('room/getTargetRoomWithTraderData', roomViewGetTargetRoomWithTraderData.as_view(), name="get-target-rooms-with-trader-data"),
]
