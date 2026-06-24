import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_ai(question: str):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                You are an AI assistant for an Energy Utility Company.
                Help customers with:
                - Electricity bill enquiries
                - Power outage complaints
                - Utility services
                - General customer support
                """
            },
            {
                "role": "user",
                "content": question
            }
        ],
        model="llama-3.3-70b-versatile"
    )

    return response.choices[0].message.content