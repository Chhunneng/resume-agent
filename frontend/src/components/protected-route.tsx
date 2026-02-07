import { Navigate, useLocation } from "react-router-dom"
import { ROUTES } from "@/config/routes"

interface ProtectedRouteProps {
  isAuthenticated: boolean
  children: React.ReactNode
}

export function ProtectedRoute({ isAuthenticated, children }: ProtectedRouteProps) {
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} state={{ from: location }} replace />
  }

  return <>{children}</>
}
