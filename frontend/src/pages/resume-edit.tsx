import { useEffect, useRef, useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { toast } from "sonner"
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { ResizeHandle } from "@/components/resize-handle"
import { ROUTES } from "@/config/routes"
import { useAuth } from "@/features/auth"
import { useResizePanel } from "@/hooks/use-resize-panel"
import * as resumesApi from "@/api/resumes"
import type { ResumeDetail } from "@/api/resumes"
import {
  DEFAULT_LEFT_PX,
  MAX_PANEL_PERCENT,
  MIN_PANEL_PX,
  PROVIDERS,
} from "./resume-edit.constants"

export function ResumeEditPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { isAuthenticated, accessToken } = useAuth()
  const [resume, setResume] = useState<ResumeDetail | null>(null)
  const [loading, setLoading] = useState(true)
  const [latex, setLatex] = useState("")
  const [saving, setSaving] = useState(false)
  const [generating, setGenerating] = useState(false)
  const [selectedProvider, setSelectedProvider] = useState<string>("openai")
  const [previewPdfUrl, setPreviewPdfUrl] = useState<string | null>(null)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [previewError, setPreviewError] = useState<string | null>(null)
  const prevUrlRef = useRef<string | null>(null)

  const {
    leftPanelPx,
    panelContainerRef,
    resizeHandleRef,
    handleResizeStart,
  } = useResizePanel({
    minPx: MIN_PANEL_PX,
    maxPercent: MAX_PANEL_PERCENT,
    defaultPx: DEFAULT_LEFT_PX,
  })

  const resumeId = id ? parseInt(id, 10) : NaN

  useEffect(() => {
    if (!isAuthenticated) {
      navigate(ROUTES.LOGIN, { replace: true })
      return
    }
    if (!accessToken || !Number.isInteger(resumeId)) return
    resumesApi
      .getResume(resumeId, accessToken)
      .then((r) => {
        setResume(r)
        setLatex(r.latex_content || "")
      })
      .catch((e) => {
        toast.error(e instanceof Error ? e.message : "Failed to load resume")
        navigate(ROUTES.RESUMES)
      })
      .finally(() => setLoading(false))
  }, [isAuthenticated, accessToken, resumeId, navigate])

  useEffect(() => {
    return () => {
      if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current)
    }
  }, [])

  function handlePreview() {
    if (!latex.trim() || !accessToken) {
      toast.error("Add LaTeX content first")
      return
    }
    setPreviewError(null)
    setPreviewLoading(true)
    resumesApi
      .previewPdf(latex, accessToken)
      .then((blob) => {
        if (prevUrlRef.current) URL.revokeObjectURL(prevUrlRef.current)
        const url = URL.createObjectURL(blob)
        prevUrlRef.current = url
        setPreviewPdfUrl(url)
        setPreviewError(null)
      })
      .catch((e) => {
        setPreviewPdfUrl(null)
        setPreviewError(e instanceof Error ? e.message : "Preview failed")
      })
      .finally(() => setPreviewLoading(false))
  }

  function handleGenerate() {
    if (!accessToken || !Number.isInteger(resumeId)) return
    setGenerating(true)
    resumesApi
      .generateLatex(resumeId, selectedProvider, accessToken)
      .then((r) => {
        setLatex(r.latex_content)
        setResume((prev) => (prev ? { ...prev, latex_content: r.latex_content } : null))
        toast.success("LaTeX generated")
      })
      .catch((e) => toast.error(e instanceof Error ? e.message : "Generate failed"))
      .finally(() => setGenerating(false))
  }

  function handleSave() {
    if (!accessToken || !Number.isInteger(resumeId)) return
    setSaving(true)
    resumesApi
      .updateResume(resumeId, { latex_content: latex }, accessToken)
      .then(() => toast.success("Saved"))
      .catch((e) => toast.error(e instanceof Error ? e.message : "Save failed"))
      .finally(() => setSaving(false))
  }

  if (!isAuthenticated || loading) return null
  if (!resume) return null

  return (
    <div className="flex h-[calc(100vh-2rem)] flex-col gap-2 px-2 py-2 md:px-3">
      <div className="flex shrink-0 flex-wrap items-center justify-between gap-2">
        <div className="min-w-0">
          <h1 className="truncate text-lg font-bold">{resume.title}</h1>
          <p className="truncate text-muted-foreground text-xs">
            {resume.source_file_name} · {resume.source_file_type}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-1.5">
          <select
            className="h-8 rounded border bg-background px-2 text-xs"
            value={selectedProvider}
            onChange={(e) => setSelectedProvider(e.target.value)}
          >
            {PROVIDERS.map((p) => (
              <option key={p.id} value={p.id}>
                {p.label}
              </option>
            ))}
          </select>
          <Button
            size="sm"
            className="h-8 text-xs"
            onClick={handleGenerate}
            disabled={generating || !resume.extracted_text}
          >
            {generating ? "Generating…" : "Generate LaTeX"}
          </Button>
          <Button size="sm" variant="outline" className="h-8 text-xs" onClick={handleSave} disabled={saving}>
            {saving ? "Saving…" : "Save"}
          </Button>
          <Button size="sm" variant="outline" className="h-8 text-xs" onClick={handlePreview} disabled={previewLoading || !latex.trim()}>
            {previewLoading ? "Compiling…" : "Preview PDF"}
          </Button>
          <Button size="sm" variant="ghost" className="h-8 text-xs" asChild>
            <Link to={ROUTES.RESUMES}>Back</Link>
          </Button>
        </div>
      </div>

      <div
        ref={panelContainerRef}
        className="flex min-h-0 flex-1 gap-0 overflow-hidden"
      >
        <Card
          className="flex shrink-0 flex-col overflow-hidden"
          style={{ width: leftPanelPx }}
        >
          <CardHeader className="shrink-0 space-y-0 px-3 py-2">
            <CardTitle className="text-sm">LaTeX source</CardTitle>
            <CardDescription className="text-xs">Edit below and click Save. Click Preview to see PDF.</CardDescription>
          </CardHeader>
          <CardContent className="min-h-0 flex-1 overflow-hidden p-2">
            <textarea
              className="h-full min-h-[200px] w-full resize-none rounded border bg-muted/30 p-2 font-mono text-xs leading-snug"
              value={latex}
              onChange={(e) => setLatex(e.target.value)}
              placeholder="Generate LaTeX or paste your own..."
              spellCheck={false}
            />
          </CardContent>
        </Card>
        <ResizeHandle ref={resizeHandleRef} onResizeStart={handleResizeStart} />
        <Card className="flex min-w-0 flex-1 flex-col overflow-hidden">
          <CardHeader className="shrink-0 space-y-0 px-3 py-2">
            <CardTitle className="text-sm">Preview</CardTitle>
            <CardDescription className="text-xs">
              Click &quot;Preview PDF&quot; to compile and show the PDF. No request until you click.
            </CardDescription>
          </CardHeader>
          <CardContent className="min-h-0 flex-1 overflow-hidden p-2">
            <div className="flex h-full min-h-[300px] flex-col overflow-auto rounded border bg-muted/20">
              {previewLoading && (
                <p className="p-2 text-muted-foreground text-xs">Compiling PDF…</p>
              )}
              {previewError && (
                <p className="p-2 text-destructive text-xs">{previewError}</p>
              )}
              {previewPdfUrl && !previewLoading && (
                <iframe
                  title="LaTeX PDF preview"
                  src={previewPdfUrl}
                  className="min-h-full flex-1 border-0"
                />
              )}
              {!previewPdfUrl && !previewLoading && !previewError && (
                <p className="p-2 text-muted-foreground text-xs">
                  Add LaTeX and click &quot;Preview PDF&quot; to see the compiled PDF here.
                </p>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
