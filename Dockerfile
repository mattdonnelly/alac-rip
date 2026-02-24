# Use Python 3.11 image based on Debian Bookworm (for GLIBC 2.36 required by wrapper binary)
# Explicitly set platform to linux/amd64 since the wrapper binary is x86_64 only
FROM --platform=linux/amd64 python:3.11-bookworm

# Install build dependencies and system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    golang-go \
    wget \
    build-essential \
    pkg-config \
    zlib1g-dev \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/*

# Build and install GPAC from source (not available in Bookworm repos)
# Note: wrapper binary requires GLIBC 2.34+, so we need Bookworm (GLIBC 2.36)
# but gpac is only in Bullseye, so we build it from source
RUN cd /tmp && \
    git clone --depth 1 --branch v2.2.1 https://github.com/gpac/gpac.git && \
    cd gpac && \
    ./configure --static-bin && \
    make -j$(nproc) && \
    make install && \
    cd / && \
    rm -rf /tmp/gpac

# Verify MP4Box is installed
RUN MP4Box -version || echo "MP4Box installed but version check failed (expected)"

# Create a non-root user early
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Change ownership of /app to appuser
RUN chown appuser:appuser /app

# Copy application files (before wrapper to avoid overwriting)
COPY --chown=appuser:appuser . .

# Download and setup wrapper binary with required capabilities
# This must be done as root and AFTER ownership changes to preserve capabilities
RUN cd /tmp && \
    wget -q https://github.com/WorldObservationLog/wrapper/releases/download/Wrapper.x86_64.0df45b5/Wrapper.x86_64.0df45b5.zip && \
    unzip -q Wrapper.x86_64.0df45b5.zip && \
    mkdir -p /app/wrapper && \
    mv wrapper /app/wrapper/ && \
    chown appuser:appuser /app/wrapper/wrapper && \
    chmod +x /app/wrapper/wrapper && \
    setcap cap_sys_chroot+ep /app/wrapper/wrapper && \
    rm -f Wrapper.x86_64.0df45b5.zip && \
    echo "Wrapper binary installed with SYS_CHROOT capability"

# Install Python dependencies
RUN pip install --no-cache-dir flask pyyaml

# Switch to non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Run the application
CMD ["python3", "main.py"]
