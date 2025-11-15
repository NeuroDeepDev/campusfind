# CampusFind Backend

## Setup Instructions

### Prerequisites
- Python 3.11+
- pip
- Virtual environment

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd campusfind
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Load sample data**
   ```bash
   python manage.py load_sample_data
   ```

7. **Create superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at: `http://localhost:8000/api/`

### API Documentation

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

### Project Structure

```
campusfind/
├── main_core/           # Django settings & urls
├── users/               # User management (Student & Admin)
├── categories/          # Item categories
├── locations/           # Campus locations/buildings
├── items/               # Lost/found items
├── reports/             # Item reports
├── claims/              # Item claims
├── audit/               # Audit logs
├── sql/                 # Database schema & seed data
├── media/               # User uploads
├── staticfiles/         # Static files
├── manage.py
├── requirements.txt
├── .env.example
└── README.md
```

### Key Endpoints

#### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/auth/users/` - Register new user
- `POST /api/auth/users/activation/` - Activate user email
- `POST /api/auth/users/reset_password/` - Request password reset

#### Users
- `GET /api/users/students/` - List all students
- `GET /api/users/students/{id}/` - Get student details
- `GET /api/users/students/me/` - Get current user profile
- `PUT /api/users/students/update_profile/` - Update profile

#### Items
- `GET /api/items/` - List all items
- `POST /api/items/` - Create new item
- `GET /api/items/found_items/` - List found items
- `GET /api/items/lost_items/` - List lost items
- `GET /api/items/my_items/` - List my items

#### Claims
- `GET /api/claims/` - List claims
- `POST /api/claims/` - Create new claim
- `GET /api/claims/my_claims/` - Get my claims
- `GET /api/claims/pending/` - Get pending claims (admin only)
- `POST /api/claims/{id}/approve/` - Approve claim (admin only)
- `POST /api/claims/{id}/reject/` - Reject claim (admin only)

#### Reports
- `GET /api/reports/` - List reports
- `POST /api/reports/` - Create report
- `GET /api/reports/my_reports/` - Get my reports

#### Audit
- `GET /api/audit/` - List audit logs (admin only)
- `GET /api/audit/by_action/` - Filter by action
- `GET /api/audit/claim_history/` - Get claim history

### Running Tests

```bash
python manage.py test
```

### Docker Deployment

```bash
docker-compose up -d
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | (required) |
| `DEBUG` | Debug mode | `True` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |
| `JWT_SECRET_KEY` | JWT signing key | (uses SECRET_KEY) |
| `EMAIL_BACKEND` | Email backend | `console.EmailBackend` |
| `DATABASE_URL` | Database URL | `sqlite:///db.sqlite3` |

### Production Deployment

1. Set `DEBUG=False`
2. Update `ALLOWED_HOSTS` with production domain
3. Use PostgreSQL instead of SQLite
4. Set strong `SECRET_KEY` and `JWT_SECRET_KEY`
5. Use SMTP email backend with valid credentials
6. Run `collectstatic`: `python manage.py collectstatic`
7. Use Gunicorn: `gunicorn main_core.wsgi:application`

### Authentication Notes

- JWT tokens are used for API authentication
- Access tokens valid for 60 minutes
- Refresh tokens valid for 7 days
- Include `Authorization: Bearer <token>` header for authenticated requests
- Tokens are NOT stored in httpOnly cookies by default; frontend should store in localStorage or sessionStorage
- For enhanced security, implement custom JWT backend to store tokens in httpOnly cookies

### Common Issues

**Import errors for rest_framework**: Install requirements.txt
**Database locked**: Delete `db.sqlite3` and re-run migrations
**Permission denied on migrations**: Run `python manage.py migrate --run-syncdb`
