from ai_service import ask_ai


def generate_call_summary(conversation: str):

    prompt = f"""
    You are a utility call center assistant.

    Summarize the following customer conversation.

    Include:
    1. Summary
    2. Complaint Type
    3. Priority
    4. Recommended Action

    Conversation:
    {conversation}
    """

    return ask_ai(prompt)