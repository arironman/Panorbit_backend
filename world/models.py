from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

class Country(models.Model):
    Code = models.CharField(max_length=3, primary_key=True)
    Name = models.CharField(max_length=52, default='')
    CONTINENT_CHOICES = (
        ('Asia', 'Asia'),
        ('Europe', 'Europe'),
        ('North America', 'North America'),
        ('Africa', 'Africa'),
        ('Oceania', 'Oceania'),
        ('Antarctica', 'Antarctica'),
        ('South America', 'South America'),
    )
    Continent = models.CharField(max_length=15, choices=CONTINENT_CHOICES, default='Asia')
    Region = models.CharField(max_length=26, default='')
    SurfaceArea = models.FloatField(default=0.00)
    IndepYear = models.SmallIntegerField(null=True)
    Population = models.IntegerField(default=0)
    LifeExpectancy = models.FloatField(null=True)
    GNP = models.FloatField(null=True)
    GNPOld = models.FloatField(null=True)
    LocalName = models.CharField(max_length=45, default='')
    GovernmentForm = models.CharField(max_length=45, default='')
    HeadOfState = models.CharField(max_length=60, null=True)
    Capital = models.IntegerField(null=True)
    Code2 = models.CharField(max_length=2, default='')

    class Meta:
        db_table = 'country'

    def __str__(self):
        return self.Name



class CountryLanguage(models.Model):
    CountryCode = models.ForeignKey('Country', on_delete=models.CASCADE, db_column='CountryCode')
    Language = models.CharField(max_length=30)
    ISOFFICIAL_CHOICES = (
        ('T', 'T'),
        ('F', 'F'),
    )
    IsOfficial = models.CharField(max_length=1, choices=ISOFFICIAL_CHOICES, default='F')
    Percentage = models.FloatField(default=0.0, validators=[MaxValueValidator(100.0)])

    class Meta:
        db_table = 'countrylanguage'
        unique_together = (('CountryCode', 'Language'),)

    def __str__(self):
        return f'{self.CountryCode} - {self.Language}'



class City(models.Model):
    ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=35)
    CountryCode = models.ForeignKey('Country', on_delete=models.CASCADE, db_column='CountryCode')
    District = models.CharField(max_length=20)
    Population = models.IntegerField(default=0)

    class Meta:
        db_table = 'city'
        
    def __str__(self):
        return f'{self.CountryCode} - {self.Name}'
