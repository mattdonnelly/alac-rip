# Use Python 3.11 slim image based on Debian Bullseye (gpac is not available in newer Debian versions)
FROM python:3.11-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    gpac \
    golang-go \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Change ownership of /app to appuser
RUN chown appuser:appuser /app

# Copy application files
COPY --chown=appuser:appuser . .

# Install Python dependencies
RUN pip install --no-cache-dir flask pyyaml

# Switch to non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python3", "main.py"]
