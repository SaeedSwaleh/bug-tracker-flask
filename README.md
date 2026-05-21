# Bug Tracker – Full‑Stack Flask App on AWS

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-lightgrey.svg)](https://flask.palletsprojects.com/)
[![AWS RDS](https://img.shields.io/badge/AWS-RDS-orange.svg)](https://aws.amazon.com/rds/)
[![AWS EC2](https://img.shields.io/badge/AWS-EC2-orange.svg)](https://aws.amazon.com/ec2/)

**Live demo:** [http://13.61.33.248:5000](http://13.61.33.248:5000) – *HTTP only for demonstration.*

A production‑ready bug tracking system with user authentication, team assignment, and comments. Built with Flask, PostgreSQL (AWS RDS), and deployed on AWS EC2 with systemd.

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
   