FROM python:3.11-slim

# dependências do chrome e chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg2 \
    ca-certificates \
    libx11-dev \
    libxext6 \
    libxi6 \
    libgconf-2-4 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libdbus-1-3 \
    libxtst6 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libxcomposite1 \
    libxrandr2 \
    libepoxy0 \
    libgbm-dev \
    --no-install-recommends && apt-get clean


RUN apt-get update \
    && apt-get install -y wget curl gnupg2 ca-certificates \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* google-chrome-stable_current_amd64.deb


# Baixar o chromedriver 135
RUN wget https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.114/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver \
    && rm -rf chromedriver-linux64 chromedriver-linux64.zip

# Instalar o Selenium
RUN pip install selenium

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os requisitos e instalar dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código para o container
COPY . /app/

# Comando para iniciar seu app Flask
CMD ["python", "app.py"]
