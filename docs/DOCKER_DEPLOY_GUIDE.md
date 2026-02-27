# Guia de Deploy com Docker + Java

## 🐳 Deploy Recomendado: Render.com com Docker

### Por que esta solução?
✅ Java instalado no container
✅ Haplogrep3 JAR funciona perfeitamente
✅ Free tier disponível
✅ Deploy automático via GitHub

---

## 📋 Passo a Passo

### 1. Preparar o Projeto

Já criamos os arquivos necessários:
- ✅ `Dockerfile` - Configuração do container com Java
- ✅ `docker-compose.yml` - Para testes locais
- ✅ Wrapper atualizado com suporte a JAR

### 2. Testar Localmente com Docker

```bash
# Build da imagem
docker build -t dnabr-afr .

# Executar container
docker run -p 8501:8501 dnabr-afr

# Ou usar docker-compose
docker-compose up
```

Acesse: http://localhost:8501

### 3. Deploy no Render.com

#### A. Criar conta no Render
1. Acesse: https://render.com
2. Faça login com GitHub
3. Autorize o acesso aos repositórios

#### B. Criar New Web Service
1. Dashboard → "New +" → "Web Service"
2. Conectar repositório: `leandrodavila/dnabr_afr_ufrgs`
3. Configurações:
   - **Name**: `dnabr-afr`
   - **Region**: Escolha mais próxima
   - **Branch**: `main`
   - **Runtime**: `Docker`
   - **Plan**: `Free`

#### C. Configurar Variáveis de Ambiente (opcional)
Se necessário, adicione em "Environment":
```
HAPLOGREP_PATH=/app/haplogrep/haplogrep3.jar
USE_JAR=true
```

#### D. Deploy
1. Clique em "Create Web Service"
2. Aguarde ~5-10 minutos (primeiro build é mais lento)
3. URL estará disponível: `https://dnabr-afr.onrender.com`

---

## 🔧 Atualizar App Streamlit para usar JAR

✅ **JÁ CONFIGURADO!** O `app_streamlit.py` detecta automaticamente o ambiente:

```python
# Detectar ambiente (Docker/Cloud vs Local Windows)
if os.path.exists("/app/haplogrep/haplogrep3.jar"):
    # Ambiente Docker/Cloud (Render.com)
    DEFAULT_HAPLOGREP_PATH = "/app/haplogrep/haplogrep3.jar"
    USE_JAR = True
else:
    # Ambiente local Windows
    DEFAULT_HAPLOGREP_PATH = "C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
    USE_JAR = False

# O wrapper é inicializado com:
wrapper = Haplogrep3Wrapper(
    haplogrep_path=haplogrep_path,
    default_tree=selected_tree,
    use_jar=USE_JAR  # Automaticamente True no Docker
)
```

**Não é necessário configurar nada manualmente!** O app detecta automaticamente se está rodando no Render.com.

---

## 🎯 Alternativas de Deploy

### Opção A: Render.com (Recomendado)
- ✅ Free tier permanente
- ✅ SSL automático
- ✅ Deploy automático via GitHub
- ✅ 750 horas/mês grátis
- ⚠️ Hiberna após 15min de inatividade (free tier)

### Opção B: Railway.app
- ✅ $5 crédito mensal grátis
- ✅ Muito fácil de usar
- ✅ Não hiberna
- ⚠️ Créditos limitados no free tier

### Opção C: Fly.io
- ✅ Free tier generoso
- ✅ Global edge network
- ✅ Não hiberna (com configuração)
- ⚠️ Requer Fly CLI

---

## 📊 Comparação

| Plataforma | Java | Free Tier | Hibernate | SSL | Deploy |
|------------|------|-----------|-----------|-----|--------|
| **Streamlit Cloud** | ❌ Não | ✅ Sim | ❌ Não | ✅ Sim | GitHub |
| **Render** | ✅ Docker | ✅ Sim | ⚠️ Sim | ✅ Sim | GitHub |
| **Railway** | ✅ Docker | ⚠️ $5/mês | ❌ Não | ✅ Sim | GitHub |
| **Fly.io** | ✅ Docker | ✅ Sim | ⚠️ Config | ✅ Sim | CLI |
| **PythonAnywhere** | ❌ Complexo | ✅ Sim | ❌ Não | ✅ Sim | Manual |

---

## 🚀 Próximos Passos

1. **Commit e Push das mudanças:**
   ```bash
   git add Dockerfile docker-compose.yml haplogrep_wrapper/wrapper.py
   git commit -m "Add Docker support with Java for Haplogrep3 JAR"
   git push origin main
   ```

2. **Fazer Deploy:**
   - Siga o passo a passo do Render.com acima
   - Ou escolha outra plataforma

3. **Testar:**
   - Aguarde o build completar
   - Acesse a URL fornecida
   - Teste com um arquivo VCF

---

## 🔍 Troubleshooting

### Problema: Build falha no Docker
**Solução**: Verifique se o arquivo JAR foi baixado corretamente no Dockerfile

### Problema: Java não encontrado
**Solução**: Verifique se `default-jre` foi instalado no Dockerfile

### Problema: Permissões de arquivo
**Solução**: Adicione `RUN chmod +x haplogrep/haplogrep3.jar` no Dockerfile

### Problema: App muito lento
**Solução**: No free tier do Render, o primeiro acesso após hibernação é lento (cold start)

---

## ✅ Checklist de Deploy

- [ ] Dockerfile criado
- [ ] Wrapper atualizado com suporte JAR
- [ ] App Streamlit detecta ambiente automaticamente
- [ ] Testado localmente com Docker
- [ ] Código commitado e pushed para GitHub
- [ ] Conta criada no Render.com
- [ ] Web Service criado e conectado ao repo
- [ ] Build completado com sucesso
- [ ] App testado na URL de produção

---

## 💡 Dicas

1. **Monitoramento**: Render mostra logs em tempo real
2. **Domínio custom**: Pode adicionar seu próprio domínio
3. **Escalabilidade**: Upgrade para plano pago se necessário
4. **Backup**: Mantenha cópia local dos dados importantes
5. **Segurança**: Não commite credenciais ou dados sensíveis

---

## 📞 Suporte

- **Render Docs**: https://render.com/docs
- **Docker Docs**: https://docs.docker.com
- **Streamlit Docs**: https://docs.streamlit.io
