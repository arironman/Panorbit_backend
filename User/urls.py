from django.urls import path
from User.views import Auth, GenerateOTPView, LoginView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  
    path('login/', LoginView.as_view(), name='login'),  
    path('get-otp/', GenerateOTPView.as_view(), name='get_otp'),  
    path('auth/', Auth.as_view(), name='auth'),  
    
]