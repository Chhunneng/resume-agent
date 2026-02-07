# System Architecture Overview

This document provides a high-level overview of the Resume Agent system architecture.

## System Components

### Backend

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT with RBAC
- **API Documentation**: Scalar

### Frontend

- **Framework**: React
- **Language**: TypeScript
- **UI Library**: Tailwind CSS, Shadcn UI
- **Build Tool**: Vite

### Infrastructure

- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Development**: Hot-reload enabled

## Architecture Diagram

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       │ HTTP/HTTPS
       │
┌──────▼──────────────────┐
│   Frontend (React)      │
│   - Vite                │
│   - Tailwind CSS        │
│   - Shadcn UI           │
└──────┬──────────────────┘
       │
       │ REST API
       │
┌──────▼──────────────────┐
│   Backend (FastAPI)     │
│   - JWT Auth            │
│   - RBAC                │
│   - Business Logic      │
└──────┬──────────────────┘
       │
       │ SQL
       │
┌──────▼──────────────────┐
│   PostgreSQL Database   │
│   - User Data           │
│   - Roles/Permissions   │
│   - Application Data    │
└─────────────────────────┘
```

## Request Flow

### 1. Client Request

```
Client → Frontend → Backend API → Database
```

### 2. Authentication Flow

```
1. User logs in → Backend validates credentials
2. Backend issues JWT tokens (access + refresh)
3. Client stores tokens
4. Client includes access token in subsequent requests
5. Backend validates token and checks permissions
```

### 3. Authorization Flow

```
1. Request arrives with JWT token
2. Backend validates token
3. Backend loads user roles from database
4. Backend checks permissions using RBAC cache
5. Request proceeds if authorized
```

## Data Flow

### User Registration

```
1. Client sends registration data
2. Backend validates data
3. Backend hashes password
4. Backend creates user with default roles
5. Backend returns JWT tokens
```

### Permission Check

```
1. User makes request
2. Backend extracts user from JWT
3. Backend gets user roles from database
4. Backend checks permissions in cache (O(1))
5. Request allowed/denied based on permissions
```

## Key Design Patterns

### Dependency Injection

FastAPI's dependency injection system is used for:
- Database sessions
- Authentication
- Authorization
- Configuration

### Repository Pattern

Database access is abstracted through:
- SQLAlchemy models
- Session management
- Query builders

### Caching Strategy

- In-memory cache for RBAC permissions
- O(1) permission lookups
- Automatic cache invalidation

## Security Architecture

### Authentication

- JWT-based stateless authentication
- Access tokens (short-lived)
- Refresh tokens (long-lived)
- Password hashing with secure algorithms

### Authorization

- Role-Based Access Control (RBAC)
- Permission-based checks
- Fast cache-based lookups

### Data Protection

- HTTPS in production
- Secure password storage
- SQL injection prevention (ORM)
- XSS protection

## Scalability Considerations

### Horizontal Scaling

- Stateless backend (JWT)
- Database connection pooling
- Load balancer ready

### Performance Optimization

- RBAC cache for fast permission checks
- Database indexes
- Efficient queries
- Connection pooling

## Technology Stack

### Backend Stack

- **Python 3.11**: Programming language
- **FastAPI**: Web framework
- **PostgreSQL**: Database
- **SQLAlchemy 2.0**: ORM
- **Alembic**: Migrations
- **JWT**: Authentication
- **Pydantic**: Data validation

### Frontend Stack

- **TypeScript**: Programming language
- **React**: UI framework
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Shadcn UI**: Component library

### DevOps Stack

- **Docker**: Containerization
- **Docker Compose**: Orchestration
- **Git**: Version control

## Related Documentation

- [Authentication Architecture](authentication.md) - Auth system details
- [Database Schema](database-schema.md) - Database design
- [Caching Strategy](caching.md) - Cache implementation
- [API Design](api-design.md) - API structure

