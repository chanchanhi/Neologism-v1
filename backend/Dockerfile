FROM python:3.10

RUN apt update && apt install -y \
    wget \
    unzip \
    curl \
    chromium \
    chromium-driver
    
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install cryptography

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]