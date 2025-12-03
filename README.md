# CampusFind (Minimal)

This is a minimal Django project implementing the CampusFind schema with a simple HTML/CSS/JS frontend.

Run locally (recommended steps):

1. Create a virtualenv and install deps:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Apply migrations and load fixtures:

```bash
python manage.py migrate
python manage.py loaddata core/fixtures/initial_data.json
```

3. Run server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.
# CampusFind

Fresh start workspace.
