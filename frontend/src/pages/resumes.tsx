import { useEffect, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { ROUTES } from "@/config/routes"
import { useAuth } from "@/features/auth"
import * as resumesApi from "@/api/resumes"
import type { ResumeListItem } from "@/api/resumes"

export function ResumesPage() {
  const navigate = useNavigate()
  const { isAuthenticated, accessToken } = useAuth()
  const [items, setItems] = useState<ResumeListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)

  useEffect(() => {
    if (!isAuthenticated || !accessToken) {
      navigate(ROUTES.LOGIN, { replace: true })
      return
    }
    resumesApi
      .listResumes(accessToken)
      .then((r) => setItems(r.items))
      .catch((e) => toast.error(e instanceof Error ? e.message : "Failed to load resumes"))
      .finally(() => setLoading(false))
  }, [isAuthenticated, accessToken, navigate])

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file || !accessToken) return
    setUploading(true)
    resumesApi
      .uploadResume(file, accessToken)
      .then((resume) => {
        toast.success("Resume uploaded")
        setItems((prev) => [
          {
            id: resume.id,
            title: resume.title,
            source_file_name: resume.source_file_name,
            source_file_type: resume.source_file_type,
            has_latex: false,
            created_at: resume.created_at,
          },
          ...prev,
        ])
        navigate(ROUTES.RESUME_EDIT(resume.id))
      })
      .catch((e) => toast.error(e instanceof Error ? e.message : "Upload failed"))
      .finally(() => {
        setUploading(false)
        e.target.value = ""
      })
  }

  if (!isAuthenticated) return null

  return (
    <div className="container mx-auto max-w-4xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Resumes</h1>
        <label className="cursor-pointer">
          <input
            type="file"
            accept=".pdf,.docx"
            className="hidden"
            onChange={handleFileChange}
            disabled={uploading}
          />
          <Button asChild disabled={uploading}>
            <span>{uploading ? "Uploading…" : "Upload resume"}</span>
          </Button>
        </label>
      </div>
      <p className="text-muted-foreground mb-4 text-sm">
        Upload a PDF or Word resume. Then generate LaTeX and edit it with live preview.
      </p>
      {loading ? (
        <p className="text-muted-foreground">Loading…</p>
      ) : items.length === 0 ? (
        <Card>
          <CardHeader>
            <CardTitle>No resumes yet</CardTitle>
            <CardDescription>Upload a PDF or Word document to get started.</CardDescription>
          </CardHeader>
          <CardContent>
            <label className="cursor-pointer">
              <input
                type="file"
                accept=".pdf,.docx"
                className="hidden"
                onChange={handleFileChange}
                disabled={uploading}
              />
              <Button>{uploading ? "Uploading…" : "Upload your first resume"}</Button>
            </label>
          </CardContent>
        </Card>
      ) : (
        <ul className="space-y-3">
          {items.map((r) => (
            <Card key={r.id}>
              <CardHeader className="flex flex-row items-center justify-between py-4">
                <div>
                  <CardTitle className="text-lg">{r.title}</CardTitle>
                  <CardDescription>
                    {r.source_file_name} · {r.source_file_type}
                    {r.has_latex ? " · LaTeX generated" : ""}
                  </CardDescription>
                </div>
                <Button asChild variant="default">
                  <Link to={ROUTES.RESUME_EDIT(r.id)}>Edit</Link>
                </Button>
              </CardHeader>
            </Card>
          ))}
        </ul>
      )}
    </div>
  )
}
