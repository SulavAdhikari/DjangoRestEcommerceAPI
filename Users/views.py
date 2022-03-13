from logging import raiseExceptions
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt
from clothRentalBackend import settings
from .serializers import (
    RegistrationSerializer, LoginSerializer, UserList,
    UserProfilePublicView,  UserProfilePrivateView,
    UserProfilePrivateAdd, UserAll)
from .models import User, UserProfile

# Create your views here.
class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

     
            
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserListAPIView(APIView):
    serializer_class = UserList
    def get(self, request):
        users = User.objects.filter(is_active=True)
        userserializer = self.serializer_class(users, many=True)
        return Response(userserializer.data)

class UsersAllAPIView(APIView):
    serializer_class = UserList
    def get(self, request):
        users = User.objects.all()
        userserializer = self.serializer_class(users, many=True)
        return Response(userserializer.data)

class UserReactivate(APIView):
    serializer_class = UserAll
    def put(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        context = dict()
        context['id'] = id
        user.is_active = True
        serializer = self.serializer_class(user, data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class UserPublicAPIView(APIView):
    serializer_class = UserProfilePublicView
    def get_obj(self,id):
        user = User.objects.filter(id=id, is_active=True).first()
        userprofile = UserProfile.objects.filter(user=user).first()
        return userprofile
    
    def get(self, request, id):
        userprofile = self.get_obj(id)
        if not userprofile:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(userprofile)

        return Response(serializer.data)

class UserPrivateAPIView(APIView):
    serializer_class = UserProfilePrivateView
    serializer_add = UserProfilePrivateAdd
    def get_user_obj(self, id):
        return User.objects.filter(id=id).first()

    def get_obj(self, id):
        user = User.objects.filter(id=id, is_active=True).first()
        userprofile = UserProfile.objects.filter(user=user).first()
        return userprofile

    def is_authenticated(self, request, id):
        jwtoken = request.COOKIES.get('jwt')
        userdata = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=['HS256'])
        if id == userdata.get('id'):
            return True
        return False
    def get(self, request, id):
        try:
            if self.is_authenticated(request, id):
                userprofile = self.get_obj(id)
                if not userprofile:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                serializer = self.serializer_class(userprofile)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, id):
        try:
            if self.is_authenticated(request, id):
                request.data._mutable = True
                request.data['user'] = id#self.get_user_obj(id)
                user = User.objects.filter(id=id).first()
                userprofile = UserProfile.objects.filter(user=user).first()
                from rest_framework import serializers
                if userprofile is not None:
                    raise serializers.ValidationError(
                    {
                        'validationError':'This user already has a profile.'
                    }
                )
                serializer = self.serializer_add(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      
        
    def put(self, request, id):
        try:
            if self.is_authenticated(request, id):
                userprofile = self.get_obj(id)
                if not userprofile:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                obj = self.get_obj(id)
                context = dict()  
                context['id']=id          
                serializer = self.serializer_class(obj, data=request.data, context=context)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)      
    
        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      

    def delete(self, request,id):
        try:
            if self.is_authenticated(request, id):
                userprofile = self.get_obj(id)
                if not userprofile:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                userobj = User.objects.filter(id=id).first()
                userobj.is_active = False
                userobj.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

            

