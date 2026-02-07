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
import { Input } from "@/components/ui/input"
import { ROUTES } from "@/config/routes"
import { useAuth } from "@/features/auth"
import { formatDate } from "@/lib/format"
import * as llmConfigApi from "@/api/llm-config"
import type { LLMConfigStatus } from "@/api/llm-config"

const PROVIDER_LABELS: Record<string, string> = {
  openai: "OpenAI (ChatGPT)",
  deepseek: "DeepSeek",
}

export function ProfilePage() {
  const navigate = useNavigate()
  const { user, logout, accessToken } = useAuth()
  const [llmConfigs, setLlmConfigs] = useState<LLMConfigStatus[]>([])
  const [apiKeyInputs, setApiKeyInputs] = useState<Record<string, string>>({})
  const [saving, setSaving] = useState<string | null>(null)

  useEffect(() => {
    if (!accessToken) return
    llmConfigApi
      .getMyLLMConfig(accessToken)
      .then((r) => setLlmConfigs(r.configs))
      .catch(() => {})
  }, [accessToken])

  function handleSaveKey(provider: string) {
    const key = apiKeyInputs[provider]?.trim()
    if (!key || !accessToken) return
    setSaving(provider)
    llmConfigApi
      .setLLMConfig(provider, key, accessToken)
      .then(() => {
        toast.success(`${PROVIDER_LABELS[provider] || provider} key saved`)
        setApiKeyInputs((prev) => ({ ...prev, [provider]: "" }))
        llmConfigApi.getMyLLMConfig(accessToken).then((r) => setLlmConfigs(r.configs))
      })
      .catch((e) => toast.error(e instanceof Error ? e.message : "Failed to save"))
      .finally(() => setSaving(null))
  }

  if (!user) {
    return null
  }

  function handleLogout() {
    logout()
    navigate(ROUTES.HOME, { replace: true })
  }

  return (
    <div className="container mx-auto max-w-2xl px-4 py-8">
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Profile</h1>
        <Button variant="outline" onClick={handleLogout}>
          Log out
        </Button>
      </div>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Account</CardTitle>
          <CardDescription>Your account details.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <span className="text-muted-foreground text-sm">Name</span>
            <p className="font-medium">
              {user.firstname} {user.lastname}
            </p>
          </div>
          <div>
            <span className="text-muted-foreground text-sm">Email</span>
            <p className="font-medium">{user.email}</p>
          </div>
          <div>
            <span className="text-muted-foreground text-sm">Phone</span>
            <p className="font-medium">{user.phone_number ?? "—"}</p>
          </div>
          <div>
            <span className="text-muted-foreground text-sm">Roles</span>
            <p className="font-medium">{user.roles.length ? user.roles.join(", ") : "—"}</p>
          </div>
          <div>
            <span className="text-muted-foreground text-sm">Registered</span>
            <p className="font-medium">{formatDate(user.registration_date)}</p>
          </div>
          <div>
            <span className="text-muted-foreground text-sm">Last login</span>
            <p className="font-medium">{formatDate(user.last_login)}</p>
          </div>
        </CardContent>
      </Card>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle>API keys (for LaTeX generation)</CardTitle>
          <CardDescription>
            Set your API keys to generate LaTeX from resumes. Keys are stored encrypted.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {llmConfigs.map((c) => (
            <div
              key={c.provider}
              className="grid grid-cols-[8rem_6rem_1fr_auto] items-center gap-3 gap-y-2 sm:gap-4"
            >
              <span className="text-sm font-medium">
                {PROVIDER_LABELS[c.provider] || c.provider}
              </span>
              <span className="flex min-w-24 items-center gap-1.5 text-xs">
                <span
                  className={`size-2 shrink-0 rounded-full ${c.configured ? "bg-green-500" : "bg-muted-foreground/60"}`}
                  aria-hidden
                />
                <span className={c.configured ? "text-green-700 dark:text-green-400" : "text-muted-foreground"}>
                  {c.configured ? "Saved" : "Not set"}
                </span>
              </span>
              <div className="relative min-w-0">
                <Input
                  type="password"
                  placeholder={c.configured ? "••••••••" : "Paste API key here"}
                  className={`min-w-0 ${c.configured ? "border-green-200 bg-green-50/50 dark:border-green-900/50 dark:bg-green-950/20" : ""}`}
                  value={apiKeyInputs[c.provider] ?? ""}
                  onChange={(e) =>
                    setApiKeyInputs((prev) => ({ ...prev, [c.provider]: e.target.value }))
                  }
                />
              </div>
              <Button
                size="sm"
                className="shrink-0"
                onClick={() => handleSaveKey(c.provider)}
                disabled={saving === c.provider}
              >
                {saving === c.provider ? "Saving…" : c.configured ? "Update" : "Save"}
              </Button>
            </div>
          ))}
        </CardContent>
      </Card>

      {(user.street_address || user.city || user.state || user.zip_code || user.country) && (
        <Card>
          <CardHeader>
            <CardTitle>Address</CardTitle>
            <CardDescription>Your address on file.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-1">
            {user.street_address && <p>{user.street_address}</p>}
            <p>
              {[user.city, user.state, user.zip_code].filter(Boolean).join(", ")}
              {user.country ? ` ${user.country}` : ""}
            </p>
          </CardContent>
        </Card>
      )}

      <p className="mt-6 text-center text-sm text-muted-foreground">
        <Link to={ROUTES.HOME} className="underline underline-offset-4">
          Back to home
        </Link>
      </p>
    </div>
  )
}
