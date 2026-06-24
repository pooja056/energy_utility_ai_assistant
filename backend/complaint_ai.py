from ai_service import ask_ai


def analyze_complaint(message: str):

    prompt = f"""
    You are an Energy Utility Complaint Assistant.

    Analyze the customer message.

    Customer Message:
    {message}

    Identify:
    1. Complaint Type
    2. Priority
    3. Short Summary

    Return a professional response.
    """

    return ask_ai(prompt)