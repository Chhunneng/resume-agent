# Backend Documentation

This directory contains the backend implementation of Resume Agent, built with FastAPI, PostgreSQL, and Python.

## Overview

The backend provides a RESTful API for resume upload (PDF/Word), text extraction, LaTeX generation (OpenAI/DeepSeek), LaTeX→PDF compilation for preview, and user LLM config (encrypted API keys). Auth is JWT-based with refresh tokens and RBAC.

## Quick Start

### Using Docker (Recommended)

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Start services**:
   ```bash
   docker compose -f ../docker-compose.dev.yml up --build
   ```

3. **Run migrations**:
   ```bash
   docker compose -f ../docker-compose.dev.yml exec backend-dev alembic upgrade head
   ```

4. **Access API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

5. **LaTeX PDF preview**: The backend image includes texlive so the resume editor can compile LaTeX to PDF. If you see "pdflatex is not installed", rebuild the backend image:
   ```bash
   docker compose -f ../docker-compose.dev.yml build backend-dev --no-cache
   docker compose -f ../docker-compose.dev.yml up -d backend-dev
   ```

### Manual Setup

1. **Install dependencies**:
   ```bash
   pipenv install --dev
   pipenv shell
   ```

2. **Optional – LaTeX PDF preview**: For the resume editor’s PDF preview, install a LaTeX engine (e.g. **macOS**: `brew install --cask basictex`; **Ubuntu/Debian**: `sudo apt-get install texlive-latex-base texlive-latex-extra`).

3. **Set up database**:
   - Create PostgreSQL database
   - Configure `.env` file

4. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start server**:
   ```bash
   uvicorn src.main:app --reload
   ```

## Features

### Authentication & Authorization

- **JWT-based authentication** with access and refresh tokens
- **Role-Based Access Control (RBAC)** with roles and permissions
- **In-memory RBAC cache** for fast permission checks
- **Automatic cache invalidation** on role/permission changes

See [Auth System Documentation](docs/auth-system.md) for details.

### API Endpoints

- **Health**: `GET /health`, `GET /v1/health/detailed`
- **Authentication**: `POST /v1/auth/register`, `POST /v1/auth/login`, `POST /v1/auth/refresh`, `GET /v1/auth/me`
- **Resumes**: `POST /v1/resumes/upload`, `GET /v1/resumes`, `GET /v1/resumes/{id}`, `PATCH /v1/resumes/{id}`, `POST /v1/resumes/{id}/generate-latex`, `POST /v1/resumes/preview-pdf`
- **LLM config**: `GET /v1/users/me/llm-config`, `PUT /v1/users/me/llm-config`

See [API Documentation](../../docs/api/reference.md) for complete API reference.

### Database

- **PostgreSQL 16+** with async SQLAlchemy
- **Alembic migrations** for schema management
- **SQLModel** for type-safe models

See [Database Documentation](docs/database.md) for details.

## Project Structure

```
backend/
├── src/
│   ├── auth/              # Authentication & RBAC (User, Role, Permission, JWT, cache)
│   ├── database/          # PostgreSQL connection, base models
│   ├── documents/         # PDF/Word parsing (text extraction)
│   ├── health/            # Health check endpoints
│   ├── llm/               # LaTeX generation, encrypted user API keys, LLM config API
│   ├── resumes/           # Resume CRUD, upload, generate-latex, preview-pdf (pdflatex)
│   ├── routes/v1/         # API route aggregation (auth, health, resumes, users/me)
│   └── main.py            # FastAPI application
├── alembic/               # Database migrations
├── tests/
├── docs/                  # Backend-specific documentation
└── .env.example           # Environment variable template
```

## Environment Variables

See `.env.example` for the full list. Key variables:

**Required**

- `JWT_ACCESS_TOKEN_SECRET`: Secret for access tokens (e.g. `openssl rand -hex 32`)
- `JWT_REFRESH_TOKEN_SECRET`: Secret for refresh tokens (e.g. `openssl rand -hex 32`)
- Database: set `POSTGRES_*` or `DATABASE_URL`. For Docker, `POSTGRES_PASSWORD` and `POSTGRES_HOST` are typically set.

**Optional (with defaults)**

- `LLM_CONFIG_ENCRYPTION_KEY`: Encrypts user API keys. Use a 64-char hex string or a Fernet key (see `.env.example`). Required for LaTeX generation and profile API key storage; if unset, those features will fail.
- `DEBUG`: Enable debug mode (default: `false`)
- `UPLOADS_DIR`: Directory for uploaded resume files (default: `uploads`)
- `JWT_ALG`: JWT algorithm (default: `HS256`)
- `JWT_ACCESS_TOKEN_EXP`: Access token expiry (default: 15 minutes)
- `JWT_REFRESH_TOKEN_EXP`: Refresh token expiry (default: 30 days)
- `SECURE_COOKIES`: Set to `false` for development over HTTP (default: `true`)

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

See [Database Documentation](docs/database.md) for detailed migration guide.

## Testing

### Run Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=html
```

See [Testing Documentation](docs/testing.md) for testing guidelines.

## API Documentation

### Interactive Documentation

- **Scalar**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Manual Documentation

- [API Reference](../../docs/api/reference.md)
- [Authentication API](../../docs/api/authentication.md)
- [API Examples](../../docs/api/examples.md)

## Documentation

### Backend-Specific

- [Auth System](docs/auth-system.md) - Complete authentication documentation
- [Database](docs/database.md) - Database setup and migrations
- [Testing](docs/testing.md) - Testing guide

### General Documentation

- [Getting Started](../../docs/guides/getting-started.md)
- [Development Setup](../../docs/development/setup.md)
- [Architecture Overview](../../docs/architecture/overview.md)
- [Full Documentation Index](../../docs/README.md)

## Development

### Pre-commit Hooks

This project uses pre-commit hooks to automatically run Ruff linting and formatting before each commit. This ensures code quality and consistency.

#### Installation

1. **Install dependencies** (if not already done):
   ```bash
   pipenv install --dev
   ```

2. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

   This will set up the git hooks in your `.git/hooks/` directory.

#### Usage

Once installed, pre-commit hooks will automatically run when you make a commit. The hooks will:

- Run `ruff check --fix` on staged Python files in `backend/src/` to catch and auto-fix linting issues
- Run `ruff format` on staged Python files in `backend/src/` to ensure consistent formatting

If the hooks find issues that can't be auto-fixed, the commit will be blocked. Fix the issues and try committing again.

#### Manual Execution

You can manually run the pre-commit hooks on all files (not just staged ones):

```bash
pre-commit run --all-files
```

#### Updating Hooks

To update the pre-commit hooks to their latest versions:

```bash
pre-commit autoupdate
```

#### Skipping Hooks (Not Recommended)

If you need to skip the hooks for a specific commit (not recommended), you can use:

```bash
git commit --no-verify
```

However, this should only be used in exceptional circumstances, as it bypasses the code quality checks.
