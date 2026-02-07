# Deployment Guide

This guide covers deploying Resume Agent to production.

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured
- SSL certificate (for HTTPS)
- Database backup strategy

## Production Checklist

- [ ] Strong, random secrets for JWT tokens
- [ ] HTTPS enabled with valid SSL certificate
- [ ] `DEBUG=false` in production
- [ ] Secure database passwords
- [ ] Firewall rules configured
- [ ] Database backups scheduled
- [ ] Monitoring set up
- [ ] Logging configured
- [ ] Environment variables secured

## Environment Configuration

### Production Environment Variables

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

**Important:** Generate strong, random secrets. Never use default values.

## Docker Deployment

### 1. Create Production Docker Compose

Create `docker-compose.yml`:

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
      - JWT_SECRET=${JWT_SECRET}
      - SECURE_COOKIES=true
      - DEBUG=false
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "8000:8000"
    restart: unless-stopped
    command: uvicorn src.main:app --host 0.0.0.0 --port 8000

volumes:
  postgres_data:
```

### 2. Build and Deploy

```bash
docker compose up -d --build
```

### 3. Run Migrations

```bash
docker compose exec backend alembic upgrade head
```

## Reverse Proxy (Nginx)

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;
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

## SSL Certificate

### Using Let's Encrypt

```bash
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

Certbot automatically sets up auto-renewal.

## Database Backups

### Automated Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/resume_agent_$DATE.sql"

docker compose exec -T postgres pg_dump -U postgres resume_agent > $BACKUP_FILE

# Keep only last 7 days
find $BACKUP_DIR -name "resume_agent_*.sql" -mtime +7 -delete
```

### Schedule with Cron

```bash
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

### Resource Monitoring

Monitor CPU, memory, and disk usage:

```bash
docker stats
```

## Scaling

### Horizontal Scaling

Scale backend services:

```yaml
services:
  backend:
    deploy:
      replicas: 3
```

Use a load balancer to distribute traffic.

## Security

### Firewall

Configure firewall rules:

```bash
# Allow SSH
ufw allow 22/tcp

# Allow HTTP/HTTPS
ufw allow 80/tcp
ufw allow 443/tcp

# Enable firewall
ufw enable
```

### Updates

Keep system and Docker images updated:

```bash
sudo apt-get update && sudo apt-get upgrade
docker compose pull
docker compose up -d --build
```

## Rollback

If you need to rollback:

1. Stop current deployment
2. Restore database backup
3. Deploy previous version
4. Run migrations if needed

## Related Documentation

- [Monitoring Guide](monitoring.md) - Monitoring setup
- [Troubleshooting](troubleshooting.md) - Production issues
- [Deployment Guide](../guides/deployment.md) - Quick deployment

