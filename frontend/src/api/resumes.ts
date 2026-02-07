import { authFetch, handleResponse } from "./client"

export interface ResumeListItem {
  id: number
  title: string
  source_file_name: string
  source_file_type: string
  has_latex: boolean
  created_at: string
}

export interface ResumeDetail {
  id: number
  title: string
  source_file_name: string
  source_file_type: string
  extracted_text: string | null
  latex_content: string | null
  created_at: string
  updated_at: string
}

export interface ResumeListResponse {
  items: ResumeListItem[]
}

export interface GenerateLatexResponse {
  latex_content: string
}

export async function uploadResume(
  file: File,
  accessToken: string
): Promise<{ id: number; title: string; source_file_name: string; source_file_type: string; created_at: string }> {
  const form = new FormData()
  form.append("file", file)
  const res = await authFetch("/v1/resumes/upload", {
    method: "POST",
    body: form,
  }, accessToken)
  return handleResponse(res)
}

export async function listResumes(accessToken: string): Promise<ResumeListResponse> {
  const res = await authFetch("/v1/resumes", { method: "GET" }, accessToken)
  return handleResponse(res)
}

export async function getResume(id: number, accessToken: string): Promise<ResumeDetail> {
  const res = await authFetch(`/v1/resumes/${id}`, { method: "GET" }, accessToken)
  return handleResponse(res)
}

export async function generateLatex(
  resumeId: number,
  provider: string,
  accessToken: string
): Promise<GenerateLatexResponse> {
  const res = await authFetch(`/v1/resumes/${resumeId}/generate-latex`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider }),
  }, accessToken)
  return handleResponse(res)
}

export async function updateResume(
  id: number,
  payload: { title?: string; latex_content?: string },
  accessToken: string
): Promise<ResumeDetail> {
  const res = await authFetch(`/v1/resumes/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  }, accessToken)
  return handleResponse(res)
}

/** Compile LaTeX to PDF (Overleaf-style). Returns PDF blob or throws. */
export async function previewPdf(
  latexContent: string,
  accessToken: string
): Promise<Blob> {
  const res = await authFetch("/v1/resumes/preview-pdf", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ latex_content: latexContent }),
  }, accessToken)
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    const message = typeof data.detail === "string" ? data.detail : "Preview failed"
    throw new Error(message)
  }
  return res.blob()
}
