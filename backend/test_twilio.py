from twilio_service import send_sms

sid = send_sms(
    "+91 93985 45491",
    "Hello Pooja! Twilio is connected successfully."
)

print("Message SID:", sid)