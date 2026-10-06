Music School Management System

Streamlit-based music school management application

The Music School Management System (MSMS) is a Python application for managing students, teachers, courses, lesson schedules and student attendance. The system uses a Streamlit graphical user interface and JSON file storage.

## Overview

This project provides a simple interface for common music school management tasks where users can view information on dashboard, register and search for students, view daily lessons, and check students into courses.

The project uses design from PST3 and extends it with a Streamlit GUI for PST4.

## Features

### Dashboard

The dashboard provides an overview of the system, including:
- Total number of students
-  Total number of teachers
- Total number of courses
- Navigation between the main system pages

### Student Management

The Student Management page allows users to:
- Register a new student
- Enter the student's name and instrument
- Automatically assign a student ID
- Search students by name, ID or instrument
- View registered student information

### Daily Roster

The Daily Roster page allows users to:
- Select a day of the week
- View lessons scheduled for that day
- View the course name, lesson time and room

### Student Check-in

The Student Check-in feature allows users to:
- Enter a student ID
- Enter a course ID
- Validate the student and course
- Record attendance with timestamp
- Display a success or error message

### Data Persistence

The system stores its data in:

data/msms.json

Student registration and attendance records are saved to the JSON file so that changes can persist after the application is closed.

## Project Structure

msms-project/
├─ app/
|    ├─ schedule.py
|    ├─ student.py
|    ├─ teacher.py
|    ∟ user.py
├─ data/
|    ∟ msms.json
├─ gui/
|    ├─ __init__.py
|    ├─ main_dashboard.py
|    ├─ student_pages.py
|    ∟  roster_pages.py
∟ main.py

app/

Contains the application's core classes and business logic.
- schedule.py contains the ScheduleManager, which manages students, teachers, courses, lessons and attendance.
- student.py defines the student class.
- teacher.py defines teacher and course class.
- user.py contains the base user class.

data/

Contains JSON data used by application.
- msms.json stores students, teachers, courses, lessons, attendance records and ID counters.

gui/

Contains the Streamlit user interface.
- main_dashboard.py controls the main dashboard and navigation.
- student_pages.py contains the Student Management page.
- roster_pages.py contains the Daily Roster and Student Check-in page.
- __init__.py identifies the directory as a Python package.

main.py
It launches the Streamlit dashboard.

## Installation and Setup

Requirements

The application requires:
- Python 3
- Streamlit
- Git (for version control)

Create and activate the virtual environment

From the project directory, create a virtual environment:
python -m venv .venv
Activate it in Git Bash:
source .venv/Scripts/activate

Install Streamlit

Install Streamlit using:
pip install streamlit

Running the Application

Make sure the virtual environment is activated and that you are in the project directory.
Run:
streamlit run main.py
Streamlit will start the application and provide a local URL, normally:
http://localhost:8501
Open the URL in a web browser to use the system.

## Testing the Application

1. Test the Dashboard

Open the application and select Dashboard from the sidebar.

Check that:
- The dashboard loads successfully.
- Student, teacher and course counts are displayed.
- Navigation options are available.

2) Test Student Management

Select Student Management
Test student registration by:
- Entering a student name.
- Entering an instrument.
- Selecting Register Student.
- Confirming that a success message and Student ID are displayed.
Test searching by entering a student's:
- Name
- ID
- Instrument

The displayed list should update according to the search term.

3) Test the Daily Roster

Select Daily Roster

Choose different days from the dropdown and check that scheduled lessons are displayed when lessons exist for that day.

4) Test Student Check-in
Enter a valid Student ID and Course ID and select Check-in Student.
A successful check-in should display a success message and save an attendance record.
An invalid Student ID or Course ID should display an error message.

## Design Choices and Assumptions

Separation of GUI and Business Logic

The Streamlit GUI is separated from the application's business logic. The classes in app/ are responsible for managing the underlying data and operations, while the files in gui/ are responsible for displaying and collecting information from the user.

ScheduleManager

ScheduleManager acts as the main controller for the system. GUI pages call its methods instead of directly modifying the underlying data.

Session State

Streamlit's st.session_state is used to keep the same ScheduleManager instance available while the user moves between pages.
This prevents the application from creating a new manager every time the user changes the sidebar selection.

JSON Storage

The existing JSON data structure is kept to store the data. This avoids using a database and keeps the system simple and consistent with the previous version.

Input Validation

The GUI checks that the registration fields are not empty before calling the registration method.
The check-in process validates that the supplied Student ID and Course ID exist before recording attendance.

Assumptions

- The Student IDs, Teacher IDs and Course IDs are positive integers.
- The existing JSON file contains the initial school data.
- Users operate the system through the Streamlit interface.
- The application is intended for local use rather than simultaneous multi-user access.