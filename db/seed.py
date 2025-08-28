from .database import SessionLocal
from .models import Doctor, Patient

def run():
    session = SessionLocal()
    if session.query(Doctor).count() == 0:
        session.add_all([
            Doctor(name="Dr. Asha Noor", specialization="General Medicine", contact_info="0700-111-111"),
            Doctor(name="Dr. Yusuf Ali", specialization="Pediatrics", contact_info="0700-222-222"),
            Doctor(name="Dr. Mary Wanjiru", specialization="Dermatology", contact_info="0700-333-333"),
        ])
    if session.query(Patient).count() == 0:
        session.add_all([
            Patient(name="John Doe", age=30, gender="Male", contact_info="john@example.com"),
            Patient(name="Fatma Ibrahim", age=26, gender="Female", contact_info="fatma@example.com"),
        ])
    session.commit()
    session.close()
    print("Seed complete.")

if __name__ == "__main__":
    run()
