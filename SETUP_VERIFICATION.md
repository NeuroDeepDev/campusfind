# CampusFind Setup Verification Checklist

Use this checklist to verify that all components are properly set up and working.

## Backend Setup Verification

### Django Installation
- [ ] Python 3.11+ installed (`python --version`)
- [ ] Virtual environment created and activated
- [ ] `requirements.txt` installed (`pip install -r requirements.txt`)
- [ ] Django installed (`python -m django --version`)
- [ ] DRF installed (`pip show djangorestframework`)

### Database Setup
- [ ] Migrations created (`python manage.py makemigrations`)
- [ ] Migrations applied (`python manage.py migrate`)
- [ ] `db.sqlite3` file created
- [ ] Sample data loaded (`python manage.py load_sample_data`)
- [ ] Can access SQLite database directly

### Superuser & Admin
- [ ] Superuser created (`python manage.py createsuperuser`)
- [ ] Can login to Django admin (`http://localhost:8000/admin/`)
- [ ] All models visible in admin panel:
  - [ ] Students
  - [ ] Admins
  - [ ] Categories
  - [ ] Locations
  - [ ] Items
  - [ ] Reports
  - [ ] Claims
  - [ ] Audit logs

### API Endpoints
- [ ] Backend running (`python manage.py runserver`)
- [ ] API accessible at `http://localhost:8000/api/`
- [ ] Can access swagger docs (`http://localhost:8000/api/docs/`)
- [ ] Can access ReDoc (`http://localhost:8000/api/redoc/`)

### API Testing
- [ ] Register endpoint works (POST `/api/auth/users/`)
- [ ] Login endpoint works (POST `/api/token/`)
- [ ] Token refresh works (POST `/api/token/refresh/`)
- [ ] Can get current user (GET `/api/users/students/me/`)
- [ ] Can list items (GET `/api/items/`)
- [ ] Can create item (POST `/api/items/`)
- [ ] Can create claim (POST `/api/claims/`)
- [ ] Can approve claim (admin only)
- [ ] Can view audit logs (admin only)

### Configuration
- [ ] `.env` file created from `.env.example`
- [ ] `SECRET_KEY` set
- [ ] `JWT_SECRET_KEY` set
- [ ] `DEBUG=True` for development
- [ ] `ALLOWED_HOSTS` configured
- [ ] `CORS_ALLOWED_ORIGINS` includes frontend URL
- [ ] Email backend configured (console for dev)

## Frontend Setup Verification

### Node.js & npm
- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Working in `frontend/` directory

### Dependencies
- [ ] `package.json` exists
- [ ] Dependencies installed (`npm install`)
- [ ] `node_modules/` directory created
- [ ] React installed (`npm list react`)
- [ ] React Router installed
- [ ] Axios installed
- [ ] Tailwind CSS installed

### Configuration
- [ ] `.env.local` created from `.env.example`
- [ ] `VITE_API_URL` points to backend (`http://localhost:8000/api`)
- [ ] `vite.config.ts` configured
- [ ] `tailwind.config.js` exists
- [ ] `tsconfig.json` configured

### Build & Dev Server
- [ ] Dev server starts (`npm run dev`)
- [ ] Dev server accessible at `http://localhost:5173`
- [ ] Frontend loads without errors
- [ ] No console errors on page load

### Features Testing
- [ ] Can navigate to login page
- [ ] Can navigate to register page
- [ ] Can open search page
- [ ] Tailwind CSS styling applied (colors, responsive design)
- [ ] Navigation links work

## Integration Testing

### Authentication Flow
- [ ] Register new user
- [ ] Receive verification email (check console)
- [ ] Login with credentials
- [ ] JWT tokens stored in localStorage
- [ ] Can access protected pages
- [ ] Logout clears tokens

### Item Management
- [ ] Can view found items list
- [ ] Can view lost items list
- [ ] Can view item details
- [ ] Can create new item (authenticated)
- [ ] Can upload evidence file
- [ ] File appears in media directory

### Claiming Flow
- [ ] Can view unclaimed items
- [ ] Can create claim on found item
- [ ] Claim appears in "my claims"
- [ ] Admin can view pending claims
- [ ] Admin can approve claim
- [ ] Item status changes to "Returned"
- [ ] Audit log created

