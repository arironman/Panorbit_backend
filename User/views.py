from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from User.models import MyUser
from User.utils import generate_otp, send_otp
from .serializers import MyUserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class SignupView(APIView):
    def post(self, request):        
        # Serialize the request data
        serializer = MyUserSerializer(data=request.data)

        # Validate the data
        if serializer.is_valid():
            # Create a new user using the serializer's create method
            user = serializer.create(serializer.validated_data)

            # Return a success response
            body = {'message': 'User registered successfully'}
            return Response(body, status=status.HTTP_201_CREATED)

        # Return an error response with the validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
            
    def post(self, request):
        # authentication_classes = [JWTAuthentication]
        
        email_or_phone = request.data.get('email')
        otp = request.data.get('otp')


        # Check if the email_or_phone is a valid email address
        if '@' in email_or_phone:
            # User is trying to login with email, authenticate using email and password
            user = MyUser.objects.authenticate(email_or_phone=email_or_phone, otp=otp)
            print(user)
        else:
            # User is trying to login with phone number, verify the OTP
            user = MyUser.objects.filter(phone_number=email_or_phone).first()

            if user:
                if user.check_otp(otp):
                    # If OTP is verified, authenticate the user
                    user = MyUser.objects.authenticate(email_or_phone=email_or_phone, otp=otp)
                    
                else:
                    body = {'message': 'Invalid OTP'}
                    return Response(body, status=status.HTTP_401_UNAUTHORIZED)
        # If the user is authenticated
        if user is not None:
            # Log the user in
            # login(request, user)

            refresh = RefreshToken.for_user(user)
            # Return a success response with the token
            body = {
                # 'token': token.key,
                'user_id': user.email,
                'access': str(refresh.access_token),
            }
            return Response(body, status=status.HTTP_200_OK)

        # Return an error response if authentication fails
        body = {'message': 'Invalid email/phone'}
        return Response(body, status=status.HTTP_401_UNAUTHORIZED)


class GenerateOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')

        # Check if the user with the given phone number exists
        user = MyUser.objects.filter(email=email).first()
        if user:
            # Generate an OTP
            otp = generate_otp(6)  # Generate a 6-digit OTP

            # Send the OTP to the user's phone number
            # to_email = 'meanuragrai@gmail.com'  
            phone = user.phone_number
            send_otp(phone, otp) 


            # Save the OTP to the user model
            user.set_otp(otp)
            # user.otp = otp
            # user.otp_created_at = datetime.now()
            # user.save()


            # Return a success response
                # "otp":otp
            body = {
                "message": "OTP sent to the provided phone number"
                }
            return Response(body, status=status.HTTP_200_OK)

        # Return an error response if the user is not found
        body = {'message': 'User not found with the provided Email address.'}
        return Response(body, status=status.HTTP_404_NOT_FOUND)


class Auth(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = request.user.email

        body = {
            "email":email
        }
        return Response(body, status=status.HTTP_200_OK)
