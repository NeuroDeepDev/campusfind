# CampusFind - Lost & Found Campus Platform

A full-stack web application to help students find lost items and return found items on campus.

## 🎯 Features

- **User Authentication**: JWT-based registration, login, email verification, and password reset
- **Item Reporting**: Report found or lost items with photos and details
- **Item Claims**: Students can claim items they lost; admins approve/reject claims
- **Search & Filter**: Search by name, category, location, or status
- **Admin Dashboard**: Manage claims, view audit logs, approve/reject claims
- **Audit Logging**: Track all claim approvals and status changes
- **Responsive UI**: Modern, mobile-friendly interface with Tailwind CSS
- **Docker Support**: Complete Docker & docker-compose setup for easy deployment
- **CI/CD**: GitHub Actions workflow for automated testing and builds

## 🏗️ Architecture

### Tech Stack

**Backend:**
- Django 4.2 + Django REST Framework
- JWT Authentication (simplejwt)
- SQLite (dev) / PostgreSQL (production)
- Gunicorn WSGI server

**Frontend:**
- React 18 with TypeScript
- Vite (fast build tool)
- Tailwind CSS (styling)
- React Router (routing)
- Axios (HTTP client)
- Zustand (state management)

**DevOps:**
- Docker & Docker Compose
- Nginx (reverse proxy)
- GitHub Actions (CI/CD)
- PostgreSQL 15 (production database)

## 📁 Project Structure

```
campusfind/
├── backend/                    # Django project root
│   ├── main_core/             # Django settings & URL config
│   ├── users/                 # User authentication app
│   ├── items/                 # Lost/found items app
│   ├── claims/                # Claims management app
│   ├── reports/               # Item reports app
│   ├── categories/            # Item categories
│   ├── locations/             # Campus locations
│   ├── audit/                 # Audit logging
│   ├── manage.py
│   ├── requirements.txt
│   └── tests/                 # Test files
├── frontend/                  # React app
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable components
│   │   ├── services/         # API client
│   │   ├── stores/           # State management
│   │   ├── styles/           # Global styles
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── sql/                       # Database schema & seed data
│   └── campusfind_schema_and_seed.sql
├── .github/workflows/         # CI/CD workflows
│   └── ci.yml
├── docker-compose.yml         # Multi-container setup
├── Dockerfile                 # Backend container
├── nginx.conf                 # Nginx reverse proxy
├── .env.example
└── README.md
```

## 🚀 Quick Start

### Local Development (without Docker)

#### Backend Setup

1. **Clone & navigate**
   ```bash
   git clone <repo-url>
   cd campusfind
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Load sample data**
   ```bash
   python manage.py load_sample_data
   ```

7. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start backend**
   ```bash
   python manage.py runserver
   ```

   Backend: http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Create .env.local**
   ```bash
   cp .env.example .env.local
   ```

4. **Start dev server**
   ```bash
   npm run dev
   ```

   Frontend: http://localhost:5173

### Docker Deployment

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop services
docker-compose down
```

Services:
- **Backend**: http://localhost:8000/api/
- **Frontend**: http://localhost:5173
- **Admin**: http://localhost:8000/admin/
- **Database**: PostgreSQL on localhost:5432

## 📚 API Documentation

### Available at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/users/` | Register new user |
| POST | `/api/token/` | Get JWT tokens |
| GET | `/api/items/` | List all items |
| POST | `/api/items/` | Create new item |
| GET | `/api/items/found_items/` | List found items |
| POST | `/api/claims/` | Create claim |
| GET | `/api/claims/pending/` | List pending claims (admin) |
| POST | `/api/claims/{id}/approve/` | Approve claim (admin) |
| GET | `/api/audit/` | View audit logs (admin) |

## 🔐 Authentication

### How JWT Works

