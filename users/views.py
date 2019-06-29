from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Users
from .serializers import UsersSerializer, UsersFilteredSerializer

class userViewGet(APIView):

    def post(self, request):
        try:
            response = Response()

            inputUsername = self.request.data['username']

            user = Users.objects.filter(username=inputUsername)

            response.data = {
                "data": UsersFilteredSerializer(user, many=True).data,
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
            return response

class userViewLogin(APIView):

    def post(self, request):
        try:
            response = Response()

            inputUsername = self.request.data['username']
            inputPassword = self.request.data['password']

            user = Users.objects.filter(username=inputUsername, password=inputPassword)

            if user.count() == 0:
                response.data = {
                    "data": None,
                    "failedReason": "Failed login",
                    "success": False
                }
                return response

            response.data = {
                "data": UsersFilteredSerializer(user, many=True).data,
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
            return response

class userViewRegister(APIView):

    def post(self, request):
        try:
            response = Response()

            inputUsername = self.request.data['username']
            inputPassword = self.request.data['password']

            user = Users.objects.filter(username=inputUsername)

            if user.count() > 0:
                response.data = {
                    "data": None,
                    "failedReason": "User already existed",
                    "success": False
                }
                return response

            userData = {
                "username": inputUsername,
                "password": inputPassword,
                "token": 50.00
            }

            serializer = UsersSerializer(data=userData)
            if serializer.is_valid(raise_exception=True):
                savedUser = serializer.save()

            response.data = {
                "data": {
                    "username": inputUsername,
                    "token": 50.00
                },
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
