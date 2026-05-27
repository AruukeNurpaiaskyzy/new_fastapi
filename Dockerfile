FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости (минимально)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем только requirements.txt сначала (для лучшего кэширования)
COPY requirements.txt .

# Устанавливаем Python пакеты с улучшенными настройками сети
RUN pip install --no-cache-dir \
    --default-timeout=100 \
    --retries=10 \
    --index-url https://pypi.org/simple/ \
    --extra-index-url https://mirrors.aliyun.com/pypi/simple/ \
    --trusted-host mirrors.aliyun.com \
    -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем непривилегированного пользователя
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]