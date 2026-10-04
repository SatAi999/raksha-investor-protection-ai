FROM python:3.10-slim

WORKDIR /app

# System dependencies for OCR, PDF generation, and network utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-hin \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose FastAPI backend port
EXPOSE 8000

CMD ["python", "-m", "backend.app.main"]
