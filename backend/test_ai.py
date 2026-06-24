from database import SessionLocal
from utility_ai import get_bill_summary

db = SessionLocal()

print(get_bill_summary(1, db))

db.close()