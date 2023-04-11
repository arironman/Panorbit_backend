from rest_framework import serializers

from User.utils import generate_otp
from .models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
    # Define the serializer fields
    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name', 'gender', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True}  # Password field should be write-only
        }

    # Override the create method to handle user creation
    def create(self, validated_data):
        # Extract the password from the validated data
        password = ""
        if password in validated_data:
            password = validated_data.pop('password')
            
        otp = generate_otp(6)
        validated_data['otp'] = otp

        # Create a new user using the MyUserManager.create_user() method
        user = MyUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        return user
