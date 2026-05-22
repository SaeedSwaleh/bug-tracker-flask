[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey.svg)](https://flask.palletsprojects.com)
[![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20RDS-orange.svg)](https://aws.amazon.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://postgresql.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Live Demo](https://img.shields.io/badge/demo-online-green.svg)](http://13.61.33.248:5000)

# Bug Tracker – Full-Stack Flask App on AWS

A production-ready bug tracking system with user authentication, team assignment, and comments. Built with Flask, PostgreSQL (AWS RDS), and deployed on AWS EC2 with systemd.

**Live demo:** [http://13.61.33.248:5000](http://13.61.33.248:5000)

---

## Who is this project for?

This project is suited for software development teams who need a simple, lightweight way to track bugs. It's great for small startups, student projects, or internal team use where you don't want to pay for expensive tools like Jira.

---

## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Real-time bug statistics and recent activity*

### Bug List
![Bug List](screenshots/bug-list.png)
*Filterable bug list with assignment column*

### Bug Detail with Comments
![Bug Detail](screenshots/bug-detail.png)
*Comment threads and status updates*

### Assignment Filter
![Assignment Filter](screenshots/assignment-filter.png)
*Filter bugs assigned to you*

### Login Page
![Login](screenshots/login-form.png)
*Secure authentication with Flask-Login*

### Signup Page
![Signup](screenshots/signup-form.png)
*Easy account creation*

---

## Features

- **User authentication** – signup, login, logout, password hashing.
- **Bug lifecycle** – create, list, view details, update status (Open / In Progress / Closed).
- **Team assignment** – assign bugs to other users, filter by "Assigned to me".
- **Comment threads** – add, delete, and view comments on each bug.
- **Dashboard** – real‑time counts of open, in‑progress, closed, and assigned bugs.
- **RESTful routes** – clean URL design with Flask.
- **Deployed on AWS** – EC2 (t3.micro) + RDS PostgreSQL (free tier).

---

## Tech Stack

| Layer        | Technology |
|--------------|------------|
| Backend      | Flask (Python) |
| Database     | PostgreSQL (AWS RDS) |
| ORM          | SQLAlchemy |
| Frontend     | HTML, Bootstrap 5, Jinja2 |
| Auth         | Flask‑Login |
| Deployment   | AWS EC2, Gunicorn, systemd |
| Version Ctrl | Git + GitHub |

---

## Local Development Setup

1. **Clone the repo**  
   ```bash
   git clone https://github.com/SaeedSwaleh/bug-tracker-flask.git
   cd bug-tracker-flask
