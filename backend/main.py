from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from voice_bot import handle_voice

from database import get_db
from models import Complaint, Customer, Bill,User
from schemas import (
    ComplaintCreate,
    CustomerCreate,
    BillCreate,
    ChatRequest,
    AIComplaintRequest,
    UserCreate,
    LoginRequest,
    ComplaintStatusUpdate
)

from ai_service import ask_ai
from utility_ai import get_bill_summary
from complaint_ai import analyze_complaint

app = FastAPI()


# ------------------------
# HOME APIs
# ------------------------

@app.get("/")
def home():
    return {"message": "Utility AI Backend Running"}


@app.get("/about")
def about():
    return {
        "project": "Energy Utility AI Assistant",
        "version": "1.0"
    }


# ------------------------
# COMPLAINT APIs
# ------------------------

@app.post("/complaint")
def register_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db)
):
    new_complaint = Complaint(
        customer_name=complaint.customer_name,
        issue=complaint.issue,
        status="Open"
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return {
        "message": "Complaint Registered Successfully",
        "complaint_id": new_complaint.id
    }


@app.get("/complaints")
def get_complaints(db: Session = Depends(get_db)):
    complaints = db.query(Complaint).all()

    return [
        {
            "id": complaint.id,
            "customer_name": complaint.customer_name,
            "issue": complaint.issue,
            "status": complaint.status
        }
        for complaint in complaints
    ]


# ------------------------
# AI COMPLAINT API
# ------------------------

@app.post("/ai/complaint")
def ai_complaint(
    request: AIComplaintRequest,
    db: Session = Depends(get_db)
):
    ai_analysis = analyze_complaint(request.message)

    new_complaint = Complaint(
        customer_name=request.customer_name,
        issue=request.message,
        status="Open"
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return {
        "message": "Complaint Registered Successfully",
        "complaint_id": new_complaint.id,
        "ai_analysis": ai_analysis
    }


# ------------------------
# CUSTOMER APIs
# ------------------------

@app.post("/customer")
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return {
        "message": "Customer Created Successfully",
        "customer_id": new_customer.id
    }


@app.get("/customers")
def get_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()

    return [
        {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address
        }
        for customer in customers
    ]


# ------------------------
# BILL APIs
# ------------------------

@app.post("/bill")
def create_bill(
    bill: BillCreate,
    db: Session = Depends(get_db)
):
    new_bill = Bill(
        customer_id=bill.customer_id,
        amount=bill.amount,
        due_date=bill.due_date,
        status=bill.status
    )

    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)

    return {
        "message": "Bill Created Successfully",
        "bill_id": new_bill.id
    }


@app.get("/bills")
def get_bills(db: Session = Depends(get_db)):
    bills = db.query(Bill).all()

    return [
        {
            "id": bill.id,
            "customer_id": bill.customer_id,
            "amount": bill.amount,
            "due_date": bill.due_date,
            "status": bill.status
        }
        for bill in bills
    ]


@app.get("/bill/{customer_id}")
def get_customer_bill(
    customer_id: int,
    db: Session = Depends(get_db)
):
    bills = db.query(Bill).filter(
        Bill.customer_id == customer_id
    ).all()

    return [
        {
            "id": bill.id,
            "amount": bill.amount,
            "due_date": bill.due_date,
            "status": bill.status
        }
        for bill in bills
    ]


# ------------------------
# AI BILL API
# ------------------------

@app.get("/ai/bill/{customer_id}")
def ai_bill_explanation(
    customer_id: int,
    db: Session = Depends(get_db)
):
    response = get_bill_summary(customer_id, db)

    return {
        "customer_id": customer_id,
        "ai_response": response
    }


# ------------------------
# AI CHAT API
# ------------------------

@app.post("/chat")
def chat(chat_request: ChatRequest):
    response = ask_ai(chat_request.message)

    return {
        "question": chat_request.message,
        "response": response
    }


@app.api_route("/voice", methods=["GET", "POST"])
def voice():
    return handle_voice()
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

@app.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == login_data.email
    ).first()

    if not user:
        return {"message": "User not found"}

    if user.password != login_data.password:
        return {"message": "Invalid password"}

    return {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name
    }

@app.put("/complaint/{complaint_id}")
def update_complaint_status(
    complaint_id: int,
    update: ComplaintStatusUpdate,
    db: Session = Depends(get_db)
):
    complaint = db.query(Complaint).filter(
        Complaint.id == complaint_id
    ).first()

    if not complaint:
        return {"message": "Complaint not found"}

    complaint.status = update.status

    db.commit()

    return {
        "message": "Complaint status updated successfully",
        "complaint_id": complaint.id,
        "new_status": complaint.status
    }
