# API Reference

Complete reference for all Resume Agent API endpoints.

## Base URL

```
http://localhost:8000  # Development
https://your-domain.com  # Production
```

## Authentication

Most endpoints require authentication using Bearer tokens:

```http
Authorization: Bearer <access_token>
```

See [Authentication API](authentication.md) for authentication endpoints.

## Interactive Documentation

For interactive API documentation, visit:
- **Development**: http://localhost:8000/docs
- **Production**: https://your-domain.com/docs

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

### Authentication Endpoints

See [Authentication API](authentication.md) for detailed documentation.

- `POST /v1/auth/register` - Register new user
- `POST /v1/auth/login` - Login user
- `POST /v1/auth/refresh` - Refresh access token
- `GET /v1/auth/me` - Get current user

### Resumes (all require auth)

- `POST /v1/resumes/upload` - Upload a resume (PDF or Word); returns created resume id, title, source_file_name, source_file_type, created_at.
- `GET /v1/resumes` - List current user's resumes (id, title, source_file_name, source_file_type, has_latex, created_at).
- `GET /v1/resumes/{resume_id}` - Get one resume including extracted_text and latex_content.
- `PATCH /v1/resumes/{resume_id}` - Update title and/or latex_content.
- `POST /v1/resumes/{resume_id}/generate-latex` - Generate LaTeX from extracted text. Body: `{ "provider": "openai" | "deepseek" }`. Returns `{ "latex_content": "..." }`. Uses user's stored API key for the provider.
- `POST /v1/resumes/preview-pdf` - Compile LaTeX to PDF. Body: `{ "latex_content": "..." }`. Returns binary PDF. Requires pdflatex on the server.

### LLM config (user API keys, require auth)

- `GET /v1/users/me/llm-config` - List which providers are configured (no keys returned). Response: `{ "configs": [ { "provider": "openai"|"deepseek", "is_configured": true|false } ] }`.
- `PUT /v1/users/me/llm-config` - Set API key for a provider. Body: `{ "provider": "openai"|"deepseek", "api_key": "..." }`. Keys are stored encrypted.

### Health Endpoints

#### GET /v1/health/detailed

Get detailed health check information.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

## Error Responses

### 400 Bad Request

Invalid request data.

```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized

Authentication required or invalid token.

```json
{
  "detail": "Invalid authentication credentials"
}
```

### 403 Forbidden

Insufficient permissions.

```json
{
  "detail": "User does not have required permission: user:delete"
}
```

### 404 Not Found

Resource not found.

```json
{
  "detail": "Resource not found"
}
```

### 422 Unprocessable Entity

Validation error.

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

### 500 Internal Server Error

Server error.

```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

Rate limiting may be applied to prevent abuse. Check response headers for rate limit information.

## Pagination

List endpoints support pagination:

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

## Filtering

Use query parameters for filtering:

```http
GET /v1/resource?status=active&created_after=2024-01-01
```

## Sorting

Use query parameters for sorting:

```http
GET /v1/resource?sort=created_at&order=desc
```

## Related Documentation

- [Authentication API](authentication.md) - Auth endpoints
- [API Examples](examples.md) - Usage examples
- [API Design](../architecture/api-design.md) - Design principles

