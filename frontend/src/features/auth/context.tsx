import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react"
import * as authApi from "@/api/auth"
import type { LoginRequest, RegisterRequest, UserResponse } from "@/api/types"
import { setRefreshAuth } from "@/api/client"
import { clearTokens, loadStoredTokens, saveTokens } from "./storage"

interface AuthState {
  user: UserResponse | null
  accessToken: string | null
  refreshToken: string | null
  isLoaded: boolean
}

interface AuthContextValue extends AuthState {
  isAuthenticated: boolean
  login: (body: LoginRequest) => Promise<void>
  register: (body: RegisterRequest) => Promise<void>
  logout: () => void
  setUser: (user: UserResponse | null) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AuthState>({
    user: null,
    accessToken: null,
    refreshToken: null,
    isLoaded: false,
  })
  const refreshTokenRef = useRef<string | null>(null)
  refreshTokenRef.current = state.refreshToken

  useEffect(() => {
    const { access, refresh } = loadStoredTokens()
    if (!access) {
      setState((prev) => ({ ...prev, isLoaded: true }))
      return
    }
    setState((prev) => ({ ...prev, accessToken: access, refreshToken: refresh }))
    authApi
      .getMe(access)
      .then((user) => setState((prev) => ({ ...prev, user, isLoaded: true })))
      .catch(() => {
        clearTokens()
        setState((prev) => ({
          ...prev,
          user: null,
          accessToken: null,
          refreshToken: null,
          isLoaded: true,
        }))
      })
  }, [])

  useEffect(() => {
    if (!state.refreshToken) {
      setRefreshAuth(null)
      return
    }
    setRefreshAuth(async () => {
      const refreshToken = refreshTokenRef.current
      if (!refreshToken) {
        clearTokens()
        setState((prev) => ({
          ...prev,
          user: null,
          accessToken: null,
          refreshToken: null,
        }))
        throw new Error("Session expired")
      }
      try {
        const tokens = await authApi.refresh(refreshToken)
        saveTokens(tokens.access_token, tokens.refresh_token)
        setState((prev) => ({
          ...prev,
          accessToken: tokens.access_token,
          refreshToken: tokens.refresh_token,
        }))
        return tokens.access_token
      } catch {
        clearTokens()
        setState((prev) => ({
          ...prev,
          user: null,
          accessToken: null,
          refreshToken: null,
        }))
        throw new Error("Session expired")
      }
    })
    return () => setRefreshAuth(null)
  }, [state.refreshToken])

  const login = useCallback(
    async (body: LoginRequest) => {
      const tokens = await authApi.login(body)
      saveTokens(tokens.access_token, tokens.refresh_token)
      const user = await authApi.getMe(tokens.access_token)
      setState({
        user,
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        isLoaded: true,
      })
    },
    []
  )

  const register = useCallback(
    async (body: RegisterRequest) => {
      const tokens = await authApi.register(body)
      saveTokens(tokens.access_token, tokens.refresh_token)
      const user = await authApi.getMe(tokens.access_token)
      setState({
        user,
        accessToken: tokens.access_token,
        refreshToken: tokens.refresh_token,
        isLoaded: true,
      })
    },
    []
  )

  const logout = useCallback(() => {
    clearTokens()
    setState({
      user: null,
      accessToken: null,
      refreshToken: null,
      isLoaded: true,
    })
  }, [])

  const setUser = useCallback((user: UserResponse | null) => {
    setState((prev) => ({ ...prev, user }))
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      ...state,
      isAuthenticated: !!state.user && !!state.accessToken,
      login,
      register,
      logout,
      setUser,
    }),
    [state, login, register, logout, setUser]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
