from tabulate import tabulate
from colorama import Fore, Style
from datetime import datetime
from db.database import SessionLocal
from db.models import Patient, Doctor, Appointment, ALLOWED_STATUSES
from .prompts import read_int, read_nonempty, read_datetime, confirm


session = SessionLocal()


MAIN_MENU = (
    "1. Patient",
    "2. Doctor",
    "3. Admin",
    "4. Exit",
)

def print_menu(options_tuple):
    print()
    for line in options_tuple:
        print(line)

def patient_register():
    name = read_nonempty("Name: ")
    age = read_int("Age: ")
    gender = read_nonempty("Gender: ")
    contact = read_nonempty("Contact info: ")
    p = Patient(name=name, age=age, gender=gender, contact_info=contact)
    session.add(p)
    session.commit()
    print(Fore.GREEN + f"Registered Patient ID: {p.id}" + Style.RESET_ALL)

def patient_book():
    patient_id = read_int("Your Patient ID: ")
    patient = session.get(Patient, patient_id)
    if not patient:
        print(Fore.RED + "Patient not found." + Style.RESET_ALL)
        return

  
    doctors = session.query(Doctor).order_by(Doctor.id).all()
    if not doctors:
        print(Fore.RED + "No doctors found. Ask admin to add doctors." + Style.RESET_ALL)
        return
    rows = [(d.id, d.name, d.specialization, d.contact_info) for d in doctors]
    print(tabulate(rows, headers=["ID", "Name", "Specialization", "Contact"]))

    doctor_id = read_int("Choose Doctor ID: ")
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        print(Fore.RED + "Doctor not found." + Style.RESET_ALL)
        return

    appt_time = read_datetime("Appointment time")
   
    conflict = (
        session.query(Appointment)
        .filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_time == appt_time,
            Appointment.status != "Cancelled",
        )
        .first()
    )
    if conflict:
        print(Fore.RED + "Selected time is already booked for this doctor." + Style.RESET_ALL)
        return

    appt = Appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_time=appt_time)
    session.add(appt)
    try:
        session.commit()
        print(Fore.GREEN + f"Appointment booked. ID: {appt.id}" + Style.RESET_ALL)
    except Exception as e:
        session.rollback()
        print(Fore.RED + f"Error booking appointment: {e}" + Style.RESET_ALL)

def patient_view():
    patient_id = read_int("Your Patient ID: ")
    appts = (
        session.query(Appointment)
        .filter_by(patient_id=patient_id)
        .order_by(Appointment.appointment_time.asc())
        .all()
    )
    if not appts:
        print(Fore.YELLOW + "No appointments found." + Style.RESET_ALL)
        return
    # List of dicts that are  then print as table
    rows = [
        {
            "ID": a.id,
            "Doctor": a.doctor.name,
            "Time": a.appointment_time.strftime("%Y-%m-%d %H:%M"),
            "Status": a.status,
        }
        for a in appts
    ]
    print(tabulate([list(r.values()) for r in rows], headers=list(rows[0].keys())))

def patient_menu():
    options = (
        "1. Register as new patient",
        "2. Book an appointment",
        "3. View my appointments",
        "4. Back",
    )
    ACTIONS = {  #this for dict mapping
        "1": patient_register,
        "2": patient_book,
        "3": patient_view,
        "4": lambda: "BACK",
    }
    while True:
        print(Fore.CYAN + "\n--- Patient Menu ---" + Style.RESET_ALL)
        print_menu(options)
        choice = input("Choose: ").strip()
        action = ACTIONS.get(choice)
        if not action:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            continue
        if action() == "BACK":
            break

def doctor_view():
    doctor_id = read_int("Your Doctor ID: ")
    appts = (
        session.query(Appointment)
        .filter_by(doctor_id=doctor_id)
        .order_by(Appointment.appointment_time.asc())
        .all()
    )
    if not appts:
        print(Fore.YELLOW + "No appointments scheduled." + Style.RESET_ALL)
        return
    rows = [(a.id, a.patient.name, a.appointment_time.strftime("%Y-%m-%d %H:%M"), a.status) for a in appts]
    print(tabulate(rows, headers=["ID", "Patient", "Time", "Status"]))

