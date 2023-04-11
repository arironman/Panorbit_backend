from django.http import JsonResponse
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from world.models import Country, CountryLanguage, City
from User.auth import verify_user_from_token
from django.db.models import Q

from world.serializers import CountrySerializer


# Create your views here.


class SearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('search')
        print(query)

        # verify_user_from_token(token)
        # query = ""
        countries = Country.objects.filter(
            Q(Name__icontains=query) |
            Q(countrylanguage__Language__icontains=query) |
            Q(city__Name__icontains=query)
        ).distinct()

        # print(countries.count())
        country_serializer = CountrySerializer(countries, many=True)
        response_data = country_serializer.data
        body = {
            "countries": response_data
        }
        
        return Response(body, status=status.HTTP_200_OK)



class CountryDetailsAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, code):
        try:
            country = Country.objects.get(Code=code)
        except Country.DoesNotExist:
            return Response({'error': 'Country not found'}, status=404)
        
        cities = City.objects.filter(CountryCode=country)
        languages = CountryLanguage.objects.filter(CountryCode=country)
        
        country_data = {
            'Code': country.Code,
            'Name': country.Name,
            'Continent': country.Continent,
            'Region': country.Region,
            'SurfaceArea': country.SurfaceArea,
            'IndepYear': country.IndepYear,
            'Population': country.Population,
            'LifeExpectancy': country.LifeExpectancy,
            'GNP': country.GNP,
            'GNPOld': country.GNPOld,
            'LocalName': country.LocalName,
            'GovernmentForm': country.GovernmentForm,
            'HeadOfState': country.HeadOfState,
            'Capital': country.Capital,
            'Code2': country.Code2,
            'Cities': [{'ID': city.ID, 'Name': city.Name, 'District': city.District, 'Population': city.Population} for city in cities],
            'Languages': [{'Language': language.Language, 'IsOfficial': language.IsOfficial, 'Percentage': language.Percentage} for language in languages]
        }
        
        return Response(country_data)
