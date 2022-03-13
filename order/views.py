from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt

from cloths.models import Cloths

from .models import Orders
from clothRentalBackend import settings
from Users.models import User, UserProfile
from .serializers import AllOrdersSerializer, OrderSerializer
# Create your views here.



class OrderAClothAPIView(APIView):
    serializer_class = OrderSerializer
    def is_authenticated(self, request):
        jwtoken = request.COOKIES.get('jwt')
        userdata = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=['HS256'])
        id = userdata.get('id')

        user =  User.objects.filter(id=id).first()
        if user is not None:
            return user, True
        return None, False

    def post(self, request, id):
        try:
            user, is_auth = self.is_authenticated(request)
            if is_auth:
                userprofile = UserProfile.objects.filter(user=user).first()
                cloth = Cloths.objects.filter(id=id).first()
                order = Orders.objects.filter(user=user, cloth=cloth).first()
                if order is not None:
                    raise serializers.ValidationError(
                {
                    'validationError':'Already ordered this cloth.'
                }
                )
                if user.id == cloth.user.id:
                    raise serializers.ValidationError(
                {
                    'validationError':'Cant order own cloth.'
                }
                )

                data=dict()
                data['user'] = user.id
                data['cloth']=id
                data['shipping_addr'] = userprofile.address
                if request.data.get('shipping_addr'):
                    data['shipping_addr'] = request.data.get('shipping_addr')
                serializer = self.serializer_class(data = data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)      
        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      

                
                        

class MySentOrdersAPIView(APIView):
    serializer_class = AllOrdersSerializer
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
                orders = Orders.objects.filter(user=user)
                clothserializer = self.serializer_class(orders, many=True)
                return Response(clothserializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)      
    
        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      

class MyClothOrdersAPIView(APIView):
    serializer_class = AllOrdersSerializer
    def is_authenticated(self, request):
        jwtoken = request.COOKIES.get('jwt')
        userdata = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=['HS256'])
        id = userdata.get('id')

        user =  User.objects.filter(id=id).first()
        if user is not None:
            return user, True
        return None, False

    def get(self, request, id):
        try:
            user, is_auth = self.is_authenticated(request)
            cloth = Cloths.objects.filter(id=id).first()
            if is_auth:
                orders = Orders.objects.filter(user=user, cloth=cloth)
                orderserializer = self.serializer_class(orders, many=True)
                return Response(orderserializer.data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)      
    
        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)      

    def delete(self, request, id):
        try:
            user, is_auth = self.is_authenticated(request)
            cloth = Cloths.objects.filter(id=id).first()
            if is_auth:
                order = Orders.objects.filter(user=user, cloth=cloth).first()
                if order.is_accepted:
                    raise Exception({
                        'ValidationError':'cannot delete an accepted order'
                    })
                else:
                    order.delete()                   
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)      
    
        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED) 

