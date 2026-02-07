# Deployment Guide

This guide covers deploying Resume Agent to production.

## Prerequisites

- Docker and Docker Compose installed on the server
- Domain name (optional but recommended)
- SSL certificate (for HTTPS)
- Database backup strategy

## Production Environment Variables

Create a `.env` file for production with secure values:

```env
# Application
APP_VERSION=1.0.0
DEBUG=false

# Database
POSTGRES_DB=resume_agent
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<strong_password>
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# JWT Authentication
JWT_ALG=HS256
JWT_SECRET=<strong_random_secret>
JWT_EXP=00:15:00.000000
JWT_REFRESH_TOKEN_EXP=30d,00:00:00.000000

SECURE_COOKIES=true
```

**Important:** Generate strong, random secrets for JWT tokens. Never use default or weak secrets in production.

## Docker Compose Production Setup

### 1. Create Production Docker Compose File

Create `docker-compose.yml` for production:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - JWT_SECRET=${JWT_SECRET}
      - JWT_EXP=${JWT_EXP}
      - JWT_REFRESH_TOKEN_EXP=${JWT_REFRESH_TOKEN_EXP}
      - SECURE_COOKIES=${SECURE_COOKIES}
      - DEBUG=false
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "8000:8000"
    restart: unless-stopped
    volumes:
      - ./backend:/app
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000

volumes:
  postgres_data:
```

### 2. Build and Start Services

```bash
docker compose up -d --build
```

### 3. Run Migrations

```bash
docker compose exec backend alembic upgrade head
```

## Reverse Proxy Setup (Nginx)

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## SSL Certificate Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already set up by Certbot)
```

## Database Backups

### Automated Backup Script

Create a backup script:

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/resume_agent_$DATE.sql"

docker compose exec -T postgres pg_dump -U postgres resume_agent > $BACKUP_FILE

# Keep only last 7 days of backups
find $BACKUP_DIR -name "resume_agent_*.sql" -mtime +7 -delete
```

### Schedule Backups with Cron

```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

## Monitoring

### Health Checks

Monitor the health endpoint:

```bash
curl https://your-domain.com/health
```

### Logs

View application logs:

```bash
docker compose logs -f backend
```

View database logs:

```bash
docker compose logs -f postgres
```

## Security Checklist

- [ ] Use strong, random secrets for JWT tokens
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set `DEBUG=false` in production
- [ ] Use secure database passwords
- [ ] Enable firewall rules
- [ ] Set up regular database backups
- [ ] Monitor application logs
- [ ] Keep Docker images updated
- [ ] Use non-root user in containers
- [ ] Enable rate limiting (via Nginx or application)

## Scaling

### Horizontal Scaling

To scale the backend:

```yaml
services:
  backend:
    # ... existing config ...
    deploy:
      replicas: 3
```

### Load Balancer

Use a load balancer (Nginx, HAProxy) to distribute traffic across multiple backend instances.

## Troubleshooting

### Application Won't Start

1. Check logs: `docker compose logs backend`
2. Verify environment variables
3. Check database connection
4. Verify migrations are up to date

### Database Connection Issues

1. Verify database is running: `docker compose ps`
2. Check database credentials
3. Verify network connectivity
4. Check database logs

### Performance Issues

1. Monitor resource usage
2. Check database query performance
3. Review application logs
4. Consider scaling

## Rollback Procedure

If you need to rollback:

1. Stop current deployment
2. Restore database backup
3. Deploy previous version
4. Run migrations if needed

## Related Documentation

- [Operations Deployment](../operations/deployment.md) - Detailed deployment guide
- [Monitoring Guide](../operations/monitoring.md) - Monitoring setup
- [Troubleshooting](../operations/troubleshooting.md) - Production issues

