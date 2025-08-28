from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, CheckConstraint
)
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from .database import Base
import datetime

ALLOWED_STATUSES = {"Scheduled", "Completed", "Cancelled"}

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, CheckConstraint("age >= 0"))
    gender = Column(String)               # e.g., "Male", "Female", "Other"
    contact_info = Column(String)         # phone/email

    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient #{self.id} {self.name}>"

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    contact_info = Column(String)

    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Doctor #{self.id} {self.name} ({self.specialization})>"

class Appointment(Base):
    __tablename__ = "appointments"
    __table_args__ = (
        UniqueConstraint("doctor_id", "appointment_time", name="uq_doctor_time"),
    )

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    status = Column(String, default="Scheduled", nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

    @validates("status")
    def validate_status(self, key, value):
        if value not in ALLOWED_STATUSES:
            raise ValueError(f"Invalid status '{value}'. Allowed: {sorted(ALLOWED_STATUSES)}")
        return value

    @validates("appointment_time")
    def validate_time(self, key, value):
        if not isinstance(value, datetime.datetime):
            raise ValueError("appointment_time must be a datetime")
        return value

    @hybrid_property
    def is_past(self):
        return self.appointment_time < datetime.datetime.now()

    def __repr__(self):
        t = self.appointment_time.strftime("%Y-%m-%d %H:%M")
        return f"<Appointment #{self.id} {t} {self.status}>"
