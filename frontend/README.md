# Frontend Documentation

This directory contains the frontend implementation of Resume Agent, built with React, TypeScript, Tailwind CSS, and Shadcn UI.

## Overview

The frontend provides the UI for resume upload, LaTeX editing with a resizable split view, PDF preview (backend-compiled), and profile management (API keys). Auth uses JWT with automatic token refresh on 401.

## Quick Start

### Prerequisites

- **Node.js** 18 or higher
- **npm** or **yarn**

### Installation

```bash
npm install
# or
yarn install
```

### Development

```bash
npm run dev
# or
yarn dev
```

The application will be available at **http://localhost:5173** (Vite default).

### Build

```bash
npm run build
# or
yarn build
```

## Project Structure

```
frontend/
├── src/
│   ├── api/            # Auth client, resumes, LLM config API
│   ├── components/    # Layout, UI, resize handle
│   ├── config/         # Env, route config (routes defined here, rendered in routes/)
│   ├── features/auth/  # Auth context, token storage, refresh on 401
│   ├── hooks/          # e.g. useResizePanel
│   ├── pages/          # Home, login, register, profile, resumes, resume-edit
│   └── routes/         # App router (maps over route config)
├── public/
└── (see docs/ at repo root for guides and API reference)
```

## Technology Stack

- **React**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Shadcn UI**: Component library

## Development Guidelines

### Code Style

- Use TypeScript for all code
- Follow ESLint and Prettier configurations
- Use functional components with hooks
- Keep components small and focused

### Component Structure

- One component per file
- Use TypeScript interfaces for props
- Export components as default

### Styling

- Use Tailwind CSS for styling
- Follow mobile-first responsive design
- Use Shadcn UI components when possible

## API Integration

The frontend communicates with the backend API. See:

- [API Documentation](../../docs/api/reference.md)
- [Authentication Guide](../../docs/guides/authentication.md)
- [API Examples](../../docs/api/examples.md)

## Documentation

### General Documentation

- [Getting Started](../../docs/guides/getting-started.md)
- [Development Setup](../../docs/development/setup.md)
- [Coding Standards](../../docs/development/coding-standards.md)
- [Full Documentation Index](../../docs/README.md)

