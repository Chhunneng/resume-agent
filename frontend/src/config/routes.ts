import { createElement, type ReactNode } from "react"
import { HomePage } from "@/pages/home"
import { LoginPage } from "@/pages/login"
import { ProfilePage } from "@/pages/profile"
import { RegisterPage } from "@/pages/register"
import { ResumeEditPage } from "@/pages/resume-edit"
import { ResumesPage } from "@/pages/resumes"

export const ROUTES = {
  HOME: "/",
  LOGIN: "/login",
  REGISTER: "/register",
  PROFILE: "/profile",
  RESUMES: "/resumes",
  RESUME_EDIT: (id: number) => `/resumes/${id}`,
} as const

export interface RouteConfigItem {
  path: string
  element: ReactNode
  protected?: boolean
}

export const ROUTE_CONFIG: RouteConfigItem[] = [
  { path: "", element: createElement(HomePage) },
  { path: "login", element: createElement(LoginPage) },
  { path: "register", element: createElement(RegisterPage) },
  { path: "profile", element: createElement(ProfilePage), protected: true },
  { path: "resumes", element: createElement(ResumesPage), protected: true },
  { path: "resumes/:id", element: createElement(ResumeEditPage), protected: true },
]
