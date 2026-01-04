# -----------------------
# Base image
# -----------------------
FROM python:3.10-slim

# -----------------------
# Set working directory
# -----------------------
WORKDIR /app

# -----------------------
# Install system deps (minimal)
# -----------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# -----------------------
# Copy dependency list first (layer caching)
# -----------------------
COPY requirements.txt .

# -----------------------
# Install Python dependencies
# -----------------------
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# -----------------------
# Copy application code
# -----------------------
COPY api ./api
COPY mlruns ./mlruns

# -----------------------
# Expose API port
# -----------------------
EXPOSE 8000

# -----------------------
# Start FastAPI
# -----------------------
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]


# run -> docker build -t fraud-api:v1 .
# hold -> docker cant install on my company lap, so switching to ci/cd pipeline of github actions

