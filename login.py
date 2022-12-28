import os
from wyze_sdk import Client

client = Client().login(os.environ['WYZE_EMAIL'], password=os.environ['WYZE_PASSWORD'])
print(f"access token: {client['access_token']}")
print(f"refresh token: {client['refresh_token']}")