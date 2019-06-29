from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *

class traderViewGet(APIView):

    def post(self, request):
        # try:
            response = Response()

            roomId = self.request.data['roomId']
            traderId = self.request.data['traderId']
            strategyId = self.request.data['strategyId']

            traders = TraderParticapation.objects.filter(traderId=traderId,strategyId=strategyId,roomId=roomId)
            tradersJson = TraderParticapationSerializer(traders, many=True).data
            for trader in tradersJson:
                trader['mean'] = float("%.2f" % trader['mean'])
                trader['std'] = float("%.2f" % trader['std'])
                trader['expectancy'] = float("%.2f" % trader['expectancy'])
                trader['maxDD'] = float("%.2f" % trader['maxDD'])
                trader['sharpe'] = float("%.2f" % trader['sharpe'])
                trader['sortino'] = float("%.2f" % trader['sortino'])
                trader['predicted_return'] = float("%.2f" % trader['predicted_return'])
                trader['odds_of_win'] = "1:" + str(float("%.2f" % trader['odds_of_win']))

            response.data = {
                "data": tradersJson,
                "failedReason": None,
                "success": True
            }
            return response

        # except Exception:
        #     response = Response()
        #     response.data = {
        #         "failedReason": "Request failed",
        #         "success": False
        #     }
        #     return response
