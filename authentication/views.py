from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer,LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.authtoken.models import Token
import jwt
import hashlib
# Create your views here.


class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def make_password(password):
        assert password
        hash = hashlib.md5(password).hexdigest()
        return hash

    def post(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        #print(username)
        #print(password)

        #passwords = make_password(password)
        #print(passwords)
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user:
            auth_token = jwt.encode(
                {'username': user.username}, settings.JWT_SECRET_KEY)

            serializer = UserSerializer(user)

            data = {'user': serializer.data, 'token': auth_token}

            return Response(data, status=status.HTTP_200_OK)

            # SEND RES
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

'''
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user_obj = None
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')

        if not username and not password:
            return Response({'Error': 'Username is required to login'}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.filter(
            Q(username=username)
        ).distinct()
        if user.exists() and user.count()==1:
            user_obj = user.first()
        else:
            return Response({'Error': 'Username is not valid'}, status=status.HTTP_401_UNAUTHORIZED)

        if user_obj:
            if not user_obj.check_password(password):
                return Response({'Error': 'Incorrect Credentials, Please try again'}, status=status.HTTP_401_UNAUTHORIZED)
        data["token"] = "some token"
        return Response(data, status=status.HTTP_200_OK)
'''