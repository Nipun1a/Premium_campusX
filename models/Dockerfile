# Use a valid Python base image
FROM python:3.10.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY models ./models

# Expose the application port
EXPOSE 8000

# Command to start the FastAPI application
CMD ["uvicorn", "models.app:app", "--host", "0.0.0.0", "--port", "8000"]
