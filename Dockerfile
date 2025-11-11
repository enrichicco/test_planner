FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for reports
RUN mkdir -p templates/reports output/reports

# Expose port
EXPOSE 8000

CMD ["uvicorn", "src.task_planner.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
