import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(account_sid, auth_token)


def send_sms(to_number, message_text):
    message = client.messages.create(
        body=message_text,
        from_=twilio_number,
        to=to_number
    )

    return message.sid