# syntax=docker/dockerfile:1

# 1. Definimos la versión base 
FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. Etapa de Construcción ("La Cocina")
FROM base AS builder

# Instalamos herramientas para compilar conectores de MySQL (LO QUE FALTABA)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Creamos el entorno virtual e instalamos librerías
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

# 3. Etapa Final ("El Comedor") - Solo lo necesario para correr
FROM base AS final

# Instalamos solo la librería de ejecución de MySQL (más ligera que la de desarrollo)
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Copiamos el entorno virtual preparado en la etapa anterior
COPY --from=builder /app/.venv /app/.venv
COPY . .

# Usuario de seguridad
RUN useradd -m myuser
USER myuser

# Activamos el entorno virtual automáticamente
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]