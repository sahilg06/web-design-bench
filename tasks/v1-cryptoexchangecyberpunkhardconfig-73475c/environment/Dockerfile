FROM python:3.11-slim

# Install system packages:
#   - fonts-liberation: clean Latin fonts for consistent rendering
#   - libglib2.0-0 etc: Chromium runtime deps needed by Playwright's bundled browser
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-liberation \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libdbus-1-3 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

# Install uv for Python package management
RUN pip install --no-cache-dir uv

# Install Python grader dependencies via uv into the system Python
RUN uv pip install --system \
    playwright==1.44.0 \
    scikit-image==0.23.2 \
    Pillow==10.3.0 \
    numpy==1.26.4 \
    imagehash==4.3.1 \
    opencv-python-headless==4.9.0.80

# Install Playwright's bundled Chromium (version-matched to playwright==1.44.0)
RUN playwright install chromium

# Create required directories
RUN mkdir -p /app/assets /app/output /logs/verifier /logs/agent /tests

# Copy reference screenshots into the image.
# NOTE: Harbor uses environment/ as the Docker build context,
# so assets must be placed at environment/assets/ (not task root assets/).
# The pipeline will populate this directory per task before building.
COPY assets/ /app/assets/

WORKDIR /app
