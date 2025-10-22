# PetRescue Deployment Guide

This guide covers deploying the PetRescue application to production environments.

## 🚀 Production Deployment

### Prerequisites

- Python 3.8+
- Web server (Apache/Nginx)
- Database server (MySQL/PostgreSQL)
- SSL certificate for HTTPS

### Environment Setup

1. **Create production settings file**
   ```python
   # settings_production.py
   from .settings import *
   
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
   
   # Database configuration
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'petrescue_db',
           'USER': 'petrescue_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   
   # Static and media files
   STATIC_ROOT = '/var/www/petrescue/static/'
   MEDIA_ROOT = '/var/www/petrescue/media/'
   
   # Security settings
   SECURE_SSL_REDIRECT = True
   SECURE_HSTS_SECONDS = 31536000
   SECURE_HSTS_INCLUDE_SUBDOMAINS = True
   SECURE_HSTS_PRELOAD = True
   SESSION_COOKIE_SECURE = True
   CSRF_COOKIE_SECURE = True
   
   # Email configuration
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.your-provider.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'noreply@your-domain.com'
   EMAIL_HOST_PASSWORD = 'email_password'
   ```

2. **Install production dependencies**
   ```bash
   pip install gunicorn
   pip install mysqlclient  # or psycopg2 for PostgreSQL
   ```

3. **Collect static files**
   ```bash
   python manage.py collectstatic --settings=petrescue.settings_production
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate --settings=petrescue.settings_production
   ```

### Web Server Configuration

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location /static/ {
        alias /var/www/petrescue/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    location /media/ {
        alias /var/www/petrescue/media/;
        expires 1y;
        add_header Cache-Control "public";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Gunicorn Service
```ini
# /etc/systemd/system/petrescue.service
[Unit]
Description=PetRescue Django Application
After=network.target

[Service]
User=petrescue
Group=petrescue
WorkingDirectory=/var/www/petrescue
Environment="DJANGO_SETTINGS_MODULE=petrescue.settings_production"
ExecStart=/var/www/petrescue/venv/bin/gunicorn petrescue.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

### Database Setup

#### MySQL
```sql
CREATE DATABASE petrescue_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'petrescue_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON petrescue_db.* TO 'petrescue_user'@'localhost';
FLUSH PRIVILEGES;
```

### Security Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use HTTPS with SSL certificate
- [ ] Set secure cookie flags
- [ ] Configure HSTS headers
- [ ] Use strong database passwords
- [ ] Set up regular backups
- [ ] Configure firewall rules
- [ ] Keep dependencies updated

### Monitoring and Maintenance

1. **Log Configuration**
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'level': 'INFO',
               'class': 'logging.FileHandler',
               'filename': '/var/log/petrescue/django.log',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['file'],
               'level': 'INFO',
               'propagate': True,
           },
       },
   }
   ```

2. **Database Backups**
   ```bash
   # Daily backup script
   #!/bin/bash
   DATE=$(date +%Y%m%d_%H%M%S)
   mysqldump -u petrescue_user -p petrescue_db > /backups/petrescue_$DATE.sql
   find /backups -name "petrescue_*.sql" -mtime +7 -delete
   ```

3. **Health Checks**
   - Monitor application logs
   - Check database performance
   - Monitor disk space for media files
   - Set up uptime monitoring

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "petrescue.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=mysql://user:password@db:3306/petrescue
    depends_on:
      - db
    volumes:
      - media_volume:/app/media

  db:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=petrescue
      - MYSQL_USER=petrescue_user
      - MYSQL_PASSWORD=secure_password
      - MYSQL_ROOT_PASSWORD=root_password
    volumes:
      - db_data:/var/lib/mysql

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - media_volume:/var/www/media
    depends_on:
      - web

volumes:
  db_data:
  media_volume:
```

## ☁️ Cloud Deployment

### Heroku
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn petrescue.wsgi
   ```
3. Add `django-heroku` to requirements.txt
4. Configure settings for Heroku
5. Deploy:
   ```bash
   heroku create petrescue-app
   git push heroku main
   heroku run python manage.py migrate
   ```

### AWS/DigitalOcean
- Use managed database services
- Configure S3 for static/media files
- Set up load balancers for high availability
- Use CDN for static content delivery

## 🔧 Performance Optimization

1. **Database Optimization**
   - Add database indexes
   - Use database connection pooling
   - Implement query optimization

2. **Caching**
   - Configure Redis/Memcached
   - Implement view caching
   - Cache database queries

3. **Static Files**
   - Use CDN for static files
   - Enable gzip compression
   - Set proper cache headers

4. **Image Optimization**
   - Compress uploaded images
   - Generate thumbnails
   - Use WebP format when possible

## 📊 Monitoring

- Set up application monitoring (New Relic, DataDog)
- Configure error tracking (Sentry)
- Monitor server resources
- Set up alerts for critical issues

## 🔄 Backup and Recovery

1. **Database Backups**
   - Automated daily backups
   - Test restore procedures
   - Off-site backup storage

2. **Media Files**
   - Regular media file backups
   - Version control for code
   - Document recovery procedures

## 📞 Support

For deployment issues:
- Check application logs
- Verify database connectivity
- Test static file serving
- Validate SSL certificate
- Monitor server resources