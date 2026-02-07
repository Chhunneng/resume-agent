export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  firstname: string
  lastname: string
  phone_number?: string | null
  street_address?: string | null
  city?: string | null
  state?: string | null
  zip_code?: string | null
  country?: string | null
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface UserResponse {
  id: number
  email: string
  firstname: string
  lastname: string
  phone_number: string | null
  registration_date: string
  last_login: string | null
  is_active: boolean
  roles: string[]
  street_address: string | null
  city: string | null
  state: string | null
  zip_code: string | null
  country: string | null
  created_at: string
  updated_at: string
}
