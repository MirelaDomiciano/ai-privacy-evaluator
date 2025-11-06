# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy requirements and install torch CPU first
COPY requirements.txt ./
# Install remaining requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .
# Define a variável de ambiente para desativar a criação de bytecode
ENV PYTHONDONTWRITEBYTECODE 1

# Define a variável de ambiente para desativar o buffer do stdout e stderr
ENV PYTHONUNBUFFERED 1

# Expose port (default for uvicorn)
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
