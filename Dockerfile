FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including OpenCascade
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libfreetype6 \
    libocct-data-exchange-7.6 \
    libocct-draw-7.6 \
    libocct-foundation-7.6 \
    libocct-modeling-algorithms-7.6 \
    libocct-modeling-data-7.6 \
    libocct-ocaf-7.6 \
    libocct-visualization-7.6 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
