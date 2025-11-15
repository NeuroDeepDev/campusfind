# CampusFind Deployment Guide

Complete instructions for deploying CampusFind to production.

## Prerequisites

- Git
- Docker & Docker Compose
- Domain name
- SSL certificate (optional but recommended)
- Production database (PostgreSQL recommended)

## Option 1: Docker Deployment on VPS/Server

### 1. Prepare Server

```bash
# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### 2. Clone Repository

```bash
cd /opt
sudo git clone <your-repo-url> campusfind
cd campusfind
```

### 3. Configure Environment

```bash
# Create production .env
sudo cp .env.example .env
sudo nano .env
```

**Set these for production:**

```bash
DEBUG=False
SECRET_KEY=<generate-strong-key>
JWT_SECRET_KEY=<generate-strong-key>
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
CSRF_TRUSTED_ORIGINS=https://your-domain.com,https://www.your-domain.com

# PostgreSQL
DATABASE_URL=postgresql://campusfind:strong_password@db:5432/campusfind

# Email (use Gmail or SendGrid)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

CORS_ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 4. Generate Secret Keys

```bash
# Generate Django SECRET_KEY
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Generate JWT SECRET_KEY (same or different)
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Update docker-compose.yml for Production

```yaml
# Change:
# - DEBUG: "True" → DEBUG: "False"
# - SQLite → PostgreSQL
# - Gunicorn instead of runserver
```

### 6. Update nginx.conf for Production

```bash
# Uncomment HTTPS section
# Configure SSL certificate paths
# Uncomment HTTP to HTTPS redirect
```

### 7. Build and Deploy

```bash
# Build images
sudo docker-compose build

# Start services
sudo docker-compose up -d

# Run migrations
sudo docker-compose exec backend python manage.py migrate

# Load sample data (optional)
sudo docker-compose exec backend python manage.py load_sample_data

# Collect static files
sudo docker-compose exec backend python manage.py collectstatic --noinput

# Create superuser
sudo docker-compose exec backend python manage.py createsuperuser
```

### 8. SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com -d www.your-domain.com

# Update nginx.conf with certificate paths:
# /etc/letsencrypt/live/your-domain.com/fullchain.pem
# /etc/letsencrypt/live/your-domain.com/privkey.pem

# Auto-renew
sudo certbot renew --dry-run
```

### 9. Monitoring & Maintenance

```bash
# View logs
sudo docker-compose logs -f backend
sudo docker-compose logs -f frontend
sudo docker-compose logs -f nginx

# Database backup
sudo docker-compose exec db pg_dump -U campusfind campusfind > backup.sql

# Database restore
sudo cat backup.sql | docker-compose exec -T db psql -U campusfind campusfind

# Update code
cd /opt/campusfind
sudo git pull origin main
sudo docker-compose build
sudo docker-compose up -d
```

## Option 2: Render Deployment

### Backend

1. **Create New Web Service**
   - Connect GitHub repo
   - Environment: Python 3.11
   - Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start command: `gunicorn main_core.wsgi:application --bind 0.0.0.0:$PORT`

2. **Add Environment Variables**
   ```
   DEBUG=False
   SECRET_KEY=<generate-strong-key>
   JWT_SECRET_KEY=<generate-strong-key>
   DATABASE_URL=postgresql://...
   ALLOWED_HOSTS=*.onrender.com
   ```

3. **Add PostgreSQL**
   - Create PostgreSQL instance
   - Update DATABASE_URL

4. **Deploy**
   - Render will auto-deploy on push
   - Check logs in dashboard

### Frontend

1. **Create New Static Site**
   - Connect GitHub repo
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`

2. **Set Environment Variables**
   ```
   VITE_API_URL=https://your-backend.onrender.com/api
   ```

## Option 3: AWS Deployment

### ECS + RDS + CloudFront

1. **Push Docker images to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com
   
   docker tag campusfind:backend 123456789.dkr.ecr.us-east-1.amazonaws.com/campusfind:backend
   docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/campusfind:backend
   ```

2. **Create RDS PostgreSQL instance**
   - Database name: campusfind
   - Master username: campusfind
   - Store password securely

3. **Create ECS Cluster**
   - Task definition with backend image
   - Set DATABASE_URL environment variable

4. **CloudFront Distribution**
   - Origin: S3 bucket (for frontend)
   - Alternate domain: your-domain.com
   - SSL certificate from ACM

## Option 4: Heroku Deployment

```bash
# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set JWT_SECRET_KEY=your-jwt-secret

# Create Procfile (already in repo)

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

## Post-Deployment Checklist

- [ ] SSL/HTTPS configured
- [ ] Database backups scheduled
- [ ] Email notifications working
- [ ] Admin dashboard accessible
- [ ] User registration tested
- [ ] Item claiming workflow tested
- [ ] Audit logs tracking changes
- [ ] Error monitoring setup (Sentry)
- [ ] Performance monitoring (New Relic/DataDog)
- [ ] Auto-renewal of SSL certificates configured
- [ ] Database migrations run successfully
- [ ] Static files served correctly
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Security headers set

## Security Best Practices

1. **Secrets Management**
   - Never commit .env files
   - Use platform environment variables
   - Rotate keys regularly

2. **Database Security**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups
   - Restrict access

3. **API Security**
   - Enable rate limiting
   - Implement request validation
   - Use HTTPS only
   - Set security headers

4. **Frontend Security**
   - Enable CORS properly
   - Implement CSP headers
   - Sanitize user input
   - Update dependencies

5. **Monitoring**
   - Track failed logins
   - Monitor API errors
   - Log security events
   - Alert on anomalies

## Scaling Considerations

**Horizontal Scaling:**
- Use load balancer (ALB/NLB)
- Multiple backend instances
- Distributed session store (Redis)
- CDN for static/media files

**Database Scaling:**
- Read replicas
- Connection pooling
- Query optimization
- Archive old records

**Caching:**
- Redis for sessions
- Cache API responses
- Static asset caching
- Browser caching

## Troubleshooting Deployment

| Issue | Solution |
|-------|----------|
| 502 Bad Gateway | Check backend logs, verify port binding |
| Database connection | Verify DATABASE_URL, check firewall rules |
| Static files missing | Run collectstatic, check nginx config |
| CORS errors | Verify CORS_ALLOWED_ORIGINS setting |
| Slow performance | Check database queries, add caching |
| SSL certificate expired | Renew with Certbot or provider |

## Rollback Procedure

```bash
# Docker
sudo docker-compose down
sudo git checkout <previous-commit>
sudo docker-compose build
sudo docker-compose up -d

# Heroku
heroku releases
heroku rollback v<number>

# Render
Redeploy from previous commit via dashboard
```

## Support & Monitoring

- **Error Tracking**: Setup Sentry or Rollbar
- **Performance**: New Relic, DataDog, or AWS CloudWatch
- **Uptime Monitoring**: UptimeRobot, Pingdom
- **Log Aggregation**: ELK Stack, CloudWatch, Loggly

---

For more details, see README.md
