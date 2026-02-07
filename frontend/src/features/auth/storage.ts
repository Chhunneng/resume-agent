export const ACCESS_KEY = "resume_agent_access_token"
export const REFRESH_KEY = "resume_agent_refresh_token"

export function loadStoredTokens(): {
  access: string | null
  refresh: string | null
} {
  try {
    const access = localStorage.getItem(ACCESS_KEY)
    const refresh = localStorage.getItem(REFRESH_KEY)
    return { access, refresh }
  } catch {
    return { access: null, refresh: null }
  }
}

export function saveTokens(access: string, refresh: string): void {
  localStorage.setItem(ACCESS_KEY, access)
  localStorage.setItem(REFRESH_KEY, refresh)
}

export function clearTokens(): void {
  localStorage.removeItem(ACCESS_KEY)
  localStorage.removeItem(REFRESH_KEY)
}
