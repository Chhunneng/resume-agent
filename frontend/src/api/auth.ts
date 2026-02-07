import { getApiUrl, handleResponse } from "./client"
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  UserResponse,
} from "./types"

const AUTH_BASE = "/v1/auth"

export async function login(body: LoginRequest): Promise<TokenResponse> {
  const res = await fetch(getApiUrl(`${AUTH_BASE}/login`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return handleResponse<TokenResponse>(res)
}

export async function register(body: RegisterRequest): Promise<TokenResponse> {
  const res = await fetch(getApiUrl(`${AUTH_BASE}/register`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })
  return handleResponse<TokenResponse>(res)
}

export async function refresh(refreshToken: string): Promise<TokenResponse> {
  const res = await fetch(getApiUrl(`${AUTH_BASE}/refresh`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  })
  return handleResponse<TokenResponse>(res)
}

export async function getMe(accessToken: string): Promise<UserResponse> {
  const res = await fetch(getApiUrl(`${AUTH_BASE}/me`), {
    method: "GET",
    headers: { Authorization: `Bearer ${accessToken}` },
  })
  return handleResponse<UserResponse>(res)
}
