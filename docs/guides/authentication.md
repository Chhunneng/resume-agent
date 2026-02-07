# Authentication Guide

This guide explains how to use the authentication system in Resume Agent.

## Overview

Resume Agent uses JWT (JSON Web Tokens) for authentication. You'll receive two tokens:

- **Access Token**: Short-lived (15 minutes), used for API requests
- **Refresh Token**: Long-lived (30 days), used to get new access tokens

## Registration

### Register a New User

```http
POST /v1/auth/register
Content-Type: application/json

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

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note:** All address fields are optional. Only `email`, `password`, `firstname`, and `lastname` are required.

## Login

### Login with Email and Password

```http
POST /v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## Using Access Tokens

### Making Authenticated Requests

Include the access token in the `Authorization` header:

```http
GET /v1/auth/me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Example with cURL

```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://localhost:8000/v1/auth/me
```

### Example with JavaScript (Fetch)

```javascript
const response = await fetch('http://localhost:8000/v1/auth/me', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const user = await response.json();
```

### Example with Python (Requests)

```python
import requests

headers = {
    'Authorization': f'Bearer {access_token}'
}

response = requests.get('http://localhost:8000/v1/auth/me', headers=headers)
user = response.json()
```

## Refreshing Access Tokens

When your access token expires (after 15 minutes), use the refresh token to get a new one:

```http
POST /v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note:** The refresh token itself doesn't expire for 30 days, but you should refresh your access token regularly.

## Getting Current User Information

### Get Your Profile

```http
GET /v1/auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**

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

## Token Lifecycle

1. **Register or Login**: Receive access and refresh tokens
2. **Use Access Token**: Include in API requests
3. **Token Expires**: Access token expires after 15 minutes
4. **Refresh Token**: Use refresh token to get new access token
5. **Repeat**: Continue using new access tokens

## Error Handling

### Invalid Credentials

```json
{
  "detail": "Invalid email or password"
}
```

### Expired Token

```json
{
  "detail": "Invalid authentication credentials"
}
```

**Solution:** Use the refresh token to get a new access token.

### Inactive Account

```json
{
  "detail": "User account is inactive"
}
```

**Solution:** Contact an administrator to activate your account.

### Missing Token

```json
{
  "detail": "Invalid authentication credentials"
}
```

**Solution:** Include the `Authorization: Bearer <token>` header in your request.

## Best Practices

### Token Storage

- **Web Applications**: Store tokens in HTTP-only cookies or secure storage
- **Mobile Apps**: Use secure storage (Keychain on iOS, Keystore on Android)
- **Never**: Store tokens in localStorage or sessionStorage (XSS risk)

### Token Refresh

- Refresh access tokens before they expire
- Handle token refresh errors gracefully
- Implement automatic token refresh

### Security

- Use HTTPS in production
- Never share your tokens
- Log out when done (invalidate tokens if possible)
- Use strong passwords

## Example: Complete Authentication Flow

### JavaScript Example

```javascript
// Register
const registerResponse = await fetch('http://localhost:8000/v1/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'secure_password',
    firstname: 'John',
    lastname: 'Doe'
  })
});

const { access_token, refresh_token } = await registerResponse.json();

// Store tokens securely
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);

// Make authenticated request
const userResponse = await fetch('http://localhost:8000/v1/auth/me', {
  headers: {
    'Authorization': `Bearer ${access_token}`
  }
});

const user = await userResponse.json();

// Refresh token when access token expires
const refreshResponse = await fetch('http://localhost:8000/v1/auth/refresh', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    refresh_token: refresh_token
  })
});

const { access_token: new_access_token } = await refreshResponse.json();
localStorage.setItem('access_token', new_access_token);
```

### Python Example

```python
import requests

# Register
register_data = {
    'email': 'user@example.com',
    'password': 'secure_password',
    'firstname': 'John',
    'lastname': 'Doe'
}

response = requests.post(
    'http://localhost:8000/v1/auth/register',
    json=register_data
)

tokens = response.json()
access_token = tokens['access_token']
refresh_token = tokens['refresh_token']

# Make authenticated request
headers = {'Authorization': f'Bearer {access_token}'}
user_response = requests.get(
    'http://localhost:8000/v1/auth/me',
    headers=headers
)

user = user_response.json()

# Refresh token
refresh_data = {'refresh_token': refresh_token}
refresh_response = requests.post(
    'http://localhost:8000/v1/auth/refresh',
    json=refresh_data
)

new_tokens = refresh_response.json()
new_access_token = new_tokens['access_token']
```

## Roles and Permissions

After authentication, your user has roles and permissions. See [RBAC Setup Guide](rbac-setup.md) for more information.

## Related Documentation

- [Auth System Deep Dive](../../backend/docs/auth-system.md) - Technical details
- [RBAC Setup Guide](rbac-setup.md) - Setting up roles and permissions
- [API Authentication Documentation](../api/authentication.md) - API endpoint details
- [Authentication Architecture](../architecture/authentication.md) - How it works

