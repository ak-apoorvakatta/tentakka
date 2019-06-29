from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from userParticipation.models import *
from userParticipation.serializers import *
from traderParticipation.models import *
from traderParticipation.serializers import *
from traders.models import *
from traders.serializers import *
from .serializers import *
from metrics import generate_traders_for_room
import pandas as pd
import numpy as np
import uuid
import statsmodels.api as sm
from metrics import generate_metrics
from dbmanager import *
import datetime


def generate_tracks(name):
    return pd.DataFrame(np.cumprod(np.e ** (np.random.standard_t(3, 252 * 5) / 100)) * 100, columns=[name])


def init_train():
  train_traders = {}
  for j in range(0,2):
      id = str(uuid.uuid4())
      train_traders[id] = [generate_tracks("S{}".format(i)) for i in range(0,10)]

  metrics={}
  for k in train_traders.keys():
    tracks=pd.concat(train_traders[k], axis=1)
    print(k)

    for t in tracks.columns:
      metrics[k+'-'+t] = generate_metrics(tracks[[t]])
  #   metrics[k]={t: generate_metrics(tracks[t]) for t in tracks.columns}

  test_frame=pd.DataFrame(metrics).T

  y = test_frame[['mean']]
  X = test_frame[['expectancy', 'maxDD', 'sharpe']]
  model = sm.OLS(y, X).fit()
  predictions = model.predict(X) # make the predictions by the model

  # Print out the statistics
  return model.params.values.flatten().tolist()

coeff = init_train()

def generate_trader_strategy_metrics(coefficients):
    predicted_returns = []
    traders = select_all('public', 'trader_tracks').traderid.unique().tolist()
    for t in traders:
        t_tracks = select_where('public', 'trader_tracks', 'traderid', '=', t)
        strategies = t_tracks.strategyid.unique().tolist()
        for s in strategies:
            t_track = t_tracks.query('strategyid == @s', engine='python')[['dateindex', 'value']].set_index('dateindex')
            metrics_test = generate_metrics(t_track)
            y = [metrics_test['expectancy'], metrics_test['maxDD'], metrics_test['sharpe']]
            predicted_returns.append(
                {
                    'traderid': t,
                    'strategyid': s,
                    'strategy_metrics': metrics_test,
                    'predicted_return': [i*j for i,j in list(zip(coefficients, y))][0]
                })

    return predicted_returns

class roomViewGetTargetRoom(APIView):

    def post(self, request):
        try:

            response = Response()

            roomId = self.request.data['roomId']

            rooms = Rooms.objects.filter(id=roomId)
            roomsJSON = RoomsSerializer(rooms, many=True).data

            response.data = {
                "data": roomsJSON,
                "failedReason": None,
                "success": True
            }
            return response

        except Exception:
            response = Response()
            response.data = {
                "failedReason": "Request failed",
                "success": False
            }

class roomViewGetTargetRoomWithTraderData(APIView):

    def post(self, request):
        # try:

            response = Response()

            roomId = self.request.data['roomId']

            rooms = Rooms.objects.filter(id=roomId)
            roomsJSON = RoomsSerializer(rooms, many=True).data
            traders = TraderParticapation.objects.filter(roomId=roomId)
            tradersJSON = TraderParticapationSerializer(traders, many=True).data

            for room in roomsJSON:
                traderList = []
                for trader in tradersJSON:
                    trader['mean'] = float("%.2f" % trader['mean'])
                    trader['std'] = float("%.2f" % trader['std'])
                    trader['expectancy'] = float("%.2f" % trader['expectancy'])
                    trader['maxDD'] = float("%.2f" % trader['maxDD'])
                    trader['sharpe'] = float("%.2f" % trader['sharpe'])
                    trader['sortino'] = float("%.2f" % trader['sortino'])
                    trader['predicted_return'] = float("%.2f" % trader['predicted_return'])
                    trader['odds_of_win'] = "1:"+str(float("%.2f" % trader['odds_of_win']))
                    traderList.append(trader)
                room['traderData'] = traderList

            response.data = {
                "data": roomsJSON,
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

class roomViewGetActiveRooms(APIView):

    def post(self, request):
        try:
            response = Response()

            rooms = Rooms.objects.filter(active=1)
            roomsJSON = RoomsSerializer(rooms, many=True).data
            for room in roomsJSON:
                traders = TraderParticapation.objects.filter(roomId=room['id'])
                tradersJSON = TraderParticapationSerializer(traders, many=True).data
                bestOdds = 0.0
                for trader in tradersJSON:
                    if trader["odds_of_win"] > bestOdds:
                        bestOdds = trader["odds_of_win"]
                room['bestOdds'] = "1:" + str("%.2f"%bestOdds)

            response.data = {
                "data": roomsJSON,
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

class roomViewGetInActiveRooms(APIView):

    def post(self, request):
        try:
            response = Response()

            rooms = Rooms.objects.filter(active=0)
            roomsJSON = RoomsSerializer(rooms, many=True).data
            for room in roomsJSON:
                traders = TraderParticapation.objects.filter(roomId=room['id'])
                tradersJSON = TraderParticapationSerializer(traders, many=True).data
                bestOdds = 0.0
                for trader in tradersJSON:
                    if trader["odds_of_win"] > bestOdds:
                        bestOdds = trader["odds_of_win"]
                room['bestOdds'] = "1:" + str("%.2f"%bestOdds)

            response.data = {
                "data": roomsJSON,
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

class roomViewSetActiveRooms(APIView):

    def post(self, request):
        try:
            response = Response()

            tradersInRoomObject = generate_traders_for_room(generate_trader_strategy_metrics(coeff))

            roomList = Rooms.objects.filter(active=1)

            createdAt = datetime.datetime.now().strftime("%Y-%m-%d")
            roomNo = "Room " + str(roomList.count()+1)

            roomData = {
                "roomName": roomNo,
                "status": 1,
                "active": 1,
                "createdAt": createdAt
            }

            serializer = RoomsSerializer(data=roomData)
            if serializer.is_valid(raise_exception=True):
                savedRoom = serializer.save()

            newRoomList = Rooms.objects.filter(roomName=roomNo, createdAt=createdAt)
            newRoomListJson = RoomsSerializer(newRoomList, many=True).data

            newRoomId = newRoomListJson[0]['id']

            i = 1
            for trader in tradersInRoomObject:
                traderParticipationDate = {
                    "traderId": trader['traderid'],
                    "traderName": 'Trader ' + str(i),
                    "strategyId": trader['strategyid'],
                    "roomId": newRoomId,
                    "mean": trader['strategy_metrics']['mean'],
                    "std": trader['strategy_metrics']['std'],
                    "expectancy": trader['strategy_metrics']['expectancy'],
                    "maxDD": trader['strategy_metrics']['maxDD'],
                    "sharpe": trader['strategy_metrics']['sharpe'],
                    "sortino": trader['strategy_metrics']['sortino'],
                    "predicted_return": trader['predicted_return'],
                    "odds_of_win": trader['odds_of_win']
                }
                i = i + 1

                serializer = TraderParticapationSerializer(data=traderParticipationDate)
                if serializer.is_valid(raise_exception=True):
                    savedTraderParticipattion = serializer.save()

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