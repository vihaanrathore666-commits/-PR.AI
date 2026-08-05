# Use a lightweight, high-performance base image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establish high-performance secure application workspace
WORKDIR /workspace

# Install essential system utilities needed for matrix imaging operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency mappings and execute caching install pipeline
COPY backend/requirements.txt /workspace/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /workspace/backend/requirements.txt

# Copy all application assets cleanly into current container image context
COPY . /workspace/

# Expose internal app cloud container proxy network port
EXPOSE 8000

# Fire up the production-grade application loop directly on system boot
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
