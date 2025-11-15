# Resume Agent

Resume Agent is an intelligent application designed to help job seekers optimize their resumes for specific job descriptions, pass Applicant Tracking Systems (ATS), and effectively track their job applications. The platform uses AI-powered analysis to extract skills from job descriptions, compare them with your existing skills, and generate tailored resumes that maximize your chances of landing interviews.

## Table of Contents

- [Features](#features)
  - [Core Features](#core-features)
  - [Additional Features](#additional-features)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
  - [Using Docker (Recommended)](#using-docker-recommended)
  - [Manual Setup](#manual-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)

## Features

### Core Features

#### 1. Job Description Skill Analysis

Analyze job descriptions to extract required skills and identify related skills that may not be explicitly mentioned. This helps you understand the full scope of what employers are looking for.

#### 2. Skill Gap Comparison

Compare your existing skills against the requirements in a job description. Get a clear breakdown of:

- Skills you already have
- Skills you're missing
- Skills that are related and could strengthen your application

#### 3. Resume Tailoring

Automatically customize your resume to match specific job descriptions while ensuring it passes ATS filters. The system optimizes keyword placement and formatting to avoid AI-generated content detection.

#### 4. LaTeX to PDF Resume Generation

Generate professional, ATS-friendly resumes using LaTeX templates and export them directly to PDF format. This ensures consistent formatting and professional appearance.

#### 5. Feedback System

Receive detailed feedback on your resume based on how well it matches the job description. Get suggestions for improvements, keyword optimization, and content adjustments.

#### 6. Job Application Tracking

Track all your job applications in one place. Each application is linked to its corresponding job description, allowing you to:

- Monitor application status
- Review tailored resumes for each position
- Track application dates and deadlines

#### 7. Template Selection

Choose from multiple professional resume templates optimized for different industries and ATS systems. Each template is designed to maximize readability and keyword visibility.

### Additional Features

The following features are planned to enhance job search effectiveness:

#### Skill Gap Analysis with Learning Resources

When skills are missing, receive recommendations for courses, tutorials, and learning resources to help you acquire those skills quickly.

#### Keyword Optimization

Get suggestions for ATS-friendly keywords based on the job description. The system analyzes industry-specific terminology and suggests the best keywords to include in your resume.

#### Resume Versioning

Maintain multiple versions of your resume for different types of positions. Track changes and compare versions to see which performs best.

#### Cover Letter Generation

Automatically generate tailored cover letters that complement your resume and address specific points in the job description.

#### Interview Preparation

Generate potential interview questions based on the job description and your resume. Practice with questions that are likely to be asked for that specific role.

#### ATS Score Analysis

Get a compatibility score that indicates how well your resume will perform with Applicant Tracking Systems. Receive specific recommendations to improve your score.

#### Resume Comparison Tool

Compare different versions of your resume side-by-side to see which format and content work best for different job types.

#### Application Deadline Tracking

Set reminders for application deadlines and important dates. Never miss an opportunity due to missed deadlines.

#### Export Formats

Export your resume in multiple formats including PDF, Word, LaTeX, and plain text to meet different application requirements.

#### Multi-language Support

Create and manage resumes in different languages for international job applications.

#### Resume Analytics Dashboard

Track your application success rates, ATS scores over time, and identify patterns that lead to more interviews and job offers.

#### Market Demand Analysis

Analyze keywords and skills from all job descriptions you've applied to across your application history. The system aggregates data from your job applications to identify which skills are most frequently requested in the market. Get insights on trending skills, understand market demand patterns, and discover which skills are highly sought after by employers. This helps you prioritize which skills to learn or highlight based on real market demand, making your job search more strategic and effective.

#### Company Research Integration

Link company information and research to your job applications. Keep notes about company culture, values, and recent news to help with interviews.

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
- **Orchestration**: Docker Compose
- **Development**: Hot-reload enabled development containers

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
   cp .env.example backend/.env
   ```

   Edit `backend/.env` with your configuration:

   ```env
   POSTGRES_DB=resume_agent
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=postgres
   POSTGRES_PORT=5432
   DEBUG=true
   ```

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
   - Frontend: <http://localhost:3000> (when frontend is set up)

### Manual Setup

For detailed manual setup instructions, see:

- [backend/README.md](backend/README.md) - Backend manual setup
- [frontend/README.md](frontend/README.md) - Frontend manual setup

## Usage

> **Note**: Detailed usage documentation will be available in the respective directory READMEs. See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for more information.

### Basic Workflow

1. **Upload or Create Your Resume**
   - Start by uploading your existing resume or creating a new one using one of the available templates.

2. **Add a Job Description**
   - Paste or upload a job description you're interested in applying for.

3. **Analyze Skills**
   - The system will extract required skills from the job description and suggest related skills.

4. **Review Skill Gap**
   - See which skills you have, which you're missing, and get recommendations for improvement.

5. **Tailor Your Resume**
   - Use the resume tailoring feature to automatically optimize your resume for the specific job description.

6. **Generate PDF**
   - Export your tailored resume as a professional PDF using LaTeX templates.

7. **Track Application**
   - Save the job application with the tailored resume for future reference and tracking.

8. **Get Feedback**
   - Review feedback on how well your resume matches the job description and make improvements.

To be continued...

## Project Structure

```text
resume-agent/
├── backend/
│   ├── alembic/              # Database migration files
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/        # Migration versions
│   ├── src/                 # Main source code
│   │   ├── auth/            # Authentication module
│   │   │   └── config.py
│   │   ├── config.py        # Application configuration
│   │   ├── database.py      # Database connection and setup
│   │   ├── exceptions.py    # Custom exception classes
│   │   ├── main.py          # FastAPI application entry point
│   │   └── pagination.py    # Pagination utilities
│   ├── tests/               # Test files
│   ├── templates/           # Template files
│   ├── scripts/             # Utility scripts
│   │   ├── lint.sh          # Linting script
│   │   └── migrate.sh       # Migration script
│   ├── alembic.ini          # Alembic configuration
│   ├── dev.Dockerfile       # Development Dockerfile
│   ├── entrypoint.sh        # Docker entrypoint script
│   ├── Pipfile              # Python dependencies
│   ├── Pipfile.lock         # Locked dependencies
│   └── pyproject.toml       # Python project configuration
├── frontend/                # Frontend React application
│   └── (to be implemented)
├── docker-compose.dev.yml   # Docker Compose configuration
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Development

> **Note**: For detailed development documentation, including code style guidelines, testing, linting, and database migrations, see [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md).

### Development Workflow

1. Create a feature branch from `main`
2. Make your changes following the code style guidelines (see directory-specific READMEs)
3. Write tests for new features
4. Run linting and tests
5. Create a pull request

## Documentation

For detailed documentation, please refer to:

- [backend/README.md](backend/README.md) - Backend-specific documentation (API details, database setup, etc.)
- [frontend/README.md](frontend/README.md) - Frontend-specific documentation (component structure, build process, etc.)

## Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork the repository** and create a feature branch
2. **Follow the code style** guidelines mentioned above
3. **Write tests** for new features and ensure all tests pass
4. **Update documentation** as needed (including directory-specific READMEs)
5. **Submit a pull request** with a clear description of your changes

### Reporting Issues

If you encounter any bugs or have feature requests, please open an issue on the repository with:

- A clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Any relevant error messages or logs