def doctor_complete():
    appt_id = read_int("Appointment ID to mark Completed: ")
    appt = session.get(Appointment, appt_id)
    if not appt:
        print(Fore.RED + "Appointment not found." + Style.RESET_ALL)
        return
    appt.status = "Completed"
    session.commit()
    print(Fore.GREEN + "Marked as Completed." + Style.RESET_ALL)

def doctor_menu():
    options = (
        "1. View my appointments",
        "2. Mark appointment completed",
        "3. Back",
    )
    ACTIONS = {
        "1": doctor_view,
        "2": doctor_complete,
        "3": lambda: "BACK",
    }
    while True:
        print(Fore.MAGENTA + "\n--- Doctor Menu ---" + Style.RESET_ALL)
        print_menu(options)
        choice = input("Choose: ").strip()
        action = ACTIONS.get(choice)
        if not action:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            continue
        if action() == "BACK":
            break

def admin_list_patients():
    patients = session.query(Patient).order_by(Patient.id).all()
    if not patients:
        print(Fore.YELLOW + "No patients." + Style.RESET_ALL)
        return
    rows = [(p.id, p.name, p.age, p.gender, p.contact_info) for p in patients]
    print(tabulate(rows, headers=["ID", "Name", "Age", "Gender", "Contact"]))

def admin_list_doctors():
    doctors = session.query(Doctor).order_by(Doctor.id).all()
    if not doctors:
        print(Fore.YELLOW + "No doctors." + Style.RESET_ALL)
        return
    rows = [(d.id, d.name, d.specialization, d.contact_info) for d in doctors]
    print(tabulate(rows, headers=["ID", "Name", "Specialization", "Contact"]))

def admin_list_appointments():
    appts = session.query(Appointment).order_by(Appointment.appointment_time).all()
    if not appts:
        print(Fore.YELLOW + "No appointments." + Style.RESET_ALL)
        return
    rows = [
        (a.id, a.patient.name, a.doctor.name, a.appointment_time.strftime("%Y-%m-%d %H:%M"), a.status)
        for a in appts
    ]
    print(tabulate(rows, headers=["ID", "Patient", "Doctor", "Time", "Status"]))

def admin_add_doctor():
    name = read_nonempty("Doctor name: ")
    spec = read_nonempty("Specialization: ")
    contact = read_nonempty("Contact info: ")
    d = Doctor(name=name, specialization=spec, contact_info=contact)
    session.add(d)
    session.commit()
    print(Fore.GREEN + f"Added Doctor ID: {d.id}" + Style.RESET_ALL)

def admin_cancel_appointment():
    appt_id = read_int("Appointment ID to cancel: ")
    appt = session.get(Appointment, appt_id)
    if not appt:
        print(Fore.RED + "Appointment not found." + Style.RESET_ALL)
        return
    if not confirm("Are you sure you want to cancel?"):
        print(Fore.YELLOW + "Cancelled by user." + Style.RESET_ALL)
        return
    appt.status = "Cancelled"
    session.commit()
    print(Fore.RED + "Appointment status set to Cancelled." + Style.RESET_ALL)

def admin_menu():
    options = (
        "1. View all patients",
        "2. View all doctors",
        "3. View all appointments",
        "4. Add doctor",
        "5. Cancel appointment",
        "6. Back",
    )
    ACTIONS = {
        "1": admin_list_patients,
        "2": admin_list_doctors,
        "3": admin_list_appointments,
        "4": admin_add_doctor,
        "5": admin_cancel_appointment,
        "6": lambda: "BACK",
    }
    while True:
        print(Fore.YELLOW + "\n--- Admin Menu ---" + Style.RESET_ALL)
        print_menu(options)
        choice = input("Choose: ").strip()
        action = ACTIONS.get(choice)
        if not action:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            continue
        if action() == "BACK":
            break