1. **Login**: Send email/password → get access & refresh tokens
2. **Authenticated Requests**: Include `Authorization: Bearer <access_token>` header
3. **Token Refresh**: When access token expires, use refresh token to get new one
4. **Logout**: Clear tokens from client storage

### Token Storage Strategy

**Current Implementation**: Tokens stored in `localStorage`
- ✅ Easy to implement
- ❌ Vulnerable to XSS attacks

**Recommended for Production**:
- Use httpOnly cookies (backend sets, browser doesn't expose to JS)
- Implement CSRF protection
- Add token rotation

To implement httpOnly cookies, modify:
1. Backend: Set cookies in response instead of returning tokens
2. Frontend: Remove manual token management; browser handles cookie automatically
3. Axios: Configure to send cookies with requests

## 🗄️ Database Schema

### Tables
- **student**: Student user accounts
- **admin**: Administrator accounts
- **category**: Item categories (Electronics, Books, etc.)
- **location**: Campus locations/buildings
- **item**: Lost/found items
- **report**: Reports for items
- **claim**: Student claims on items
- **audit**: Audit log of actions

### Views
- **lost_items_view**: All lost items with details
- **student_history_view**: Student's reported items
- **unclaimed_found_items_view**: Found items with pending claims count

## 🧪 Running Tests

### Backend Tests
```bash
python manage.py test
```

### Frontend Tests
```bash
cd frontend
npm run test:unit
```

### CI/CD
Tests run automatically on push/PR to main/develop branches. See `.github/workflows/ci.yml`

## 📦 Environment Variables

### Backend (.env)

```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

# Database
DATABASE_URL=sqlite:///db.sqlite3
# For PostgreSQL: postgresql://user:pass@localhost/dbname

# Email (Gmail example)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@campusfind.com

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env.local)

```bash
VITE_API_URL=http://localhost:8000/api
```

## 🔧 Common Workflows

### Add New Item Type
1. Update SQL schema: Add to `item_type` enum
2. Backend: No change needed (already supports custom types)
3. Frontend: Update filter options

### Custom User Fields
1. Add field to `Student` model
2. Run migration: `python manage.py makemigrations`
3. Run migration: `python manage.py migrate`
4. Update serializers and forms

### Create Admin User
```bash
python manage.py createsuperuser
# Access at http://localhost:8000/admin/
```

### Reset Database
```bash
# Remove old database
rm db.sqlite3
# Migrate and seed
python manage.py migrate
python manage.py load_sample_data
```

## 🚢 Production Deployment

### Backend (Render/Heroku/Railway)

```bash
# Set environment variables in platform dashboard
# Run migrations on deploy
python manage.py migrate

# Use Gunicorn
gunicorn main_core.wsgi:application

# Collect static files
python manage.py collectstatic --noinput
```

### Frontend (Vercel/Netlify)

```bash
# Build
npm run build

# Deploy dist/ folder
# Set environment variables in platform dashboard:
# VITE_API_URL=https://your-backend.com/api
```

### Using PostgreSQL

1. **Backend**: Change `DATABASE_URL` to PostgreSQL connection string
2. **Update Django settings**: Already configured in settings.py
3. **Create database**: `createdb campusfind`
4. **Run migrations**: `python manage.py migrate`

### SSL/HTTPS

Uncomment HTTPS section in `nginx.conf` and provide certificates.

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push: `git push origin feature/amazing-feature`
4. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| Backend won't connect | Ensure Django running on 8000, check CORS settings |
| Can't login | Verify user exists in DB, check JWT_SECRET_KEY |
| 404 on API | Check URL routing in urls.py |
| Migrations conflict | Delete migrations, start fresh |
| CORS errors | Update CORS_ALLOWED_ORIGINS in .env |
| Docker build fails | Delete docker images, rebuild: `docker-compose build --no-cache` |

## 📞 Support

For issues or questions:
1. Check GitHub Issues
2. Review API documentation
3. Check logs: `docker-compose logs backend`

---

**Happy coding! 🎉**
