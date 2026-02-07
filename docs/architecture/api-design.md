# API Design

This document describes the API design principles and patterns used in Resume Agent.

## API Principles

### RESTful Design

- Use HTTP methods correctly (GET, POST, PUT, DELETE)
- Resource-based URLs
- Stateless requests
- Standard HTTP status codes

### Versioning

- API versioned at `/v1/`
- Future versions at `/v2/`, `/v3/`, etc.
- Backward compatibility maintained

### Response Format

Standard response format:

```json
{
  "data": {...},
  "message": "Success"
}
```

Error response format:

```json
{
  "detail": "Error message"
}
```

## Endpoint Structure

### Authentication Endpoints

All under `/v1/auth/`:

- `POST /v1/auth/register` - Register new user
- `POST /v1/auth/login` - Login user
- `POST /v1/auth/refresh` - Refresh access token
- `GET /v1/auth/me` - Get current user

### Resource Endpoints

Follow RESTful patterns:

- `GET /v1/resource` - List resources
- `GET /v1/resource/{id}` - Get resource
- `POST /v1/resource` - Create resource
- `PUT /v1/resource/{id}` - Update resource
- `DELETE /v1/resource/{id}` - Delete resource

## HTTP Status Codes

### Success Codes

- `200 OK`: Successful GET, PUT, DELETE
- `201 Created`: Successful POST (resource created)
- `204 No Content`: Successful DELETE (no content to return)

### Client Error Codes

- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

### Server Error Codes

- `500 Internal Server Error`: Server error

## Authentication

### Bearer Token Authentication

All protected endpoints require Bearer token:

```http
Authorization: Bearer <access_token>
```

### Token in Response

Authentication endpoints return tokens:

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

## Request/Response Examples

### Register User

**Request:**

```http
POST /v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "firstname": "John",
  "lastname": "Doe"
}
```

**Response (201 Created):**

```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Get Current User

**Request:**

```http
GET /v1/auth/me
Authorization: Bearer <access_token>
```

**Response (200 OK):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "firstname": "John",
  "lastname": "Doe",
  "is_active": true
}
```

## Error Handling

### Validation Errors

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Authentication Errors

```json
{
  "detail": "Invalid email or password"
}
```

### Authorization Errors

```json
{
  "detail": "User does not have required permission: user:delete"
}
```

## Pagination

For list endpoints, use pagination:

```http
GET /v1/resource?page=1&page_size=20
```

**Response:**

```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "pages": 5
}
```

## Filtering and Sorting

Use query parameters:

```http
GET /v1/resource?status=active&sort=created_at&order=desc
```

## API Documentation

### Interactive Documentation

- Scalar documentation at `/docs`
- Interactive API explorer
- Request/response examples

### OpenAPI Schema

- Auto-generated from FastAPI
- Available at `/openapi.json`
- Used by Scalar for documentation

## Best Practices

### Naming Conventions

- Use lowercase with hyphens for URLs: `/v1/user-profiles`
- Use plural nouns for resources: `/v1/users`
- Use verbs for actions: `/v1/auth/login`

### Request Validation

- Validate all input data
- Use Pydantic models for validation
- Return clear error messages

### Response Consistency

- Consistent response format
- Include relevant metadata
- Use appropriate status codes

### Security

- Always validate authentication
- Check permissions for protected resources
- Sanitize input data
- Use HTTPS in production

## Related Documentation

- [API Reference](../api/reference.md) - Complete API reference
- [API Examples](../api/examples.md) - Usage examples
- [Authentication API](../api/authentication.md) - Auth endpoints

