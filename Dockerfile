# Usa uma imagem oficial leve do Python
FROM python:3.11-slim

# Evita que o Python gere arquivos .pyc e força log sem buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Define o diretório de trabalho na imagem
WORKDIR /app

# Instala dependências do sistema necessárias para compilar bibliotecas C++ (ex: Chroma/SQLite)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia os requisitos e instala as dependências do Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos do projeto para o container
COPY . /app/

# Expõe a porta padrão do Jupyter Notebook
EXPOSE 8888

# Comando padrão para rodar o Jupyter Server
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]