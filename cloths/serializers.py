from rest_framework import serializers
from Users.models import User
from .models import Cloths

import os

class MyClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloths
        fields = '__all__'

class AllClothsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloths
        fields = ['slug','user','name','desc','_for','picture1','picture2','picture3','picture4', 'bought_on','is_available','hourly_price','security']

class ClothSerializerAdd(serializers.ModelSerializer):
    class Meta:
        model = Cloths
        fields = ["user","name","desc","_for","picture1","picture2","picture3","picture4","bought_on", "hourly_price", "security"]

    def validate(self, data):
        user = data.get('user')
    
        #user =  User.objects.filter(id=id).first()
        
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    'validationError':'This user has been deactivated.'
                }
            )
        return data
        

class ClothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cloths
        fields = ["name", "desc","_for","picture1","picture2","picture3","picture4","is_available",'hourly_price','security']
        
    def validate(self, data):
        id = self.context.get('id')
        cloth = Cloths.objects.filter(id=id).first()
        if data.get('picture1') and cloth.picture1:
            os.remove(cloth.picture1.path)
        if data.get('picture2') and cloth.picture2:
            os.remove(cloth.picture2.path)
        if data.get('picture3') and cloth.picture3:
            os.remove(cloth.picture3.path)
        if data.get('picture4') and cloth.picture4:
            os.remove(cloth.picture4.path)
        return data



