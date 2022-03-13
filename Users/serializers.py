from rest_framework import serializers 
from django.contrib.auth import authenticate
from .models import User, UserProfile

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id','email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email')
        password = data.get('password')

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                {
                    'validationError': 'An email address is required to log in.',
                }
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                {
                    'validationError': 'A password is required to log in.'
                }
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                {
                    'validationError':'Email or password did not match.'
                }
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    'validationError': 'This user has been deactivated.'
                }
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
class UserList(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields =['id', 'email', 'username', 'created_at',]

class UserProfilePublicView(serializers.ModelSerializer):
    class Meta:
        model = UserProfile

        fields = ['picture','email', 'username', 'phone_no', 'created_at']
    def validate(self, data):
        id = self.context.get('id')
        user =  User.objects.filter(id=id).first()
        if not user.is_active():
            raise serializers.ValidationError(
                {
                    'validationError':'This user has been deactivated.'
                }
            )

class UserProfilePrivateView(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        
        fields = ['picture','email','username','phone_no','address','created_at']
    def validate(self, data):
        id = self.context.get('id')
        user =  User.objects.filter(id=id).first()
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    'validationError':'This user has been deactivated.'
                }
            )
        import os
        profile = UserProfile.objects.filter(user=user).first()
        if data.get('picture') and profile.picture:
            os.remove(profile.picture.path)
        return data

class UserProfilePrivateAdd(serializers.ModelSerializer):
    class Meta:
        model = UserProfile

        fields = ['picture', 'user', 'username','phone_no','address']
 
        def validate(self, data):
            id = data.get('user')
            user =  User.objects.filter(id=id).first()
            if not user.is_active:
                raise serializers.ValidationError(
                    {
                        'validationError':'This user has been deactivated.'
                    }  
                )
            
            return data
class UserAll(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields =['id', 'email', 'username', 'password', 'is_active']
    
    def validate(self, data):
        id = self.context.get('id')
        email = data.get('email')
        password = data.get('password')
        if not email:
            raise serializers.ValidationError({
                'validationError':'Email field is required.'
            })
        if not password:
            raise serializers.ValidationError({
                'validationError':'Password field is required.'
            })
        user = User.objects.filter(id=id).first()
        user_ = authenticate(username=email, password=password)
        if not user == user_:
            raise serializers.ValidationError({
                'validationError':'Email or password did not match.'
            })
        user.is_active = True
        user.save()
        return data