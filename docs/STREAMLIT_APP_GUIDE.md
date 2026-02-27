# Guia de Uso - Aplicação Streamlit

## Aplicação Web para Classificação de Haplogrupos

Este guia explica como usar a aplicação Streamlit para classificar haplogrupos mitocondriais.

## Instalação

1. Certifique-se de que o ambiente virtual está ativado:

   ```bash
   # Windows
   .\venv\Scripts\activate
   ```

2. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

## Iniciando a Aplicação

Execute o seguinte comando no terminal:

```bash
streamlit run app_streamlit.py
```

A aplicação abrirá automaticamente no seu navegador em: `http://localhost:8501`

## Como Usar

### 1. Configurações (Barra Lateral)

#### Caminho do Haplogrep3
- Por padrão: `C:/repos/dnabr_afr/haplogrep/haplogrep3.exe`
- Ajuste se necessário para o caminho correto na sua máquina

#### Árvore Filogenética
- **Recomendado**: PhyloTree 17 - Forensic Update 1.2
- Outras opções disponíveis para compatibilidade com estudos anteriores

#### Métrica de Classificação
- **Kulczynski** (Padrão): Medida de similaridade Kulczynski
- **Hamming**: Distância de Hamming
- **Jaccard**: Índice de Jaccard

#### Opções Avançadas
- **Relatório Estendido**: Inclui informações detalhadas sobre SNPs
- **Número de hits**: Quantidade de melhores resultados (1-10)
- **Nível de Heteroplasmia**: Limiar para incluir heteroplasmias (0.0-1.0)

### 2. Upload do Arquivo VCF

1. Clique no botão "Browse files" ou arraste o arquivo VCF
2. Formatos aceitos: `.vcf`
3. O tamanho do arquivo será exibido após o upload

### 3. Classificação

1. Clique no botão **"🚀 Classificar Haplogrupo"**
2. Aguarde o processamento (pode levar alguns segundos)
3. Os resultados aparecerão na área "Resultados"

### 4. Visualização dos Resultados

Os resultados são exibidos em três abas:

#### 📋 Resultados Principais
- Haplogrupos classificados de forma estruturada
- Métricas principais em destaque
- Fácil visualização dos dados mais importantes

#### 📄 Resultado Completo
- Saída completa do Haplogrep3
- Área de texto com todos os detalhes
- Botão para **baixar os resultados** em formato TXT

#### ℹ️ Informações Técnicas
- Configurações utilizadas na análise
- Parâmetros avançados aplicados
- Saída padrão (stdout) do comando
- Código de retorno da execução

## Exemplos de Uso

### Análise Padrão

```
1. Upload: meu_arquivo.vcf
2. Configurações: Manter padrão
3. Clicar em "Classificar Haplogrupo"
4. Visualizar resultados e baixar
```

### Análise com Múltiplos Candidatos

```
1. Upload: amostra_complexa.vcf
2. Opções Avançadas:
   - Número de hits: 5
   - Relatório Estendido: ✓
3. Clicar em "Classificar Haplogrupo"
4. Analisar os 5 melhores candidatos
```

### Análise com Árvore Específica

```
1. Upload: amostra_antiga.vcf
2. Árvore: PhyloTree 16.0
3. Métrica: Hamming
4. Processar e comparar com resultados anteriores
```

## Resolução de Problemas

### Erro: "Arquivo não encontrado"
- Verifique o caminho do Haplogrep3 nas configurações
- Confirme que o arquivo `haplogrep3.exe` existe no caminho especificado

### Erro: "Tree not found"
- A árvore selecionada pode não estar disponível
- Tente usar a árvore padrão (PhyloTree 17 - FU 1.2)

### Erro no formato do VCF
- Confirme que o arquivo está em formato VCF válido
- Verifique se contém variantes mitocondriais
- Certifique-se de que o arquivo não está corrompido

### Aplicação não abre
- Verifique se o Streamlit foi instalado: `pip install streamlit`
- Tente executar: `streamlit run app_streamlit.py --server.port 8502`

## Recursos da Interface

### 🎨 Interface Responsiva
- Layout adaptável a diferentes tamanhos de tela
- Barra lateral com todas as configurações
- Área principal dividida em colunas

### 🚀 Processamento em Tempo Real
- Feedback visual durante o processamento
- Spinner com mensagem de status
- Notificações de sucesso ou erro

### 📊 Visualização Clara
- Resultados organizados em abas
- Métricas destacadas
- Download fácil dos resultados

### 🔧 Configuração Flexível
- Todas as opções do Haplogrep3 disponíveis
- Configurações persistem durante a sessão
- Valores padrão otimizados

## Dicas

1. **Use Relatório Estendido** para análises detalhadas
2. **Aumente o número de hits** quando há incerteza na classificação
3. **Ajuste o nível de heteroplasmia** conforme a qualidade dos dados
4. **Baixe sempre os resultados** para referência futura
5. **Compare diferentes métricas** em casos complexos

## Integração com Workflow

A aplicação pode ser integrada em um workflow maior:

```
VCF → Streamlit App → Classificação → Download → Análise Posterior
```

Os resultados baixados podem ser:
- Importados em planilhas (Excel, Google Sheets)
- Processados por scripts Python
- Incluídos em relatórios
- Arquivados para documentação

## Segurança e Privacidade

- Arquivos processados são temporários
- Dados não são armazenados permanentemente
- Limpeza automática após processamento
- Execução local (sem envio para servidores externos)

## Suporte

Para problemas ou dúvidas:
- Consulte a [documentação do Haplogrep3](https://haplogrep.readthedocs.io/)
- Verifique o [guia do wrapper](docs/HAPLOGREP_WRAPPER_GUIDE.md)
- Revise os logs de erro exibidos na interface

## Próximos Passos

Após usar a aplicação, você pode:
1. Processar múltiplos arquivos usando o script batch
2. Automatizar análises com o wrapper Python
3. Integrar em pipelines de bioinformática
4. Criar relatórios personalizados
