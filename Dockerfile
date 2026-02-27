# Dockerfile para Deploy com Haplogrep3 (JAR)
FROM python:3.11-slim

WORKDIR /app

# Instalar Java Runtime Environment
RUN apt-get update && apt-get install -y \
    default-jre \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Verificar instalação do Java
RUN java -version

# Copiar arquivos de dependências
COPY requirements.txt .
COPY setup.py .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY haplogrep_wrapper/ ./haplogrep_wrapper/
COPY app_streamlit.py .
COPY .streamlit/ ./.streamlit/

# Instalar o wrapper em modo desenvolvimento
RUN pip install -e .

# Baixar e extrair Haplogrep3
RUN mkdir -p haplogrep && \
    cd haplogrep && \
    wget https://github.com/genepi/haplogrep3/releases/download/v3.2.2/haplogrep3-3.2.2-linux.zip && \
    unzip haplogrep3-3.2.2-linux.zip && \
    rm haplogrep3-3.2.2-linux.zip && \
    ls -la && \
    cd ..

# Criar diretórios necessários
RUN mkdir -p uploads results VCFs

# Expor porta do Streamlit
EXPOSE 8501

# Comando para executar a aplicação
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
