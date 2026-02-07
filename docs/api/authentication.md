# Authentication API

Complete reference for authentication endpoints.

## Base URL

All authentication endpoints are under `/v1/auth/`.

## Endpoints

### Register User

#### POST /v1/auth/register

Register a new user account.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "firstname": "John",
  "lastname": "Doe",
  "phone_number": "+1234567890",
  "street_address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "country": "USA"
}
```

**Required Fields:**
- `email`: User email address (must be unique)
- `password`: User password
- `firstname`: User first name
- `lastname`: User last name

**Optional Fields:**
- `phone_number`: Phone number
- `street_address`: Street address
- `city`: City
- `state`: State/Province
- `zip_code`: ZIP/Postal code
- `country`: Country

**Response (201 Created):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

- `400 Bad Request`: Email already registered
- `422 Unprocessable Entity`: Validation error

### Login

#### POST /v1/auth/login

Authenticate user and receive tokens.

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Required Fields:**
- `email`: User email address
- `password`: User password

**Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

- `401 Unauthorized`: Invalid email or password
- `403 Forbidden`: User account is inactive
- `422 Unprocessable Entity`: Validation error

### Refresh Token

#### POST /v1/auth/refresh

Get a new access token using a refresh token.

**Request Body:**

```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Required Fields:**
- `refresh_token`: Valid refresh token

**Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

- `401 Unauthorized`: Invalid or expired refresh token
- `422 Unprocessable Entity`: Validation error

### Get Current User

#### GET /v1/auth/me

Get the current authenticated user's information.

**Headers:**
- `Authorization: Bearer <access_token>` (required)

**Response (200 OK):**

```json
{
  "id": 1,
  "email": "user@example.com",
  "firstname": "John",
  "lastname": "Doe",
  "phone_number": "+1234567890",
  "registration_date": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-02T00:00:00Z",
  "is_active": true,
  "street_address": "123 Main St",
  "city": "New York",
  "state": "NY",
  "zip_code": "10001",
  "country": "USA"
}
```

**Error Responses:**

- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: User account is inactive

## Token Usage

### Access Token

Include the access token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

Access tokens expire after 15 minutes (configurable).

### Refresh Token

Use the refresh token to get a new access token when it expires. Refresh tokens expire after 30 days (configurable).

## Examples

### cURL Examples

**Register:**

```bash
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password",
    "firstname": "John",
    "lastname": "Doe"
  }'
```

**Login:**

```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password"
  }'
```

**Get Current User:**

```bash
curl -X GET http://localhost:8000/v1/auth/me \
  -H "Authorization: Bearer <access_token>"
```

**Refresh Token:**

```bash
curl -X POST http://localhost:8000/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "<refresh_token>"
  }'
```

### JavaScript Examples

See [API Examples](examples.md) for complete JavaScript examples.

## Related Documentation

- [Authentication Guide](../guides/authentication.md) - User guide
- [API Examples](examples.md) - Usage examples
- [Auth System Deep Dive](../../backend/docs/auth-system.md) - Technical details

