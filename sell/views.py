from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt

from cloths.models import Cloths
from Users.models import User
from order.models import Orders
from clothRentalBackend import settings

# Create your views here.

class sellAPIview(APIView):
    def is_authenticated(self, request, id):
        jwtoken = request.COOKIES.get('jwt')
        userdata = jwt.decode(jwtoken, settings.SECRET_KEY, algorithms=['HS256'])
        if id == userdata.get('id'):
            return True
        return False
    def post(self, request, id):
        order = Orders.objects.filter(id=id).first()
        if order is None:
            raise serializers.ValidationError(
                {
                    'validationError':'No order with that id'
                }
            )
        buying_user = order.user
        cloth = order.cloth
        selling_user = cloth.user
        try:
            if self.is_authenticated(request, selling_user.id):
                cloth.sell_to(buying_user.id)   
                return Response(status=status.HTTP_200_OK)      
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        except jwt.exceptions.DecodeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        