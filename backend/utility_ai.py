from sqlalchemy.orm import Session
from models import Bill
from ai_service import ask_ai


def get_bill_summary(customer_id: int, db: Session):

    bill = db.query(Bill).filter(
        Bill.customer_id == customer_id
    ).first()

    if not bill:
        return "No bill found for this customer."

    prompt = f"""
    You are an Energy Utility Assistant.

    Customer Bill Information:

    Customer ID: {bill.customer_id}
    Bill Amount: ₹{bill.amount}
    Due Date: {bill.due_date}
    Status: {bill.status}

    Explain this bill information clearly to the customer.
    """

    return ask_ai(prompt)