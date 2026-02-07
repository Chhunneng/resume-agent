import { Navigate, Route, Routes } from "react-router-dom"
import { Layout } from "@/components/layout"
import { ProtectedRoute } from "@/components/protected-route"
import { ROUTES, ROUTE_CONFIG } from "@/config/routes"
import { useAuth } from "@/features/auth"

export function AppRoutes() {
  const { isAuthenticated } = useAuth()

  return (
    <Routes>
      <Route element={<Layout />}>
        {ROUTE_CONFIG.map(({ path, element, protected: isProtected }) => (
          <Route
            key={path || "index"}
            {...(path === "" ? { index: true } : { path })}
            element={
              isProtected ? (
                <ProtectedRoute isAuthenticated={isAuthenticated}>
                  {element}
                </ProtectedRoute>
              ) : (
                element
              )
            }
          />
        ))}
        <Route path="*" element={<Navigate to={ROUTES.HOME} replace />} />
      </Route>
    </Routes>
  )
}
