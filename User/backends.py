from User.models import MyUser

class MyCustomAuthenticationBackend:
    def authenticate(self, request=None, email=None, password=None):
        # Call the custom authentication method from MyUserManager
        return MyUser.objects.authenticate(request=request, email=email, otp=password)

    def get_user(self, user_id):
        # Retrieve the user object by user_id
        try:
            return MyUser.objects.get(pk=user_id)
        except MyUser.DoesNotExist:
            return None

    # Other required methods for authentication backends here...
