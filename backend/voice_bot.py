from fastapi.responses import Response


def handle_voice():
    twiml = """
    <Response>
        <Say voice="alice">
            Welcome to Energy Utility AI Assistant.
            Your AI voice bot is working successfully.
        </Say>
    </Response>
    """

    return Response(
        content=twiml,
        media_type="application/xml"
    )