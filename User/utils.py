import os
import smtplib
import random
import string
from django.core.mail import send_mail
from twilio.rest import Client

from Search.settings import auth_token, account_sid


def generate_otp(length=6):
    """
        Function to generate OTP
    """
    characters = string.digits
    otp = ''.join(random.choice(characters) for i in range(length))
    return otp


def send_otp(phone, otp):
    '''
        Function to send the OTP to an email
    '''
    body = f'Hello,\n\nYour OTP is: {otp}\n\nPlease do not share this OTP with anyone.\n\n'

    try:
        # account_sid = os.environ.get("account_sid")
        # auth_token = os.environ.get("auth_token")
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=body,
            from_="+15074686332",
            to=f"+91{phone}"
        )
        print(message.sid)

        # print('OTP sent successfully to', to_email)
    except Exception as e:
        print('Error:', e)
