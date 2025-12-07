FROM python:3.11-slim

WORKDIR /app

# Update package list and install dependencies in one layer with error handling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python packages with increased timeout
RUN pip install --no-cache-dir --timeout=1000 -r requirements.txt

COPY app.py .

# Use PORT environment variable (Render provides this)
ENV PORT=8080
EXPOSE 8080

CMD uvicorn app:app --host 0.0.0.0 --port $PORT
