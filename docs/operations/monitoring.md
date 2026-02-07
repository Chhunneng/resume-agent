# Monitoring Guide

This guide covers monitoring and logging for Resume Agent in production.

## Health Checks

### Application Health

Monitor the health endpoint:

```bash
curl https://your-domain.com/health
```

**Expected Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### Detailed Health Check

```bash
curl https://your-domain.com/v1/health/detailed
```

**Expected Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

## Logging

### Application Logs

View application logs:

```bash
# Docker
docker compose logs -f backend

# Specific service
docker compose logs -f backend | grep ERROR
```

### Log Levels

- **DEBUG**: Detailed information for debugging
- **INFO**: General information
- **WARNING**: Warning messages
- **ERROR**: Error messages
- **CRITICAL**: Critical errors

### Log Configuration

Configure logging in application:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Resource Monitoring

### Docker Stats

Monitor container resources:

```bash
docker stats
```

### System Resources

Monitor system resources:

```bash
# CPU and memory
top

# Disk usage
df -h

# Network
netstat -tuln
```

## Database Monitoring

### Connection Status

Check database connections:

```bash
docker compose exec postgres psql -U postgres -c "SELECT count(*) FROM pg_stat_activity;"
```

### Database Size

```bash
docker compose exec postgres psql -U postgres -c "SELECT pg_size_pretty(pg_database_size('resume_agent'));"
```

### Query Performance

Enable slow query logging in PostgreSQL configuration.

## Error Monitoring

### Common Errors to Monitor

- **401 Unauthorized**: Authentication failures
- **403 Forbidden**: Permission denials
- **500 Internal Server Error**: Application errors
- **Database connection errors**: Database issues

### Error Alerts

Set up alerts for:
- High error rates
- Database connection failures
- Application crashes
- Resource exhaustion

## Performance Monitoring

### Response Times

Monitor API response times:

```bash
curl -w "@curl-format.txt" -o /dev/null -s https://your-domain.com/health
```

### Throughput

Monitor requests per second:

```bash
# Use monitoring tools like Prometheus, Grafana, or APM tools
```

## Backup Monitoring

### Verify Backups

Regularly verify backups are working:

```bash
# Check backup files exist
ls -lh /backups/

# Test restore (on test server)
pg_restore -d test_db backup_file.sql
```

## Alerting

### Set Up Alerts

Configure alerts for:
- Health check failures
- High error rates
- Database connection issues
- Disk space low
- Memory usage high

### Notification Channels

- Email
- Slack
- PagerDuty
- SMS

## Monitoring Tools

### Recommended Tools

- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking
- **Datadog**: APM and monitoring
- **New Relic**: Application monitoring

## Best Practices

1. **Monitor Key Metrics**: Response time, error rate, throughput
2. **Set Up Alerts**: Get notified of issues early
3. **Review Logs Regularly**: Identify patterns and issues
4. **Track Trends**: Monitor metrics over time
5. **Document Incidents**: Learn from issues

## Related Documentation

- [Deployment Guide](deployment.md) - Production deployment
- [Troubleshooting](troubleshooting.md) - Common issues

