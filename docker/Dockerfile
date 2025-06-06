# Use official Python runtime as parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ /app/src/
COPY config/ /app/config/

# Expose port for FastAPI
EXPOSE 8000

# Default command to run the API server
CMD ["uvicorn", "src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]
