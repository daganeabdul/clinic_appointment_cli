Author
Made with ❤ by Abdirahman Dagane.

 Clinic Appointment CLI
 
A simple Command-Line Interface (CLI) application for managing clinic appointments.
 It allows patients to book appointments, doctors to view their schedules, and admins to manage clinic records.

 Features
 
 Patients can book appointments with doctors
 Doctors can view all their scheduled appointments
 Admins can view and manage patients, doctors, and appointments
 Simple SQLite database for storing records
 Runs entirely from the terminal (no internet required)

 Project Structure
 
clinic-appointment-cli/
│── main.py            │── database.py         
│── models.py         
│── requirements.txt 
│── README.md         
│── clinic.db          


Installation & Setup

Clone or Download this project

        [ git clone https://github.com/daganeabdul/clinic-appointment-cli.git](https://github.com/daganeabdul/clinic_appointment_cli.git)


         cd clinic-appointment-cli


Check Python Version (Python 3.8 or above recommended)

 python --version
 
Run the Application

      pipenv run python main.py



 The app will automatically create a clinic.db SQLite database on the first run.

 How to Use
 
1️ Patient
Choose Patient from the menu


Enter your name and select a doctor


Pick a date & time to book your appointment


2️ Doctor

Choose  Doctor from the menu


Enter your name


View all scheduled appointments with patient details


3️ Admin

Choose Admin from the menu


View all patients, doctors, and appointments


Future extension: Add/remove doctors, update patient info



 Tech Stack
 
Python 3 (Core logic)


SQLite3 (Database)


Standard Library Only (no external dependencies)



 Example Run
 
=== Clinic Appointment CLI ===

1. Patient
2. Doctor
3. Admin
4. Exit
Choose role: 1

--- Patient Menu ---

1. Register as new patient
2. Book an appointment
3. View my appointments
4. Back
Choose: 1
Name: zam
Age: 21
Gender: female
Contact info: zam@gmail.com
Registered Patient ID: 4

--- Patient Menu ---

1. Register as new patient
2. Book an appointment
3. View my appointments
4. Back
Choose: 


 







