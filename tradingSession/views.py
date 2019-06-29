from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from users.models import Users
from .models import *
from .serializers import *
from traderParticipation.models import *
from userParticipation.models import *
from rooms.models import *
from traders.models import *
from traders.serializers import *
from traderParticipation.serializers import *
from userParticipation.serializers import *
from rooms.serializers import *
import calendar;
import time;

class tradingSessionViewSetup(APIView):

    def post(self, request):
        try:
            response = Response()

            roomId = self.request.data['roomId']
            endTimeCount = self.request.data['endTimeCount']

            Rooms.objects.update_or_create(
                id=roomId,
                defaults={'status': 2},
            )

            response.data = {
                "failedReason": None,
                "success": True
            }
            return response

        except Exception as error:
            print(error)
            response = Response()
            response.data = {
                "failedReason": "Request failed",
                "success": False
            }
            return response

class tradingSessionViewClose(APIView):

    def post(self, request):
        try:
            response = Response()

            roomId = self.request.data['roomId']
            endTimeCount = self.request.data['endTimeCount']

            Rooms.objects.update_or_create(
                id=roomId,
                defaults={'status': 3, 'active': 0},
            )

            traders = TraderParticapation.objects.filter(roomId=roomId)
            tradersJSON = TraderParticapationSerializer(traders, many=True).data
            for trader in tradersJSON:
                if trader['traderName'] == "Trader 1":
                    users11 = UserParticapation.objects.filter(roomId=roomId, traderId=trader['traderId'],strategyId=trader['strategyId'])
                    usersJSON11 = UserParticapationSerializer(users11, many=True).data

                    for uu in usersJSON11:
                        Users.objects.update_or_create(
                            username=uu['userUsername'],
                            defaults={'token': float(uu['token'])+trader['odds_for_win']*float(uu['investment'])},
                        )

            response.data = {
                "failedReason": None,
                "success": True
            }
            return response

        except Exception as error:
            print(error)
            response = Response()
            response.data = {
                "failedReason": "Request failed",
                "success": False
            }
            return response

class tradingSessionViewSetup(APIView):

    def post(self, request):
        try:
            response = Response()

            roomId = self.request.data['roomId']
            endTimeCount = self.request.data['endTimeCount']

            Rooms.objects.update_or_create(
                id=roomId,
                defaults={'status': 2},
            )

            tradingSessionJSON = {
                "roomId": roomId,
                "startTime": str(calendar.timegm(time.gmtime())),
                "endTime": str(calendar.timegm(time.gmtime())),
                "endTimeCount": endTimeCount,
            }
            serializer = TradingSessionSerializer(data=tradingSessionJSON)
            if serializer.is_valid(raise_exception=True):
                savedTradingSession = serializer.save()

            response.data = {
                "data": tradingSessionJSON,
                "failedReason": None,
                "success": True
            }
            return response

        except Exception as error:
            print(error)
            response = Response()
            response.data = {
                "failedReason": "Request failed",
                "success": False
            }
            return response

class tradingSessionViewGetData(APIView):

    def post(self, request):
        try:
            response = Response()
            #
            # roomId = self.request.data['roomId']
            #
            # session = TradingSession.objects.filter(roomId=roomId)
            # sessionJSON = TradingSessionSerializer(session, many=True).data
            # rangeLimit = 0
            # for s in sessionJSON:
            #     rangeLimit = s['endTimeCount']
            #
            # traders = TraderParticapation.objects.filter(roomId=roomId)
            # tradersJSON = TraderParticapationSerializer(traders, many=True).data
            #
            # trendList = {}
            # for trader in tradersJSON:
            #     trendListArray = []
            #     tradingRecord = Traders.objects.filter(traderid=trader['traderId'], strategyid=trader['strategyId'])
            #     tradingRecordJSON = TradersSerializer(tradingRecord, many=True).data
            #     for t in tradingRecordJSON:
            #         if t['dateindex'] <= rangeLimit:
            #             trendListArray.append(t)
            #     trendList[trader['id']]:
            #
            #
            # Rooms.objects.update_or_create(
            #     id=roomId,
            #     defaults={'status': 2},
            # )
            #
            # tradingSessionJSON = {
            #     "roomId": roomId,
            #     "startTime": str(calendar.timegm(time.gmtime())),
            #     "endTime": str(calendar.timegm(time.gmtime())),
            #     "endTimeCount": endTimeCount,
            # }
            # serializer = TradingSessionSerializer(data=tradingSessionJSON)
            # if serializer.is_valid(raise_exception=True):
            #     savedTradingSession = serializer.save()

            response.data = {
                # "data": tradingSessionJSON,
                "failedReason": None,
                "success": True
            }
            return response

        except Exception as error:
            print(error)
            response = Response()
            response.data = {
                "failedReason": "Request failed",
                "success": False
            }
            return response
