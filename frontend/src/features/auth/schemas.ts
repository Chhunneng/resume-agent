import { z } from "zod"

export const loginSchema = z.object({
  email: z.string().min(1, "Email is required").email("Invalid email"),
  password: z.string().min(1, "Password is required"),
})

export type LoginFormValues = z.infer<typeof loginSchema>

export const registerSchema = z
  .object({
    email: z.string().min(1, "Email is required").email("Invalid email"),
    password: z.string().min(8, "Password must be at least 8 characters"),
    firstname: z.string().min(1, "First name is required").max(100),
    lastname: z.string().min(1, "Last name is required").max(100),
    phone_number: z.string().max(20).optional().or(z.literal("")),
    street_address: z.string().max(255).optional().or(z.literal("")),
    city: z.string().max(100).optional().or(z.literal("")),
    state: z.string().max(100).optional().or(z.literal("")),
    zip_code: z.string().max(20).optional().or(z.literal("")),
    country: z.string().max(100).optional().or(z.literal("")),
  })

export type RegisterFormValues = z.infer<typeof registerSchema>

export const registerDefaultValues: RegisterFormValues = {
  email: "",
  password: "",
  firstname: "",
  lastname: "",
  phone_number: "",
  street_address: "",
  city: "",
  state: "",
  zip_code: "",
  country: "",
}

export function toOptionalString(value: string | undefined): string | null {
  if (value === undefined || value === "") return null
  return value
}
