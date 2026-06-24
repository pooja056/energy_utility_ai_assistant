from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    customer_name: str
    issue: str


class CustomerCreate(BaseModel):
    name: str
    email: str
    phone: str
    address: str


class BillCreate(BaseModel):
    customer_id: int
    amount: int
    due_date: str
    status: str


class ChatRequest(BaseModel):
    message: str


class AIComplaintRequest(BaseModel):
    customer_name: str
    message: str