from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt

from Users.models import User
from .models import Cloths
from .serializers import (AllClothsSerializer,
                        ClothSerializerAdd,
                        ClothSerializer,
                        MyClothSerializer)
from clothRentalBackend import settings
# Create your views here.

class CertainUserCloth(APIView):
    serializer_class = AllClothsSerializer
    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        cloths = Cloths.objects.filter(is_available=True, user=user)
        clothserializer = self.serializer_class(cloths, many=True)
        return Response(clothserializer.data)

class AuthenticatedUserCloth(APIView):
    serializer_class = MyClothSerializer
    def is_authenticated(self, request):
        jwtoken = request.COOKIES.get('jwt')
        userdata = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=['HS256'])
        id = userdata.get('id')

        user =  User.objects.filter(id=id).first()
        if user is not None:
            return user, True
        return None, False
    
    def get(self, request):
        try:
            user, is_auth = self.is_authenticated(request)
            if is_auth:
                cloths = Cloths.objects.filter(user=user)
                clothserializer = self.serializer_class(cloths, many=True)
                return Response(clothserializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)      
    
        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      


class AllClothsAPIView(APIView):
    serializer_class = AllClothsSerializer

    def get(self, request):
        cloths = Cloths.objects.all()
        clothserializer = self.serializer_class(cloths, many=True)
        return Response(clothserializer.data)
 
class AllAvailableClothsAPIView(APIView):
    serializer_class = AllClothsSerializer
    serializer_class_add = ClothSerializerAdd

    def get(self, request):
        cloths = Cloths.objects.filter(is_available=True)
        clothserializer = self.serializer_class(cloths, many=True)
        return Response(clothserializer.data)

    def is_authenticated(self, request):
        jwtoken = request.COOKIES.get('jwt')
        userdata = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=['HS256'])
        if User.objects.filter(id=userdata.get('id')).first():
            return userdata, True
        return None, False


    def post(self, request):
        try:
            user, is_auth = self.is_authenticated(request)
            if is_auth:
                request.data._mutable = True
                request.data['user'] = user.get('id')
                serializer = self.serializer_class_add(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)      
        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      


class ClothAPIView(APIView):
    serializer_class = ClothSerializer
    def get_object(self, id):
        return Cloths.objects.filter(id=id).first()

    def is_authenticated(self, request, id):
        if not self.get_object(id).user.id:
            return False
        user_id = self.get_object(id).user.id
        jwtoken = request.COOKIES.get('jwt')
        userdata = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=['HS256'])
        if userdata.get('id') == user_id:
            return True
        return False

    def get(self, request, id):
        cloth = self.get_object(id)
        if not cloth:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(cloth)
        return Response(serializer.data)
    
    def put(self, request, id):
        if not self.get_object(id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            if self.is_authenticated(request, id):
                cloth = self.get_object(id)
                context = dict()
                context['id']=id
                serializer = self.serializer_class(cloth, data=request.data, context=context)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      
          
    def delete(self, request, id):
        if not self.get_object(id):
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            if self.is_authenticated(request, id):
                cloth = self.get_object(id)
                if not cloth:
                    return Response(status=status.HTTP_204_NO_CONTENT)
                cloth.delete()
                cloth.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      
          