### Search & Filter
- [ ] Can search items by name
- [ ] Can search items by description
- [ ] Can filter by type (Found/Lost)
- [ ] Results update in real-time
- [ ] Can clear search

## Docker Verification (Optional)

### Docker Installation
- [ ] Docker installed (`docker --version`)
- [ ] Docker daemon running
- [ ] Docker Compose installed (`docker-compose --version`)

### Build & Run
- [ ] Backend image builds (`docker-compose build backend`)
- [ ] Frontend image builds (`docker-compose build frontend`)
- [ ] Services start (`docker-compose up -d`)
- [ ] No errors in logs (`docker-compose logs`)

### Container Access
- [ ] Backend accessible at `http://localhost:8000`
- [ ] Frontend accessible at `http://localhost:5173`
- [ ] Nginx accessible at `http://localhost`
- [ ] Database accessible (`docker-compose exec db psql -U campusfind`)

### Database Initialization
- [ ] Database container running
- [ ] Migrations run automatically
- [ ] Sample data loaded
- [ ] Can connect to database

## Performance & Security Checks

### Backend
- [ ] Response times < 200ms
- [ ] Pagination working (20 items per page)
- [ ] CORS headers present
- [ ] Security headers set
- [ ] Password hashing working
- [ ] Token expiration working (60 min for access, 7 days for refresh)

### Frontend
- [ ] Page loads < 2s
- [ ] No 404 errors
- [ ] No console errors
- [ ] Network requests working
- [ ] Token refresh on 401
- [ ] Protected routes accessible only when authenticated

## Deployment Readiness

### Code Quality
- [ ] No syntax errors
- [ ] No import errors
- [ ] No console warnings
- [ ] Tests pass (`python manage.py test`)
- [ ] Linting passes (if configured)

### Configuration
- [ ] All environment variables documented
- [ ] Secrets not in version control
- [ ] `.env` file in `.gitignore`
- [ ] Production settings prepared

### Documentation
- [ ] README.md complete and accurate
- [ ] API endpoints documented
- [ ] Setup instructions clear
- [ ] Troubleshooting guide provided

### Files Present
- [ ] `.env.example` present
- [ ] `.gitignore` configured
- [ ] `requirements.txt` updated
- [ ] `docker-compose.yml` present
- [ ] `Dockerfile` present
- [ ] `nginx.conf` present
- [ ] `.github/workflows/ci.yml` present

## Common Issues & Fixes

### Backend Won't Start
- [ ] Check Python version (3.11+)
- [ ] Check if port 8000 is free
- [ ] Run migrations: `python manage.py migrate`
- [ ] Check `.env` variables

### Frontend Won't Load
- [ ] Check Node.js version (18+)
- [ ] Run `npm install` again
- [ ] Check if port 5173 is free
- [ ] Clear browser cache
- [ ] Check console for errors

### API Connection Issues
- [ ] Verify backend is running
- [ ] Check CORS settings in Django
- [ ] Verify frontend VITE_API_URL
- [ ] Check browser console network tab

### Database Issues
- [ ] Delete `db.sqlite3` and re-migrate
- [ ] Run `python manage.py migrate --run-syncdb`
- [ ] Check database permissions
- [ ] Verify migrations are applied

## Final Checklist

- [ ] All items above checked
- [ ] No critical errors in logs
- [ ] All tests passing
- [ ] Ready for development
- [ ] Ready for staging/production deployment

---

## Next Steps

If all checks pass:
1. ✅ **Development**: Start building features
2. ✅ **Testing**: Run unit and integration tests
3. ✅ **Deployment**: Follow DEPLOYMENT.md guide
4. ✅ **Production**: Configure SSL, email, backups

If any checks fail:
1. ❌ Review relevant section in README or DEPLOYMENT docs
2. ❌ Check troubleshooting guide
3. ❌ Review console/server logs
4. ❌ Verify file permissions
5. ❌ Check firewall settings

---

**Date Completed**: ____________  
**Checked By**: ____________  
**Ready for Deployment**: ☐ Yes ☐ No

If "No", list remaining issues:
1. ___________________________
2. ___________________________
3. ___________________________
