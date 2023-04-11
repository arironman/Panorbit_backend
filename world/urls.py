from django.urls import path
from world.views import CountryDetailsAPIView, SearchView

urlpatterns = [
    path('', SearchView.as_view(), name='signup'),  
    path('country/<str:code>/', CountryDetailsAPIView.as_view(), name='country-details')
]