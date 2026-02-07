import { authFetch, handleResponse } from "./client"

export interface LLMConfigStatus {
  provider: string
  configured: boolean
  model_name: string | null
}

export interface LLMConfigListResponse {
  configs: LLMConfigStatus[]
}

export async function getMyLLMConfig(accessToken: string): Promise<LLMConfigListResponse> {
  const res = await authFetch("/v1/users/me/llm-config", { method: "GET" }, accessToken)
  return handleResponse(res)
}

export async function setLLMConfig(
  provider: string,
  apiKey: string,
  accessToken: string
): Promise<void> {
  const res = await authFetch("/v1/users/me/llm-config", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ provider, api_key: apiKey }),
  }, accessToken)
  await handleResponse(res)
}
