FROM python:3.11-slim

# Temel sistem bağımlılıkları, Node.js ve derleme araçları
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    procps \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-tur \
    libgl1 \
    libglib2.0-0 \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python bağımlılıklarını kur
COPY scripts/training/requirements-train.txt ./requirements-train.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    numpy \
    rank-bm25 \
    networkx \
    psutil \
    requests \
    orjson \
    diskcache \
    PyMuPDF

# Node bağımlılıklarını kur
COPY package.json ./
RUN npm install --omit=dev || npm install

# Kaynak kodları kopyala
COPY . .

# Entrypoint izinleri
RUN chmod +x docker/entrypoint.sh

# Web ve Dashboard Portları
EXPOSE 3000 8085

ENTRYPOINT ["/app/docker/entrypoint.sh"]
