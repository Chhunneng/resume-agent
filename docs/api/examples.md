# API Examples

Practical examples for using the Resume Agent API.

## Authentication Examples

### Register a New User

**JavaScript (Fetch):**

```javascript
const registerUser = async () => {
  const response = await fetch('http://localhost:8000/v1/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: 'user@example.com',
      password: 'secure_password',
      firstname: 'John',
      lastname: 'Doe',
    }),
  });

  if (response.ok) {
    const { access_token, refresh_token } = await response.json();
    // Store tokens securely
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    return { access_token, refresh_token };
  } else {
    const error = await response.json();
    throw new Error(error.detail);
  }
};
```

**Python (Requests):**

```python
import requests

def register_user():
    url = 'http://localhost:8000/v1/auth/register'
    data = {
        'email': 'user@example.com',
        'password': 'secure_password',
        'firstname': 'John',
        'lastname': 'Doe',
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    
    tokens = response.json()
    return tokens['access_token'], tokens['refresh_token']
```

### Login

**JavaScript (Fetch):**

```javascript
const login = async (email, password) => {
  const response = await fetch('http://localhost:8000/v1/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  });

  if (response.ok) {
    const { access_token, refresh_token } = await response.json();
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
    return { access_token, refresh_token };
  } else {
    const error = await response.json();
    throw new Error(error.detail);
  }
};
```

**Python (Requests):**

```python
def login(email, password):
    url = 'http://localhost:8000/v1/auth/login'
    data = {'email': email, 'password': password}
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    
    tokens = response.json()
    return tokens['access_token'], tokens['refresh_token']
```

### Get Current User

**JavaScript (Fetch):**

```javascript
const getCurrentUser = async () => {
  const accessToken = localStorage.getItem('access_token');
  
  const response = await fetch('http://localhost:8000/v1/auth/me', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });

  if (response.ok) {
    return await response.json();
  } else if (response.status === 401) {
    // Token expired, refresh it
    await refreshAccessToken();
    return getCurrentUser();
  } else {
    const error = await response.json();
    throw new Error(error.detail);
  }
};
```

**Python (Requests):**

```python
def get_current_user(access_token):
    url = 'http://localhost:8000/v1/auth/me'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()
```

### Refresh Access Token

**JavaScript (Fetch):**

```javascript
const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refresh_token');
  
  const response = await fetch('http://localhost:8000/v1/auth/refresh', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (response.ok) {
    const { access_token } = await response.json();
    localStorage.setItem('access_token', access_token);
    return access_token;
  } else {
    // Refresh token expired, need to login again
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    throw new Error('Refresh token expired');
  }
};
```

**Python (Requests):**

```python
def refresh_access_token(refresh_token):
    url = 'http://localhost:8000/v1/auth/refresh'
    data = {'refresh_token': refresh_token}
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    
    tokens = response.json()
    return tokens['access_token']
```

## Complete Authentication Flow

**JavaScript:**

```javascript
class AuthService {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async register(userData) {
    const response = await fetch(`${this.baseUrl}/v1/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
    
    const tokens = await response.json();
    this.saveTokens(tokens);
    return tokens;
  }

  async login(email, password) {
    const response = await fetch(`${this.baseUrl}/v1/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }
    
    const tokens = await response.json();
    this.saveTokens(tokens);
    return tokens;
  }

  async getCurrentUser() {
    const token = this.getAccessToken();
    if (!token) {
      throw new Error('Not authenticated');
    }

    const response = await fetch(`${this.baseUrl}/v1/auth/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });

    if (response.status === 401) {
      // Token expired, try to refresh
      await this.refreshToken();
      return this.getCurrentUser();
    }

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail);
    }

    return await response.json();
  }

  async refreshToken() {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token available');
    }

    const response = await fetch(`${this.baseUrl}/v1/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });

    if (!response.ok) {
      this.clearTokens();
      throw new Error('Refresh token expired');
    }

    const { access_token } = await response.json();
    this.saveAccessToken(access_token);
    return access_token;
  }

  saveTokens({ access_token, refresh_token }) {
    localStorage.setItem('access_token', access_token);
    localStorage.setItem('refresh_token', refresh_token);
  }

  saveAccessToken(access_token) {
    localStorage.setItem('access_token', access_token);
  }

  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  getRefreshToken() {
    return localStorage.getItem('refresh_token');
  }

  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
}

// Usage
const auth = new AuthService('http://localhost:8000');

// Register
await auth.register({
  email: 'user@example.com',
  password: 'secure_password',
  firstname: 'John',
  lastname: 'Doe',
});

// Get current user
const user = await auth.getCurrentUser();
console.log(user);
```

**Python:**

```python
import requests
from typing import Optional, Tuple

class AuthService:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

    def register(self, email: str, password: str, firstname: str, lastname: str) -> Tuple[str, str]:
        url = f'{self.base_url}/v1/auth/register'
        data = {
            'email': email,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        tokens = response.json()
        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        return self.access_token, self.refresh_token

    def login(self, email: str, password: str) -> Tuple[str, str]:
        url = f'{self.base_url}/v1/auth/login'
        data = {'email': email, 'password': password}
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        tokens = response.json()
        self.access_token = tokens['access_token']
        self.refresh_token = tokens['refresh_token']
        return self.access_token, self.refresh_token

    def get_current_user(self) -> dict:
        if not self.access_token:
            raise ValueError('Not authenticated')
        
        url = f'{self.base_url}/v1/auth/me'
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 401:
            # Token expired, refresh it
            self.refresh_access_token()
            return self.get_current_user()
        
        response.raise_for_status()
        return response.json()

    def refresh_access_token(self) -> str:
        if not self.refresh_token:
            raise ValueError('No refresh token available')
        
        url = f'{self.base_url}/v1/auth/refresh'
        data = {'refresh_token': self.refresh_token}
        
        response = requests.post(url, json=data)
        
        if not response.ok:
            self.access_token = None
            self.refresh_token = None
            raise ValueError('Refresh token expired')
        
        tokens = response.json()
        self.access_token = tokens['access_token']
        return self.access_token

# Usage
auth = AuthService('http://localhost:8000')

# Register
auth.register('user@example.com', 'secure_password', 'John', 'Doe')

# Get current user
user = auth.get_current_user()
print(user)
```

## Error Handling

**JavaScript:**

```javascript
const handleApiError = async (response) => {
  if (!response.ok) {
    const error = await response.json();
    
    switch (response.status) {
      case 401:
        // Try to refresh token
        await refreshAccessToken();
        break;
      case 403:
        console.error('Insufficient permissions');
        break;
      case 404:
        console.error('Resource not found');
        break;
      default:
        console.error('API error:', error.detail);
    }
    
    throw new Error(error.detail);
  }
};
```

**Python:**

```python
def handle_api_error(response):
    if not response.ok:
        error = response.json()
        
        if response.status_code == 401:
            # Try to refresh token
            refresh_access_token()
        elif response.status_code == 403:
            print('Insufficient permissions')
        elif response.status_code == 404:
            print('Resource not found')
        else:
            print(f'API error: {error.get("detail")}')
        
        response.raise_for_status()
```

## Related Documentation

- [Authentication API](authentication.md) - Endpoint reference
- [Authentication Guide](../guides/authentication.md) - User guide
- [API Reference](reference.md) - Complete API reference

