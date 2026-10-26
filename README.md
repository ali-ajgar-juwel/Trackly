# Trackly — Bug & Issue Tracker

A responsive Django bug tracker with projects, issue lifecycle, assignment, comments, notifications, search/filtering and REST API.

## Run on Windows PowerShell
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py makemigrations tracker
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open http://127.0.0.1:8000/ . Admin: /admin/ . API: /api/projects/, /api/bugs/, /api/comments/.

SQLite is used for simple local setup. Before production, change SECRET_KEY, DEBUG, ALLOWED_HOSTS, review permissions and configure HTTPS.
