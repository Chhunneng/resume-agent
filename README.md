# Resume Agent

Resume Agent is a web application for job seekers who want tailored resumes and clear application tracking. You upload PDF or Word resumes and job descriptions. AI analyzes job descriptions, extracts required skills, compares them with your skills, and generates ATS friendly resumes for each role. Source resumes convert to LaTeX for precise control. You edit LaTeX in a resizable split view and preview the compiled PDF in real time. Encrypted storage protects API keys for OpenAI or DeepSeek with automatic token refresh. Application tracking helps you manage submissions and status across roles.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Features

- **Resume upload** – Upload PDF or Word resumes; text is extracted for LaTeX generation.
- **LaTeX generation** – Generate LaTeX from extracted text using OpenAI or DeepSeek (API keys set in Profile).
- **Resume editor** – Edit LaTeX in a resizable panel; click “Preview PDF” to compile and view the PDF (server-side, Overleaf-style).
- **Profile** – Manage account and API keys (encrypted). Clear “Saved” vs “Not set” state per provider.
- **Auth** – Register, login, JWT with refresh; frontend auto-refreshes tokens on 401.

## Technology Stack

### Backend

- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **AI/ML**: LangChain, LangGraph (for skill analysis and resume generation)
- **Document Processing**: LaTeX processing for PDF generation
- **Package Management**: Pipenv

### Frontend

- **Framework**: React
- **Language**: TypeScript
- **UI Library**: Tailwind CSS, Shadcn UI
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with mobile-first responsive design

### Infrastructure

- **Containerization**: Docker
- **Orchestration**: Docker Compose (`docker compose`, not `docker-compose`)
- **Development**: Hot-reload for backend and frontend; backend image includes texlive for LaTeX→PDF preview

## Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)
- **Git**

For manual setup (without Docker):

- **Python** 3.11 or higher
- **Node.js** 18 or higher
- **PostgreSQL** 16 or higher
- **Pipenv** (for Python package management)
- **npm** or **yarn** (for frontend dependencies)

## Installation & Setup

### Using Docker (Recommended)

The easiest way to get started is using Docker Compose, which sets up both the backend and database services.

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd resume-agent
   ```

2. **Set up environment variables**

   ```bash
   cp backend/.env.example backend/.env
   # Optional: cp frontend/.env.example frontend/.env
   ```

   Edit `backend/.env` with your configuration (see `backend/.env.example`). For LaTeX PDF preview and API key encryption you will need `LLM_CONFIG_ENCRYPTION_KEY`; the backend image includes texlive for PDF compilation.

3. **Start the services**

   ```bash
   docker compose -f docker-compose.dev.yml up --build
   ```

4. **Run database migrations**

   ```bash
   docker compose -f docker-compose.dev.yml exec backend-dev alembic upgrade head
   ```

5. **Access the application**

   - Backend API: <http://localhost:8000>
   - API Documentation: <http://localhost:8000/docs>
   - Frontend: <http://localhost:5173>

### Manual Setup

For detailed manual setup instructions, see:

- [backend/README.md](backend/README.md) - Backend manual setup
- [frontend/README.md](frontend/README.md) - Frontend manual setup

## Usage

1. **Register or log in** at the frontend (http://localhost:5173).
2. **Profile → API keys**: Set your OpenAI and/or DeepSeek API keys (stored encrypted). A green “Saved” state indicates the key is set.
3. **Resumes**: Upload a PDF or Word resume. Open it to edit.
4. **Resume editor**: Generate LaTeX (choose provider), edit the source, drag the divider to resize panels, and click “Preview PDF” to compile and view the PDF. Save to persist changes.
5. Use the browser’s Print (e.g. Ctrl+P) to export the preview as PDF if needed.

## Project Structure

```text
resume-agent/
├── backend/
│   ├── alembic/             # Database migrations
│   ├── src/
│   │   ├── auth/            # JWT, RBAC, user management
│   │   ├── database/        # PostgreSQL connection, base models
│   │   ├── documents/       # PDF/Word parsing
│   │   ├── health/          # Health check endpoints
│   │   ├── llm/             # LaTeX generation, encryption, user LLM config
│   │   ├── resumes/         # Resume CRUD, upload, LaTeX→PDF preview
│   │   ├── routes/v1/       # API route aggregation
│   │   ├── config.py
│   │   └── main.py
│   ├── tests/
│   ├── dev.Dockerfile       # Includes texlive for PDF preview
│   ├── Pipfile / Pipfile.lock
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── api/             # Auth client, resumes, LLM config API
│   │   ├── components/      # Layout, UI, resize handle
│   │   ├── config/          # Env, routes (and route config)
│   │   ├── features/auth/  # Auth context, storage
│   │   ├── hooks/           # e.g. useResizePanel
│   │   ├── pages/           # Home, login, register, profile, resumes, resume-edit
│   │   └── routes/          # App routes (map over route config)
│   ├── dev.Dockerfile
│   └── .env.example
├── docs/                    # Guides, API reference, architecture
├── docker-compose.dev.yml   # Postgres, backend-dev, frontend-dev
├── .gitignore
└── README.md
```

## Development

> **Note**: For detailed development documentation, including code style guidelines, testing, linting, and database migrations, see [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md). Use `docker compose -f docker-compose.dev.yml up` for local dev; frontend runs on **port 5173** (Vite).

### Development Workflow

1. Create a feature branch from `main`
2. Make your changes following the code style guidelines (see directory-specific READMEs)
3. Write tests for new features
4. Run linting and tests
5. Create a pull request

## Documentation

Comprehensive documentation is available in the [docs/](docs/) directory:

- **[Documentation Index](docs/README.md)** - Complete documentation hub
- **[Getting Started Guide](docs/guides/getting-started.md)** - First-time setup
- **[API Documentation](docs/api/reference.md)** - Complete API reference
- **[Architecture Documentation](docs/architecture/overview.md)** - System design
- **[Development Guide](docs/development/setup.md)** - Development setup

### Quick Links

- [Backend Documentation](backend/README.md) - Backend setup and API details
- [Frontend Documentation](frontend/README.md) - Frontend setup and structure
- [Authentication Guide](docs/guides/authentication.md) - Using authentication
- [RBAC Setup Guide](docs/guides/rbac-setup.md) - Setting up roles and permissions

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow the code style** guidelines mentioned above
3. **Write tests** for new features and ensure all tests pass
4. **Update documentation** as needed (including directory-specific READMEs)
5. **Follow commit conventions** - We use [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages. See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
6. **Submit a pull request** with a clear description of your changes

For detailed contributing guidelines, including commit message conventions and examples, please see [CONTRIBUTING.md](CONTRIBUTING.md).

### Reporting Issues

If you encounter any bugs or have feature requests, please open an issue on the repository with:

- A clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Any relevant error messages or logs
