import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { ROUTES } from "@/config/routes"
import { useAuth } from "@/features/auth"

export function HomePage() {
  const { isAuthenticated } = useAuth()

  return (
    <div className="container mx-auto flex min-h-[70vh] flex-col items-center justify-center px-4 py-12">
      <div className="flex max-w-xl flex-col items-center gap-8 text-center">
        <div className="space-y-3">
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Resume Agent
          </h1>
          <p className="text-muted-foreground text-lg">
            Upload your resume, generate LaTeX, and edit with a live PDF preview. Set your API keys once and create polished resumes from PDF or Word.
          </p>
        </div>

        <div className="flex flex-wrap justify-center gap-3">
          {isAuthenticated ? (
            <>
              <Button asChild size="lg">
                <Link to={ROUTES.RESUMES}>My resumes</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link to={ROUTES.PROFILE}>Profile & API keys</Link>
              </Button>
            </>
          ) : (
            <>
              <Button asChild size="lg">
                <Link to={ROUTES.LOGIN}>Log in</Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link to={ROUTES.REGISTER}>Create account</Link>
              </Button>
            </>
          )}
        </div>

        {isAuthenticated && (
          <p className="text-muted-foreground text-sm">
            Upload a PDF or Word file, then generate LaTeX and preview the result. Configure OpenAI or DeepSeek in Profile to enable generation.
          </p>
        )}
      </div>
    </div>
  )
}
