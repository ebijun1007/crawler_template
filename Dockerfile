FROM python:3.9

WORKDIR /crawler

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libgomp1 \
    libgbm-dev \
    libasound2 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libxkbcommon0 \
    fonts-unifont \
    fonts-croscore \
    fonts-noto-color-emoji \
    libenchant-2-2 \
    libicu72 \
    libvpx7 \
    libwebp7 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install -r requirements.txt

RUN playwright install