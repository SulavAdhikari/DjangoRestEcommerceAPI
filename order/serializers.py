from rest_framework import serializers
from .models import Orders
from Users.models import User
from cloths.models import Cloths

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ['user','cloth','shipping_addr']
        def validate(self, data):
            user = User.objects.filter(id=data.get('user')).first()
            cloth = Cloths.objects.filter(id=data.get('cloth')).first()
            if user == cloth.user:
                raise serializers.ValidationError(
                {
                    'validationError':'You cant buy your own cloth.'
                }
            )
            if not cloth.is_available:
                raise serializers.ValidationError(
                    {
                        'validationError':'This cloth is not available.'
                    }
                ) 
            return data

class AllOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

    def validate(self,data):
        user = User.objects.filter(id=data.get('user')).first()
        cloth = Cloths.objects.filter(id=data.get('cloth')).first()
        if not cloth.is_available:
            raise serializers.ValidationError(
                {
                    'validationError':'This cloth is not available.'
                }
            )
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    'validationError':'This user has been deactivated.'
                }
            )
        return data
        