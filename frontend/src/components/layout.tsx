import { Outlet, Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { ROUTES } from "@/config/routes"
import { useAuth } from "@/features/auth"

export function Layout() {
  const { isAuthenticated } = useAuth()

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b">
        <nav className="container mx-auto flex h-14 items-center justify-between px-4">
          <Link to={ROUTES.HOME} className="font-semibold">
            Resume Agent
          </Link>
          <div className="flex gap-2">
            <Button asChild variant="ghost" size="sm">
              <Link to={ROUTES.HOME}>Home</Link>
            </Button>
            {isAuthenticated ? (
              <>
                <Button asChild variant="ghost" size="sm">
                  <Link to={ROUTES.RESUMES}>Resumes</Link>
                </Button>
                <Button asChild variant="ghost" size="sm">
                  <Link to={ROUTES.PROFILE}>Profile</Link>
                </Button>
              </>
            ) : (
              <>
                <Button asChild variant="ghost" size="sm">
                  <Link to={ROUTES.LOGIN}>Log in</Link>
                </Button>
                <Button asChild variant="ghost" size="sm">
                  <Link to={ROUTES.REGISTER}>Register</Link>
                </Button>
              </>
            )}
          </div>
        </nav>
      </header>
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  )
}
