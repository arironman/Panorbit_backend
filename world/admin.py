from django.contrib import admin

from world.models import City, Country, CountryLanguage

# Register your models here.
admin.site.register(Country)
admin.site.register(CountryLanguage)
admin.site.register(City)