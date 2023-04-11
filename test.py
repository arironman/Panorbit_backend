# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
# Set environment variables for your credentials
# Read more at http://twil.io/secure
account_sid = "AC08ff98ac386a7eccb070e3ca2aa0aea2"
# auth_token = os.environ["TWILIO_AUTH_TOKEN"]
auth_token = "4ad39c7c368dc5a60d418edf70740c53"
client = Client(account_sid, auth_token)
message = client.messages.create(
  body="Hello from Twilio",
  from_="+15074686332",
  to="+919327006155"
)
print(message.sid)