# Getting Started

Welcome to Resume Agent! This guide will help you set up the project for the first time.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git**

For manual setup (without Docker):

- **Python** 3.11 or higher
- **Node.js** 18 or higher
- **PostgreSQL** 16 or higher
- **Pipenv** (for Python package management)
- **npm** or **yarn** (for frontend dependencies)

## Quick Start with Docker (Recommended)

The easiest way to get started is using Docker Compose.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd resume-agent
```

### 2. Set Up Environment Variables

Copy the example environment file:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your configuration. See [Environment Configuration](../development/setup.md#environment-variables) for details.

### 3. Start the Services

Start the backend and database services:

```bash
docker compose -f docker-compose.dev.yml up --build
```

This will:
- Build the Docker images
- Start PostgreSQL database
- Start the FastAPI backend and the React frontend (Vite)
- Enable hot-reload for both

### 4. Run Database Migrations

In a new terminal, run migrations:

```bash
docker compose -f docker-compose.dev.yml exec backend-dev alembic upgrade head
```

### 5. Access the Application

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Scalar)
- **Health Check**: http://localhost:8000/health
- **Frontend**: http://localhost:5173 (Vite dev server)

## Manual Setup

If you prefer to run the application without Docker, see the detailed setup guides:

- [Backend Setup](../../backend/README.md#development-setup)
- [Frontend Setup](../../frontend/README.md)

## Verify Installation

### Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### Check API Documentation

Open http://localhost:8000/docs in your browser. You should see the interactive API documentation.

## Next Steps

1. **Set Up Authentication**: See [Authentication Guide](authentication.md)
2. **Configure RBAC**: See [RBAC Setup Guide](rbac-setup.md)
3. **Explore the API**: Use the interactive docs at `/docs`
4. **Read Architecture Docs**: See [Architecture Overview](../architecture/overview.md)

## Common Issues

### Port Already in Use

If port 8000 is already in use:

1. Stop the service using the port
2. Or change the port in `docker-compose.dev.yml`

### Database Connection Errors

1. Ensure PostgreSQL is running
2. Check database credentials in `.env`
3. Verify database exists

### Migration Errors

If migrations fail:

1. Check database connection
2. Ensure database is empty or migrations are in order
3. See [Troubleshooting](../development/troubleshooting.md)

## Development Workflow

Once set up, follow this workflow:

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following [Coding Standards](../development/coding-standards.md)

3. **Run tests**:
   ```bash
   # In backend container
   pytest
   ```

4. **Commit your changes** following [Conventional Commits](../../CONTRIBUTING.md)

5. **Create a pull request**

## Getting Help

- Check [Troubleshooting Guide](../development/troubleshooting.md)
- Review [API Examples](../api/examples.md)
- See [Architecture Documentation](../architecture/overview.md)
- Open an issue on the repository

## Additional Resources

- [Project README](../../README.md)
- [Contributing Guidelines](../../CONTRIBUTING.md)
- [Backend Documentation](../../backend/README.md)
- [Frontend Documentation](../../frontend/README.md)

