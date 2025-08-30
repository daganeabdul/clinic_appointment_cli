 Author
 
Abdirahman Dagane

 Clinic Appointment CLI
 
A simple command-line interface (CLI) application for managing a clinic’s appointments, patients, and doctors.
 This project simulates how patients, doctors, and admins interact in a healthcare setting.

 Features
 
 Patients


Book appointments with doctors at a specific time.


 Doctors


View scheduled appointments.


 Admin


Manage patients, doctors, and appointments.


View all clinic records in an organized way.



 Tech Stack
 
Python 3 – Core programming language


SQLite3 – Database for storing patients, doctors, and appointments


CLI – Simple text-based interface



 Project Structure
clinic-appointment-cli/
│── main.py             │── database.py          │── models.py           Doctor, Appointment classes
│── clinic.db           │── README.md           



 How to Run
Clone this repository or create the files manually.

          https://github.com/daganeabdul/clinic_appointment_cli.git
cd clinic-appointment-cli


Run the program:

    pipenv run python main.py

Follow the menu prompts:


Choose whether you are Admin, Doctor, or Patient.


Perform actions like booking an appointment, viewing schedules, or managing records.



  Database Schema
  
The app uses SQLite3 with 3 tables:

Patients


id (Primary Key)


name


age


gender


Doctors


id (Primary Key)


name


specialization


Appointments


id (Primary Key)


patient_id (Foreign Key → Patients.id)


doctor_id (Foreign Key → Doctors.id)


date


time



  Example Workflow
Patient books appointment with Dr. Ali at 10:00 AM, 1st Sept 2025.


Doctor checks their schedule → sees appointment with Patient A.


Admin views all records → confirms patients, doctors, and appointments are stored correctly.




   ![clinic_appointment_cli ](cli.png)


