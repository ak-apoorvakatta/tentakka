from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rooms.models import Rooms
from traderParticipation.models import TraderParticapation
from traderParticipation.serializers import TraderParticapationSerializer
from users.models import Users
from users.serializers import UsersFilteredSerializer
from .models import *
from .serializers import *

# Create your views here.

def updateOdds(traderJson):

   data = traderJson['traders']
   margin = 5

   totalBet = 0
   for i in range(len(data)):
       totalBet += data[i]['bets']

   newOdds = []
   for i in range(len(data)):

       tmpProb = 1/data[i]['odds']
       avgBet = data[i]['bets']/totalBet
       newProb = (tmpProb + avgBet)/2

       newOdds.append(1/newProb)

   updatedJson = {}
   updatedJson['traders'] = []
   for i in range(len(newOdds)):
       updatedJson['traders'].append({"bets": data[i]['bets'], "odds": newOdds[i], "id": data[i]['id']})

   return updatedJson

class userParticipationViewInvest(APIView):

    def post(self, request):
        # try:
            response = Response()

            inputUsername = self.request.data['username']
            inputTraderId = self.request.data['traderId']
            inputStrategyId = self.request.data['strategyId']
            inputRoomId = self.request.data['roomId']
            inputAmount = self.request.data['amount']

            userParticipationCheck = UserParticapation.objects.filter(userUsername=inputUsername, roomId=inputRoomId)
            if userParticipationCheck.count() > 0:
                response.data = {
                    "data": None,
                    # "failedReason": "Already invested in",
                    # "success": False
                    "failedReason": None,
                    "success": True
                }
                return response

            user = Users.objects.filter(username=inputUsername)
            userJSON = UsersFilteredSerializer(user, many=True).data

            for u in userJSON:
                if float(u['token']) < inputAmount:
                    response.data = {
                        "data": None,
                        "failedReason": "Not enough balance",
                        "success": False
                    }
                    return response

            Users.objects.update_or_create(
                username=inputUsername,
                defaults={'token': float(u['token']) - inputAmount},
            )

            userParticipation = {
                "userUsername": inputUsername,
                "traderId": inputTraderId,
                "strategyId": inputStrategyId,
                "roomId": inputRoomId,
                "investment": inputAmount
            }

            serializer = UserParticapationSerializer(data=userParticipation)
            if serializer.is_valid(raise_exception=True):
                savedUser = serializer.save()



            traders = TraderParticapation.objects.filter(roomId=inputRoomId)
            tradersJSON = TraderParticapationSerializer(traders, many=True).data

            toBePassedObject = {}
            list = []
            for t in tradersJSON:
                betSum = 0.0
                users11 = UserParticapation.objects.filter(roomId=inputRoomId, traderId=t['traderId'], strategyId=t['strategyId'])
                usersJSON11 = UserParticapationSerializer(users11, many=True).data

                for uu in usersJSON11:
                    betSum = betSum + float(uu['investment'])

                obj = {
                    "id": t['traderId'] + "@" + t['strategyId'],
                    "bets": betSum,
                    "odds": t['odds_of_win']
                }
                list.append(obj)
            toBePassedObject['traders'] = list

            updatedOdds = updateOdds(toBePassedObject)

            print(updatedOdds)

            for newOdds in updatedOdds['traders']:
                TraderParticapation.objects.update_or_create(
                    roomId=inputRoomId, traderId=newOdds['id'].split('@')[0], strategyId=newOdds['id'].split('@')[1],
                    defaults={'odds_of_win': newOdds['odds']},
                )


            response.data = {
                "data": userParticipation,
                "failedReason": None,
                "success": True
            }
            return response

        # except Exception as error:
        #     print(error)
        #     response = Response()
        #     response.data = {
        #         "failedReason": "Request failed",
        #         "success": False
        #     }
        #     return response
