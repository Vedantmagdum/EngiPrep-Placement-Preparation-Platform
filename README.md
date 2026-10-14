EngiPrep – Placement Preparation Platform
========================================

EngiPrep is a web-based placement preparation platform developed using Flask, PostgreSQL, HTML, CSS, JavaScript, and Google Gemini AI.

The platform helps engineering students manage their placement preparation, practice aptitude questions, maintain student profiles, track test performance, and interact with an AI-powered preparation assistant.

PROJECT OVERVIEW
----------------

Project Title: EngiPrep – Placement Preparation Platform

Project Type: Group Mini-Project

Domain: Web Development and Artificial Intelligence

FEATURES
--------

1. STUDENT AUTHENTICATION

- Student signup and login
- Password hashing for secure password storage
- Session-based authentication
- Logout functionality

2. STUDENT PROFILE MANAGEMENT

Students can maintain their personal and academic information, including:

- Full name and email
- College name and branch
- Semester and CGPA
- Graduation year
- City and phone number
- LinkedIn and GitHub profiles
- Resume link
- Strengths and weaknesses
- Academic achievements

3. APTITUDE PREPARATION

The aptitude module helps students practice placement-oriented questions through multiple sections and topics.

- Multiple aptitude sections and topics
- Multiple-choice questions
- Automatically generated questions
- Question explanations
- Automatic score calculation
- Percentage calculation
- Test attempt history

4. AI-POWERED QUESTION GENERATION

Google Gemini AI is integrated to generate aptitude questions dynamically.

- Generates questions based on the selected section and topic
- Supports placement preparation practice
- Stores generated questions in PostgreSQL for reuse
- Helps reduce repeated question generation

5. AI-POWERED CHATBOT

EngiPrep includes an AI-powered preparation assistant that:

- Answers placement preparation questions
- Uses available student profile information
- Uses available aptitude performance data
- Provides personalized preparation guidance
- Maintains recent conversation context

6. STUDENT DASHBOARD

The dashboard provides an overview of the student's preparation activity and academic information.

- Student information overview
- CGPA and profile details
- Aptitude test performance
- Preparation activity tracking
- Test results and performance summaries

TECHNOLOGY STACK
----------------

Frontend:
- HTML5
- CSS3
- JavaScript
- Poppins Font

Backend:
- Python
- Flask

Database:
- PostgreSQL
- psycopg2

Artificial Intelligence:
- Google Gemini API

Development Tools:
- Visual Studio Code
- Git
- GitHub
- pgAdmin

Deployment:
- Render

PROJECT STRUCTURE
-----------------

EngiPrep/
|
|-- app.py
|-- config.py
|-- db.py
|-- api_service.py
|-- requirements.txt
|-- render.yaml
|-- .env
|-- .gitignore
|-- README.md
|
|-- database/
|   |-- schema.sql
|
|-- routes/
|   |-- auth.py
|   |-- profile.py
|   |-- dashboard.py
|   |-- aptitude.py
|   |-- chatbot.py
|
|-- templates/
|   |-- index.html
|   |-- login.html
|   |-- signup.html
|   |-- profile.html
|   |-- Dashboard.html
|   |-- Preparation.html
|
|-- static/
    |-- css/
    |-- js/
    |-- images/

DATABASE
--------

EngiPrep uses PostgreSQL to store student information, aptitude questions, test results, and preparation-related data.

Important database tables include:

- users
- student_profile
- skills
- student_skills
- skill_gap_analysis
- academics
- aptitude_sections
- aptitude_topics
- aptitude_questions
- aptitude_attempts
- aptitude_tests
- projects
- certificates
- internships
- companies
- job_applications
- competitions

The master database structure is maintained in:

database/schema.sql

INSTALLATION AND SETUP
----------------------

Prerequisites:

- Python
- PostgreSQL
- Git
- Visual Studio Code

Step 1: Clone the Repository

git clone https://github.com/Vedantmagdum/EngiPrep-Placement-Preparation-Platform

