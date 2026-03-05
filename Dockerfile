# 🤖 IA Daily Bot - Dockerfile para fly.io
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para caché de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del bot
COPY *.py .
COPY *.json .

# Crear directorios para logs y posts
RUN mkdir -p posts logs triggers social_posts campaign

# Dar permisos
RUN chmod +x *.sh 2>/dev/null || true

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check básico
HEALTHCHECK --interval=60s --timeout=10s --start-period=120s --retries=3 \
    CMD python -c "print('OK')" || exit 1

# Comando por defecto: bot robusto
# En fly.io usa [processes] en fly.toml para múltiples procesos
CMD ["python", "bot_robusto.py"]
