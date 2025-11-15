# CampusFind Quick Reference Guide

## 🚀 Start Developing in 5 Minutes

### Quick Start (Local Development)

```bash
# 1. Clone and navigate
git clone <repo-url>
cd campusfind

# 2. Setup Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# 3. Initialize Database
python manage.py migrate
python manage.py load_sample_data
python manage.py createsuperuser  # Create admin account

# 4. Start Backend
python manage.py runserver
# Backend: http://localhost:8000

# 5. In new terminal, Setup Frontend
cd frontend
npm install
npm run dev
# Frontend: http://localhost:5173
```

### Quick Start (Docker)

```bash
# One command to start everything
docker-compose up -d

# Services ready:
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000/api/
# Admin: http://localhost:8000/admin/
# Nginx: http://localhost:80
```

## 📚 Essential URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Django backend |
| http://localhost:8000/admin | Admin panel |
| http://localhost:8000/api/ | API root |
| http://localhost:8000/api/docs/ | Swagger documentation |
| http://localhost:5173 | React frontend |
| http://localhost | Nginx (Docker) |

## 👤 Test Credentials

**Superuser** (created during setup):
- Email: `admin@university.edu`
- Password: (set during setup)

**Sample Students** (pre-loaded):
- alice@university.edu
- bob@university.edu
- charlie@university.edu
- diana@university.edu

Password hint: Sample data uses hashed passwords. Reset with:
```bash
python manage.py shell
from users.models import Student
from django.contrib.auth.hashers import make_password
s = Student.objects.get(email='alice@university.edu')
s.password_hash = make_password('newpassword123')
s.save()
```

## 🔧 Common Commands

### Backend

```bash
# Create database
python manage.py migrate

# Load sample data
python manage.py load_sample_data

# Create admin
python manage.py createsuperuser

# Run tests
python manage.py test

# Start development server
python manage.py runserver

# Shell for debugging
python manage.py shell

# Collect static files
python manage.py collectstatic --noinput

# Make migrations
python manage.py makemigrations app_name
```

### Frontend

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint

# Run tests
npm run test:unit
```

### Docker

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Run backend command
docker-compose exec backend python manage.py <command>

# Access database
docker-compose exec db psql -U campusfind -d campusfind

# Rebuild images
docker-compose build --no-cache
```

## 🌐 API Quick Reference

### Authentication

```bash
# Register
POST /api/auth/users/
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "student_id": "STU001",
  "password": "securepass123",
  "password2": "securepass123"
}

# Login
POST /api/token/
{
  "email": "user@example.com",
  "password": "securepass123"
}
Response:
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}

# Refresh Token
POST /api/token/refresh/
{
  "refresh": "eyJ..."
}
```

### Items

```bash
# List all items
GET /api/items/

# List found items
GET /api/items/found_items/

# List lost items
GET /api/items/lost_items/

# Get my items
GET /api/items/my_items/

# Create item (authenticated)
POST /api/items/
{
  "name": "Lost Laptop",
  "description": "Silver Dell XPS 15",
  "category_id": 1,
  "location_id": 2,
  "item_type": "Lost",
  "status": "Lost"
}
```

### Claims

```bash
# Create claim (authenticated)
POST /api/claims/
{
  "item": 1,
  "claim_description": "This is my laptop"
}

# Get my claims
GET /api/claims/my_claims/

# Get pending claims (admin only)
GET /api/claims/pending/

# Approve claim (admin only)
POST /api/claims/{id}/approve/

# Reject claim (admin only)
POST /api/claims/{id}/reject/
```

## 📁 File Structure Reference

```
campusfind/
├── main_core/              Django settings
├── users/                 Student/Admin models
├── items/                 Item management
├── claims/                Claims workflow
├── reports/               Reports
├── categories/            Categories
├── locations/             Locations
├── audit/                 Audit logs
├── frontend/              React app
├── sql/                   Database schema
├── .env.example          Environment template
├── requirements.txt      Python packages
├── docker-compose.yml    Docker config
├── README.md             Main docs
├── README_BACKEND.md     Backend guide
├── DEPLOYMENT.md         Deployment guide
└── SETUP_VERIFICATION.md Setup checklist
```

## 🔐 Security Reminders

✓ Never commit `.env` files
✓ Use strong secrets (SECRET_KEY, JWT_SECRET_KEY)
✓ Enable HTTPS in production
✓ Update ALLOWED_HOSTS for production
✓ Change default superuser password
✓ Configure email service properly
✓ Keep dependencies updated
✓ Run security tests before deployment

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Kill process: `lsof -ti:8000 \| xargs kill -9` |
| Port 5173 in use | Kill process: `lsof -ti:5173 \| xargs kill -9` |
| Module not found | Run `pip install -r requirements.txt` or `npm install` |
| Migration errors | Delete db.sqlite3 and re-migrate |
| CORS errors | Check CORS_ALLOWED_ORIGINS in .env |
| API not responding | Ensure backend running: `python manage.py runserver` |
| Authentication fails | Check JWT tokens, verify SECRET_KEY |
| Database locked | Restart terminal/Python process |
| Docker won't start | Run `docker-compose build --no-cache` |

## 📊 Database Backup

```bash
# Export database
python manage.py dumpdata > backup.json

# Import database
python manage.py loaddata backup.json

# SQLite backup
cp db.sqlite3 db.sqlite3.backup

# Docker database backup
docker-compose exec db pg_dump -U campusfind campusfind > backup.sql
```

## 🚢 Quick Deployment

### To Render
1. Create `.env` on Render dashboard
2. Set build command: `pip install -r requirements.txt && python manage.py migrate`
3. Set start command: `gunicorn main_core.wsgi:application --bind 0.0.0.0:$PORT`
4. Deploy via git push

### To Heroku
```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
```

### To Docker VPS
```bash
# On server
git clone <repo>
cd campusfind
docker-compose up -d
# Access at your-domain.com
```

## 📞 Getting Help

1. Check **README.md** - General overview
2. Check **README_BACKEND.md** - Backend issues
3. Check **DEPLOYMENT.md** - Deployment issues
4. Check **SETUP_VERIFICATION.md** - Setup checklist
5. Review **API docs** - `http://localhost:8000/api/docs/`
6. Check **logs** - `docker-compose logs` or `python manage.py runserver`

## ✅ Development Checklist

Before committing:
- [ ] Tests pass: `python manage.py test`
- [ ] Lint passes: `npm run lint`
- [ ] No console errors
- [ ] `.env` not committed
- [ ] Migrations created: `python manage.py makemigrations`
- [ ] Database updated: `python manage.py migrate`

Before deploying:
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS`
- [ ] Update `CORS_ALLOWED_ORIGINS`
- [ ] Set strong `SECRET_KEY`
- [ ] Configure email service
- [ ] Test on staging environment
- [ ] Backup database
- [ ] Review security settings

---

**Quick Links**: [README.md](README.md) | [Backend Guide](README_BACKEND.md) | [Deployment](DEPLOYMENT.md) | [Setup Verification](SETUP_VERIFICATION.md)

**Need help?** See the troubleshooting sections in main README.md