cd EngiPrep

Step 2: Create a Virtual Environment

python -m venv venv

Step 3: Activate the Virtual Environment

On Windows:

venv\Scripts\activate

Step 4: Install Dependencies

pip install -r requirements.txt

Step 5: Configure Environment Variables

Create a .env file in the project root directory and configure the required values.

SECRET_KEY=your_secret_key

DB_HOST=localhost
DB_PORT=5432
DB_NAME=project_database
DB_USER=postgres
DB_PASSWORD=your_postgresql_password

GEMINI_API_KEY=your_gemini_api_key

Replace the example values with your own local configuration.

Never upload actual passwords, API keys, or secret keys to GitHub.

Step 6: Create the Database

Create a PostgreSQL database named:

project_database

Create the required tables using the project's database schema and setup instructions.

Step 7: Run the Application

python app.py

Open the application in your browser:

http://127.0.0.1:5000

APPLICATION WORKFLOW
--------------------

Home Page
    |
    v
Student Signup / Login
    |
    v
Student Profile
    |
    v
Dashboard
    |
    v
Preparation Module
    |
    v
Select Aptitude Section and Topic
    |
    v
Practice Aptitude Questions
    |
    v
Automatic Score and Result Calculation
    |
    v
View Performance on Dashboard
    |
    v
Personalized AI Chatbot Assistance

SECURITY
--------

The project incorporates the following security practices:

- Password hashing
- Flask session-based authentication
- Environment variables for sensitive configuration
- Parameterized PostgreSQL queries
- Input validation

Important: The .env file contains sensitive credentials and must not be uploaded to GitHub. The .gitignore file should exclude .env and the virtual environment directory.

PROJECT TEAM
------------

Project Title: EngiPrep – Placement Preparation Platform

Project Type: Group Mini-Project

1. Vedant Magdum
Role: Project Lead,Database Design,Backend Development and Integration

Responsibilities:
- Led the development and integration of project modules.
- Worked on Flask backend functionality and application routes.
- Contributed to database schema and table organization.
- Contributed to student authentication and profile management.
- Worked on aptitude functionality, chatbot integration, and application deployment.

2. Suhan Patel
Role: Frontend Development and UI Design

Responsibilities:
- Worked on frontend development of the platform.
- Designed and developed user interface components.
- Contributed to HTML, CSS, and JavaScript implementation.
- Worked on visual layout and user experience.

3. Nilesh Lad
Role: Database Design and Management,Backend Development and Integration

Responsibilities:
- Worked on PostgreSQL database design and management.
- Contributed to database schema and table organization.
- Worked on Flask backend functionality and application routes.
- Worked on relationships between student, aptitude, and preparation data.
- Contributed to database structure and data storage.

4. Onkar Mane
Role: Testing, Documentation and Project Presentation

Responsibilities:
- Worked on application testing and verification.
- Helped document project features and implementation details.
- Contributed to identifying issues and checking application functionality.
- Prepared project presentation materials.

PROJECT LINKS
-------------

Live Application:
https://engiprep.onrender.com

GitHub Repository:
https://github.com/Vedantmagdum/EngiPrep-Placement-Preparation-Platform

FUTURE ENHANCEMENTS
-------------------

Possible future improvements include:

- Advanced skill-gap analysis
- Resume analysis and feedback
- Placement company recommendations
- Internship recommendations
- Additional aptitude categories
- Advanced student performance analytics
- Improved AI-based career guidance

CONCLUSION
----------

EngiPrep aims to provide engineering students with a centralized platform for placement preparation by combining aptitude practice, student profile management, performance tracking, and AI-powered assistance.

The project demonstrates the integration of frontend technologies, Python Flask, PostgreSQL, and Google Gemini AI into a collaborative web-based application.

Developed by the EngiPrep Project Team

Nilesh Lad | Suhan Patel | Vedant Magdum | Onkar Mane

EngiPrep – Placement Preparation Platform

Group Mini-Project for Placement Preparation and Career Development
