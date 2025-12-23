# Dockerfile
# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Define variáveis de ambiente para evitar arquivos .pyc e logs em buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependências do sistema necessárias para compilar pacotes Python
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install poetry

# Configura o Poetry para não criar virtualenv (já estamos no container isolado)
RUN poetry config virtualenvs.create false

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência primeiro (para aproveitar o cache do Docker)
COPY pyproject.toml poetry.lock* ./

# Instala as dependências (sem as de dev, para simular produção, ou com dev se preferir)
# Vamos instalar tudo por enquanto para facilitar o desenvolvimento
RUN poetry install --no-interaction --no-ansi --no-root

# Copia o restante do código
COPY . .

# Comando padrão para rodar a aplicação (será sobrescrito pelo docker-compose em dev)
CMD ["uvicorn", "src.interface.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
