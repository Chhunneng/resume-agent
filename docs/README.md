# Resume Agent Documentation

Welcome to the Resume Agent documentation! This is your central hub for all project documentation.

## Table of Contents

### Quick Start
- [Getting Started Guide](guides/getting-started.md) - Set up the project for the first time
- [Main README](../README.md) - Project overview and quick reference

### User Guides
- [Authentication Guide](guides/authentication.md) - How to use authentication features
- [RBAC Setup Guide](guides/rbac-setup.md) - Setting up roles and permissions
- [Deployment Guide](guides/deployment.md) - Production deployment instructions

### Architecture
- [System Overview](architecture/overview.md) - High-level system architecture
- [Authentication Architecture](architecture/authentication.md) - Auth flow and JWT structure
- [Database Schema](architecture/database-schema.md) - Database design and relationships
- [Caching Strategy](architecture/caching.md) - RBAC cache implementation
- [API Design](architecture/api-design.md) - API design principles and patterns

### API Documentation
- [API Reference](api/reference.md) - Complete API endpoint reference
- [Authentication API](api/authentication.md) - Auth endpoints with examples
- [API Examples](api/examples.md) - Usage examples and common patterns
- [Interactive API Docs](../README.md#access-the-application) - Scalar documentation at `/docs`

### Development
- [Development Setup](development/setup.md) - Setting up your development environment
- [Coding Standards](development/coding-standards.md) - Code style and conventions
- [Testing Guide](development/testing.md) - How to write and run tests
- [Troubleshooting](development/troubleshooting.md) - Common development issues

### Operations
- [Deployment](operations/deployment.md) - Production deployment guide
- [Monitoring](operations/monitoring.md) - Monitoring and logging setup
- [Troubleshooting](operations/troubleshooting.md) - Production troubleshooting

### Backend-Specific
- [Backend README](../backend/README.md) - Backend quick start
- [Auth System Deep Dive](../backend/docs/auth-system.md) - Comprehensive auth documentation
- [Database Documentation](../backend/docs/database.md) - Database setup and migrations
- [Backend Testing](../backend/docs/testing.md) - Backend testing guide

### Frontend-Specific
- [Frontend README](../frontend/README.md) - Frontend quick start

## Documentation Principles

### Keep It Close to Code
- Module documentation lives alongside code
- README files in each major directory
- Code examples in docstrings

### Make It Discoverable
- Clear navigation and cross-references
- Search-friendly structure
- Consistent organization

### Keep It Current
- Documentation is updated with code changes
- Outdated content is removed
- Examples are tested and working

### Write for Different Audiences
- **New developers**: Start with getting started guides
- **Experienced developers**: Jump to architecture docs
- **Users**: Focus on API usage examples
- **Operations**: See deployment and monitoring guides

## Contributing to Documentation

When adding new features or making changes:

1. **Update relevant documentation** - If you add a feature, document it
2. **Keep examples working** - Test code examples before committing
3. **Follow the structure** - Use existing docs as templates
4. **Write clearly** - Use simple language, avoid jargon
5. **Include examples** - Show, don't just tell

For detailed contribution guidelines, see [CONTRIBUTING.md](../CONTRIBUTING.md).

## Quick Links

- [Project Repository](../README.md)
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Backend Setup](../backend/README.md)
- [Frontend Setup](../frontend/README.md)
- [API Documentation](http://localhost:8000/docs) (when running locally)

## Need Help?

If you can't find what you're looking for:
1. Check the [Troubleshooting Guides](development/troubleshooting.md)
2. Review the [API Examples](api/examples.md)
3. See the [Architecture Documentation](architecture/overview.md)
4. Open an issue on the repository

