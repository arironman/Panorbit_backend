
# code to import the sql data from the given dump file

import os
from django.conf import settings
from django.db import connection
from pathlib import Path

# Configure Django's settings
# BASE_DIR = Path(__file__).resolve().parent.parent 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{BASE_DIR}/Search.settings')  
# settings.configure()
# for database in settings.DATABASES:
#     print(database)
# print(settings.ROOT_URLCONF)

# path of sql dump file
# sql_dump_file = './scripts/world.sql'
def run():
    # sql_dump_file = './scripts/country.sql'
    # sql_dump_file = './scripts/country_language.sql'
    sql_dump_file = './scripts/city.sql'

    # Open the dump file and read its contents
    with open(sql_dump_file, 'r') as f:
        sql_statements = f.read()

    # Split the SQL statements by semicolon to separate them
    statements = sql_statements.split(';')
    # id = 0
    # Loop through each statement and execute it
    with connection.cursor() as cursor:
        for statement in statements:
            # Skip empty statements
            if not statement.strip():
                continue
            
            statement = statement.replace('INSERT INTO `countrylanguage` VALUES (', f'INSERT INTO `countrylanguage` (`id`, `CountryCode`, `Language`, `IsOfficial`, `Percentage` ) VALUES ({id}, ')
            
            
            statement = statement.replace('INSERT INTO `city` VALUES', f'INSERT INTO `city` (`ID`, `Name`, `CountryCode`, `District`, `Population`) VALUES')
            # print(statement)
            # Execute the SQL statement
            cursor.execute(statement)
            # id+=1


# python manage.py runscript import_data
    