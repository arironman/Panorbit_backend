import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from User.models import MyUser

def verify_user_from_token(token):
    try:
        # Decode JWT token
        decoded_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        # Extract user ID from decoded payload
        user_id = decoded_payload['user_id']
        # Retrieve user model
        # User = get_user_model()
        # Retrieve user object
        user = MyUser.objects.get(id=user_id)
        # Return the user object
        return user
    except jwt.ExpiredSignatureError:
        # JWT token has expired
        return None
    except jwt.InvalidTokenError:
        # Invalid JWT token
        return None
    except MyUser.DoesNotExist:
        # User not found
        return None
