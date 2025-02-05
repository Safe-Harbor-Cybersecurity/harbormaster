# docker/Dockerfile
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Command to run the application
CMD ["uvicorn", "harbormaster.api.main:app", "--host", "0.0.0.0", "--port", "8000"]