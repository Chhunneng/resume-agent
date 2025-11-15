FROM python:3.11-slim

# Install pipenv
RUN pip install pipenv

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
