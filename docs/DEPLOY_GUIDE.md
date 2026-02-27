# Deploy Streamlit - Guia Completo

## 📋 Opções de Deploy

### Opção 1: Streamlit Community Cloud (RECOMENDADO)

#### Vantagens:
- ✅ Gratuito
- ✅ Integração com GitHub
- ✅ Deploy automático
- ✅ SSL/HTTPS incluído
- ✅ Feito especialmente para Streamlit

#### Passos para Deploy:

1. **Prepare o Repositório GitHub**
   - Seu código já está no GitHub: https://github.com/leandrodavila/dnabr_afr_ufrgs.git
   - Certifique-se que todos os arquivos estão commitados

2. **Crie arquivo `.streamlit/config.toml` (opcional)**
   ```toml
   [server]
   headless = true
   port = 8501

   [browser]
   gatherUsageStats = false
   ```

3. **Acesse Streamlit Community Cloud**
   - Visite: https://streamlit.io/cloud
   - Clique em "Sign up" ou "Log in"
   - Conecte sua conta GitHub

4. **Deploy da Aplicação**
   - Clique em "New app"
   - Selecione:
     - Repository: `leandrodavila/dnabr_afr_ufrgs`
     - Branch: `main`
     - Main file path: `app_streamlit.py`
   - Clique em "Deploy!"

5. **Aguarde o Deploy**
   - O Streamlit Cloud instalará as dependências automaticamente
   - Processo leva ~2-5 minutos

6. **Sua Aplicação Estará Online**
   - URL: `https://[seu-app].streamlit.app`

#### ⚠️ Limitações para este Projeto:
- **Haplogrep3 executável não funcionará** porque:
  - O executável Windows (.exe) não roda em Linux (Streamlit Cloud usa Linux)
  - Arquivos binários grandes podem exceder limites

#### Solução:
Você precisará usar a versão JAR do Haplogrep3 ou criar uma imagem Docker customizada.

---

### Opção 2: Heroku (Gratuito com limitações)

#### Requisitos:
- Conta Heroku
- Heroku CLI instalado

#### Limitações:
- Mesma limitação do executável Windows
- Heroku tem plano free limitado

---

### Opção 3: Docker + Render/Railway (Recomendado para produção)

#### Vantagens:
- Controle total do ambiente
- Pode incluir o Haplogrep3
- Free tier disponível

#### Passos básicos:
1. Criar `Dockerfile`
2. Fazer push para GitHub
3. Conectar ao Render.com ou Railway.app
4. Deploy automático

---

### Opção 4: PythonAnywhere (NÃO RECOMENDADO para Streamlit)

#### Por que NÃO usar:
- ❌ PythonAnywhere não suporta Streamlit nativamente
- ❌ Usa WSGI (Flask/Django), não WebSockets
- ❌ Workarounds são complexos e instáveis
- ❌ Não é a ferramenta certa para o trabalho

#### Se ainda quiser tentar (não recomendado):
1. Converter aplicação para Flask (muito trabalho)
2. Usar tunelamento SSH (complexo, instável)
3. Executar em sempre-online task (limitações do free tier)

---

## 🐳 Solução Completa: Docker

Para fazer funcionar em qualquer plataforma (incluindo com o executável Haplogrep3),
a melhor solução é usar Docker:

### Arquivo `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos
COPY requirements.txt .
COPY haplogrep_wrapper/ ./haplogrep_wrapper/
COPY app_streamlit.py .
COPY haplogrep/ ./haplogrep/
COPY setup.py .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

# Expor porta
EXPOSE 8501

# Comando para executar
CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Deploy com Docker:
1. **Render.com**: Detecta Dockerfile automaticamente
2. **Railway.app**: Deploy com um clique
3. **Fly.io**: Ótimo free tier

---

## 📝 Recomendação Final

### Para Desenvolvimento/Teste:
```bash
# Local
streamlit run app_streamlit.py
```

### Para Deploy Rápido (sem executável):
1. **Streamlit Community Cloud** - Mais fácil
2. Modificar código para usar API REST ou versão JAR do Haplogrep3

### Para Deploy Profissional (com executável):
1. **Docker + Render/Railway** - Mais controle
2. Incluir o JAR do Haplogrep3 e Java no container

---

## 🔧 Próximos Passos

Escolha uma opção acima e me diga qual prefere. Posso te ajudar com:
1. Criar Dockerfile completo
2. Configurar para Streamlit Cloud
3. Adaptar código para não usar executável Windows
4. Setup em Render/Railway/Fly.io

---

## ❓ Perguntas Frequentes

**Q: Por que PythonAnywhere não funciona?**
A: PythonAnywhere é para apps WSGI (Flask/Django). Streamlit usa arquitetura diferente com WebSockets.

**Q: Posso rodar Streamlit no PythonAnywhere?**
A: Tecnicamente sim, mas requer configuração muito complexa e não é estável. Não vale a pena.

**Q: Qual é a opção mais simples?**
A: Streamlit Community Cloud, mas você precisará adaptar para não usar o .exe

**Q: Como rodar o Haplogrep3 no Linux?**
A: Use a versão JAR: `java -jar haplogrep3.jar ...`
