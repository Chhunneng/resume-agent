# Production Troubleshooting

Common production issues and solutions for Resume Agent.

## Application Issues

### Application Won't Start

**Symptoms:** Container fails to start or crashes

**Solutions:**
1. Check logs:
   ```bash
   docker compose logs backend
   ```

2. Verify environment variables:
   ```bash
   docker compose config
   ```

3. Check database connection:
   ```bash
   docker compose exec backend python -c "from src.database import init_db; import asyncio; asyncio.run(init_db())"
   ```

4. Verify migrations:
   ```bash
   docker compose exec backend alembic current
   ```

### High Error Rate

**Symptoms:** Many 500 errors or application errors

**Solutions:**
1. Check application logs for errors
2. Verify database connectivity
3. Check resource usage (CPU, memory)
4. Review recent deployments
5. Check external service dependencies

### Slow Response Times

**Symptoms:** API responses are slow

**Solutions:**
1. Check database query performance
2. Monitor resource usage
3. Review database indexes
4. Check for N+1 query problems
5. Consider caching strategies

## Database Issues

### Connection Pool Exhausted

**Symptoms:** "Too many connections" errors

**Solutions:**
1. Increase connection pool size:
   ```python
   engine = create_async_engine(..., pool_size=20)
   ```

2. Check for connection leaks
3. Restart application to clear connections

### Database Performance

**Symptoms:** Slow queries, high CPU usage

**Solutions:**
1. Check database indexes:
   ```sql
   \d+ table_name
   ```

2. Analyze slow queries:
   ```sql
   SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
   ```

3. Vacuum database:
   ```sql
   VACUUM ANALYZE;
   ```

### Database Corruption

**Symptoms:** Data inconsistencies, errors

**Solutions:**
1. Restore from backup
2. Run database integrity checks
3. Contact database administrator

## Authentication Issues

### Token Validation Failures

**Symptoms:** Many 401 errors

**Solutions:**
1. Verify JWT secrets haven't changed
2. Check token expiration settings
3. Verify clock synchronization
4. Check token format in requests

### Permission Denials

**Symptoms:** Many 403 errors

**Solutions:**
1. Verify RBAC cache is loaded
2. Check role/permission assignments
3. Refresh RBAC cache if needed
4. Review permission checks in code

## Network Issues

### Connection Timeouts

**Symptoms:** Requests timeout

**Solutions:**
1. Check network connectivity
2. Verify firewall rules
3. Check load balancer configuration
4. Review reverse proxy settings

### SSL Certificate Issues

**Symptoms:** SSL errors, certificate warnings

**Solutions:**
1. Verify certificate is valid:
   ```bash
   openssl x509 -in certificate.crt -text -noout
   ```

2. Check certificate expiration
3. Renew certificate if expired
4. Verify certificate chain

## Resource Issues

### High Memory Usage

**Symptoms:** Out of memory errors, slow performance

**Solutions:**
1. Monitor memory usage:
   ```bash
   docker stats
   ```

2. Check for memory leaks
3. Increase container memory limits
4. Optimize application code

### High CPU Usage

**Symptoms:** Slow performance, high load

**Solutions:**
1. Identify CPU-intensive operations
2. Optimize database queries
3. Add caching where appropriate
4. Scale horizontally if needed

### Disk Space

**Symptoms:** Disk full errors

**Solutions:**
1. Check disk usage:
   ```bash
   df -h
   ```

2. Clean up old logs
3. Remove old Docker images:
   ```bash
   docker system prune -a
   ```

4. Archive old backups

## Deployment Issues

### Failed Deployments

**Symptoms:** Deployment fails or rolls back

**Solutions:**
1. Check deployment logs
2. Verify environment variables
3. Test migrations before deployment
4. Use blue-green deployment strategy

### Migration Failures

**Symptoms:** Migrations fail during deployment

**Solutions:**
1. Test migrations on staging first
2. Backup database before migration
3. Check migration dependencies
4. Have rollback plan ready

## Monitoring Issues

### Monitoring Not Working

**Symptoms:** No metrics or alerts

**Solutions:**
1. Verify monitoring service is running
2. Check monitoring configuration
3. Verify network connectivity to monitoring service
4. Review monitoring service logs

## Emergency Procedures

### Application Down

1. Check health endpoint
2. Review application logs
3. Check database connectivity
4. Restart services if needed
5. Rollback to previous version if necessary

### Data Loss

1. Stop application immediately
2. Assess data loss extent
3. Restore from latest backup
4. Investigate root cause
5. Implement prevention measures

### Security Incident

1. Isolate affected systems
2. Preserve logs and evidence
3. Assess impact
4. Notify stakeholders
5. Remediate vulnerabilities
6. Review and update security measures

## Getting Help

If you can't resolve an issue:

1. Collect relevant logs
2. Document error messages
3. Note recent changes
4. Check monitoring dashboards
5. Contact support team

## Related Documentation

- [Deployment Guide](deployment.md) - Production deployment
- [Monitoring Guide](monitoring.md) - Monitoring setup
- [Development Troubleshooting](../development/troubleshooting.md) - Development issues

