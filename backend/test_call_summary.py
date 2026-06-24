from call_summary import generate_call_summary

conversation = """
Customer: There has been no power in LB Nagar since morning.
Customer: I have elderly people at home.
Customer: Please resolve this issue quickly.
"""

print(generate_call_summary(conversation))