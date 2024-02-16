from django.shortcuts import render
from .serializers import UserSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework import status,authentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context={
                'success':True,
                'status':status.HTTP_201_CREATED,
                'msg':'Registration successfully',
                'data':serializer.data
            }
            return Response(context)
        context={
                'success':False,
                'status':status.HTTP_400_BAD_REQUEST,
                'msg':'Invalid Crediancial',
                'data':serializer.errors
            }
        return Response(context)
    
class UserLoginView(APIView):
    def post(self,request, *args, **kwargs):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            user=authenticate(email=email,password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                context={
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(context)
            context={
                'success':False,
                'status':status.HTTP_401_UNAUTHORIZED,
                'msg':'Invalid Credentials',
                'data':{}
            }
            return Response(context)
        context={
            'success':False,
            'status':status.HTTP_400_BAD_REQUEST,
            'msg':'Login Failed',
            'data':serializer.errors
        }
        return Response(context)

        

