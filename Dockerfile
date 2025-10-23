FROM python:3.11-slim AS base

# Define o diretório de trabalho
WORKDIR /app

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential && \
    rm -rf /var/lib/apt/lists/*

# Instala o gerenciador uv (mais rápido que pip)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Adiciona o binário do uv ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Copia o pyproject e o lockfile se existir
COPY pyproject.toml ./
COPY uv.lock ./

# Instala as dependências do projeto (modo produção)
RUN uv sync --frozen --no-dev

# Copia o código da aplicação
COPY . .

# Expõe a porta padrão do FastAPI
EXPOSE 8000

# Comando de execução com Gunicorn + Uvicorn
CMD ["uv", "run", "gunicorn", "src.main:app", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "120"]



