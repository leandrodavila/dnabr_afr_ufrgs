# Dockerfile para Deploy com Haplogrep3 (JAR)
FROM python:3.11-slim

WORKDIR /app

# Instalar Java Runtime Environment
RUN apt-get update && apt-get install -y \
    default-jre \
    wget \
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

# Baixar Haplogrep3 JAR
# Nota: Ajuste a URL para a versão mais recente
RUN mkdir -p haplogrep && \
    wget -O haplogrep/haplogrep3.jar \
    https://github.com/genepi/haplogrep3/releases/download/v3.2.2/haplogrep3.jar

# Criar diretórios necessários
RUN mkdir -p uploads results VCFs

# Expor porta do Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Comando para executar a aplicação
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
