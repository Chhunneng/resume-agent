# Backend Documentation

This directory contains the backend implementation of Resume Agent, built with FastAPI, PostgreSQL, and Python.

## Overview

The backend provides a RESTful API for resume analysis, job description processing, skill matching, and resume generation. It uses AI-powered analysis through LangChain and LangGraph to extract skills, compare resumes with job descriptions, and generate tailored resumes.

## Status

To be continued...

This documentation will be expanded with detailed information about:

- API endpoints and usage
- Database schema and migrations
- Authentication and authorization
- Environment configuration
- Development setup and workflow
- Testing guidelines
- Deployment instructions

## Development Setup

### Pre-commit Hooks

This project uses pre-commit hooks to automatically run Ruff linting and formatting before each commit. This ensures code quality and consistency.

#### Installation

1. **Install dependencies** (if not already done):
   ```bash
   pipenv install --dev
   ```

2. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

   This will set up the git hooks in your `.git/hooks/` directory.

#### Usage

Once installed, pre-commit hooks will automatically run when you make a commit. The hooks will:

- Run `ruff check --fix` on staged Python files in `backend/src/` to catch and auto-fix linting issues
- Run `ruff format` on staged Python files in `backend/src/` to ensure consistent formatting

If the hooks find issues that can't be auto-fixed, the commit will be blocked. Fix the issues and try committing again.

#### Manual Execution

You can manually run the pre-commit hooks on all files (not just staged ones):

```bash
pre-commit run --all-files
```

#### Updating Hooks

To update the pre-commit hooks to their latest versions:

```bash
pre-commit autoupdate
```

#### Skipping Hooks (Not Recommended)

If you need to skip the hooks for a specific commit (not recommended), you can use:

```bash
git commit --no-verify
```

However, this should only be used in exceptional circumstances, as it bypasses the code quality checks.

