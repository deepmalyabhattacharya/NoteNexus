#  Note taking Web application "NoteNexus"

#### Video Demo: <[Demo]](https://youtu.be/jifM0qNgoyA))>

---

#### Project Description:
A Flask-based web app where users register, log in, and manage personal notes — create, edit, and delete notes using SQLite.It is built with HTML, CSS, and JavaScript for a clean, responsive interface.The web application ensures secure authentication and smooth CRUD operations using Flask and SQLite

---

#### Project Overview:

This project is a Note Taking Web Application built as my final submission for CS50’s Introduction to Computer Science course. The goal of this project is to create a simple yet powerful web app that allows users to register, log in, and manage personal notes in a secure and user-friendly environment.

The application enables users to:

Register for an account

Log in securely

Create new notes

Edit existing notes

Delete notes they no longer need

It is built using Flask for the backend, SQLite for the database, and HTML, CSS, and JavaScript for the frontend. This project demonstrates my understanding of web development, databases, CRUD operations, and authentication.
---
####  Prjoect Structure:
│
├── static/
│   ├── statics.js          # JavaScript for client-side interactivity
│   └── styles.css          # Custom styling for the web app
│
├── templates/
│   ├── layout.html         # Base HTML layout (header, footer, etc.)
│   ├── index.html          # Main page displaying user’s notes
│   ├── login.html          # Login form page
│   └── register.html       # Registration form page
│
├── app.py                  # Main Flask application file
├── project.db              # SQLite database storing users and notes
├── README.md               # Documentation file
└── requirements.txt        # Python dependencies

---
####  Technologies Used:
- **Frontend**

HTML5 – Defines the structure of the web pages.

CSS3 – Provides styling for a clean and responsive design.

JavaScript (statics.js) – Adds dynamic behavior, such as editing notes without full page reloads.

- **Backend**

Python (Flask Framework) – Handles routing, user sessions, and database communication.

Jinja2 Templates – Enables dynamic content rendering on HTML pages.

- **Database**

SQLite – A lightweight relational database used to store user credentials.

---
####  Features:
1. - **User Authentication**

The application includes a complete login and registration system:

New users can register using a username and password.

Passwords are securely hashed before being stored in the database.

Returning users can log in and access their personal notes.

Flask sessions are used to keep users logged in across requests.

2. - **Creating Notes**

After logging in, users are redirected to the main page (index.html).
Here, users can:

Create new notes by entering text into a form.

Notes are displayed immediately.

3. - **Editing Notes**

Each note can be edited.
When a user clicks on the Edit button:

The note content becomes editable.

After editing, the user can save changes, which updates the note in the database.

4. - **Delete notes**

Users can delete notes with a single click.

---
####  File Descriptions:

- **app.py**
This is the core of the project — the Flask application file.
It contains:

Route definitions for /login, /register, /logout, and /.

Logic for user authentication and session management.

CRUD operations for creating, reading, updating, and deleting notes.

Integration with the SQLite database.

- **project.db**
The SQLite database file with one primary table
user – Stores user credentials (id, username, hashed password).

- **template/**
Contains HTML files rendered by Flask:

layout.html – Defines the general structure (navigation bar).

index.html – Displays the list of notes and note management buttons.

login.html – Login form.

register.html – Registration form.

- **static/**
Holds static files such as JavaScript and CSS:

statics.js – Handles client-side functionality like editing/deleting notes dynamically.

styles.css – Adds styling and layout to the web pages.

- **requirements.text**
cs50
flask
flask_session
werkzeug.security
functools
os
secrets

---

#### Future Improvements:

Implementation of AI (for voice to text)

Exportation of notes in the form of pdf

Better user Authentication

Having custom mode settings


---

####  Usage:

1. Run the program in the terminal:

```bash
python project.1. Clone the repository
git clone https://github.com/deepmalyabhattacharya/NoteNexus.git
cd NoteNexus

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate

3. Install dependencies

```bash
pip install -r requirements.txt

4. Run the Flask app

```bash
flask run


or

```bash
python app.py

5. Open in browser

Visit: http://127.0.0.1:5000
