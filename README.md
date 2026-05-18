# Bug Tracker

A full-stack web application for tracking software bugs, built with Flask and AWS.

## Status
🚧 **In Progress** - Building user authentication

## Features (Coming)
- [ ] User signup/login
- [ ] Create, edit, delete bug tickets
- [ ] Assign bugs to users
- [ ] Update status (Open → In Progress → Closed)
- [ ] Add comments to bugs

## Tech Stack
- Backend: Flask (Python)
- Database: SQLite (→ moving to AWS RDS PostgreSQL)
- Authentication: Flask-Login
- Frontend: Bootstrap 5

## Setup
```bash
git clone https://github.com/SaeedSwaleh/bug-tracker-flask.git
cd bug-tracker-flask
pip install -r requirements.txt
python app.py