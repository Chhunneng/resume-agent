import { apiBaseUrl } from "@/config/env"

export function getApiUrl(path: string): string {
  const base = apiBaseUrl.replace(/\/$/, "")
  const normalizedPath = path.startsWith("/") ? path : `/${path}`
  return `${base}${normalizedPath}`
}

export async function handleResponse<T>(res: Response): Promise<T> {
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    const message =
      typeof data.detail === "string"
        ? data.detail
        : Array.isArray(data.detail)
          ? data.detail.map((d: { msg?: string }) => d.msg).join(", ")
          : "Request failed"
    throw new Error(message)
  }
  return data as T
}

/** Called when a request gets 401; should refresh tokens and return new access token. Throw to logout. */
let refreshAuthFn: (() => Promise<string>) | null = null

export function setRefreshAuth(fn: (() => Promise<string>) | null): void {
  refreshAuthFn = fn
}

export async function authFetch(
  path: string,
  options: RequestInit,
  accessToken: string,
  isRetry = false
): Promise<Response> {
  const url = getApiUrl(path)
  const headers = new Headers(options.headers)
  headers.set("Authorization", `Bearer ${accessToken}`)
  const res = await fetch(url, { ...options, headers })

  if (res.status === 401 && !isRetry && refreshAuthFn) {
    try {
      const newToken = await refreshAuthFn()
      return authFetch(path, options, newToken, true)
    } catch {
      throw new Error("Session expired. Please sign in again.")
    }
  }

  return res
}
