FROM python:3.11-slim

# Install pipenv and texlive for LaTeX-to-PDF preview (Overleaf-style)
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/* \
    && pip install pipenv

# Set working directory
WORKDIR /app

ENV PIPENV_VENV_IN_PROJECT=1

# Copy Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv lock --clear && pipenv install --deploy --system

# Copy application code
COPY . .

# Copy and set up entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the application
EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]
CMD ["fastapi", "dev", "src/main.py", "--host", "0.0.0.0", "--reload"]
