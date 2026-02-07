# Development Setup

This guide covers setting up your development environment for Resume Agent.

## Prerequisites

- **Docker** (version 20.10 or higher) and **Docker Compose** (version 2.0 or higher)
- **Git**
- **Python 3.11+** (for manual setup)
- **Node.js 18+** (for frontend development)
- **PostgreSQL 16+** (for manual setup)

## Quick Start with Docker

### 1. Clone Repository

```bash
git clone <repository-url>
cd resume-agent
```

### 2. Set Up Environment Variables

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your configuration (see [Environment Variables](#environment-variables)).

### 3. Start Development Services

```bash
docker compose -f docker-compose.dev.yml up --build
```

This starts:
- PostgreSQL database
- FastAPI backend with hot-reload

### 4. Run Migrations

```bash
docker compose -f docker-compose.dev.yml exec backend-dev alembic upgrade head
```

### 5. Access Services

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Manual Setup (Without Docker)

### Backend Setup

#### 1. Install Python Dependencies

```bash
cd backend
pipenv install --dev
pipenv shell
```

#### 2. Set Up Database

Create PostgreSQL database:

```sql
CREATE DATABASE resume_agent;
```

#### 3. Configure Environment

Copy and edit environment file:

```bash
cp .env.example .env
```

#### 4. Run Migrations

```bash
alembic upgrade head
```

#### 5. Start Backend

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

See [Frontend README](../../frontend/README.md) for frontend setup instructions.

## Environment Variables

### Backend Environment Variables

Create `backend/.env` with the following variables:

```env
# Application
APP_VERSION=1.0.0
DEBUG=true

# Database
POSTGRES_DB=resume_agent
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost  # Use 'postgres' in Docker
POSTGRES_PORT=5432
# Or use DATABASE_URL directly
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/resume_agent

# JWT Authentication
JWT_ALG=HS256
JWT_SECRET=your_jwt_secret_key
JWT_EXP=00:15:00.000000  # minutes
JWT_REFRESH_TOKEN_EXP=30d,00:00:00.000000  # days

SECURE_COOKIES=false  # Set to true in production
```

### Required Variables

- `JWT_SECRET`: Secret key for access tokens
- `POSTGRES_PASSWORD`: Database password (or use `DATABASE_URL`)

### Optional Variables

- `DEBUG`: Enable debug mode (default: false)
- `JWT_EXP`: Access token expiration in minutes (default: 15)
- `JWT_REFRESH_TOKEN_EXP`: Refresh token expiration in days (default: 30)

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write code following [Coding Standards](coding-standards.md)
- Write tests for new features
- Update documentation as needed

### 3. Run Tests

```bash
# In backend directory
pytest

# With coverage
pytest --cov=src
```

### 4. Run Linting

```bash
# Automatic linting and formatting
pre-commit run --all-files

# Or manually
ruff check src/
ruff format src/
```

### 5. Commit Changes

Follow [Conventional Commits](../../CONTRIBUTING.md):

```bash
git add .
git commit -m "feat(auth): add new feature"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

## Hot Reload

### Backend Hot Reload

When running with Docker or `uvicorn --reload`, code changes automatically reload the server.

### Frontend Hot Reload

Frontend development server supports hot module replacement (HMR).

## Database Migrations

### Create Migration

```bash
alembic revision --autogenerate -m "description"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

See [Database Documentation](../../backend/docs/database.md) for details.

## Testing

### Run Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_auth.py

# With verbose output
pytest -v

# Stop on first failure
pytest -x
```

### Test Coverage

```bash
pytest --cov=src --cov-report=html
```

See [Testing Guide](testing.md) for details.

## Debugging

### Backend Debugging

1. Set breakpoints in your code
2. Use Python debugger (pdb) or IDE debugger
3. Check logs: `docker compose logs -f backend`

### Database Debugging

1. Connect to database:
   ```bash
   docker compose exec postgres psql -U postgres -d resume_agent
   ```
2. Check tables: `\dt`
3. Query data: `SELECT * FROM user;`

## Common Issues

### Port Already in Use

If port 8000 is in use:

1. Change port in `docker-compose.dev.yml`
2. Or stop the service using the port

### Database Connection Errors

1. Verify database is running
2. Check credentials in `.env`
3. Verify network connectivity

### Migration Errors

1. Check database connection
2. Ensure migrations are in order
3. See [Troubleshooting](troubleshooting.md)

## IDE Setup

### VS Code

Recommended extensions:
- Python
- Pylance
- Ruff
- Docker

### PyCharm

Configure:
- Python interpreter (Pipenv)
- Docker integration
- Database tools

## Related Documentation

- [Coding Standards](coding-standards.md) - Code style guidelines
- [Testing Guide](testing.md) - Testing approach
- [Troubleshooting](troubleshooting.md) - Common issues
- [Getting Started Guide](../guides/getting-started.md) - Quick start

