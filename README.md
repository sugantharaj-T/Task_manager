# TaskFlow Django Task Manager

TaskFlow is a Django and SQL-backed task-management frontend for projects, task workflows, kanban boards, schedules, reports, comments, profiles and authentication screens.

## Features Included

- User registration, login, logout and password reset screens
- Profile page with role, department, designation and assigned tasks
- Project list, search, status filtering and project creation
- Task list, creation, priority/status/assignee filters and task detail pages
- Kanban workflow for To Do, In Progress, Review, Done and Blocked
- Calendar-style upcoming deadline timeline
- Reporting dashboard for completion, overdue tasks, status and priority metrics
- SQL models for projects, tasks, sprints, comments, attachments and activity logs

## Run Locally

Install Python first if it is not already installed, then run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

Demo login after seeding:

- Username: `manager`
- Password: `manager123`

## PostgreSQL

The project uses SQLite by default for easy local setup. To use PostgreSQL, replace `DATABASES` in `taskmanager/settings.py` with your PostgreSQL connection details.
