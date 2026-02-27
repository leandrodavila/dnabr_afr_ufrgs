"""
Aplicação Streamlit para Classificação de Haplogrupos Mitocondriais

Esta aplicação permite fazer upload de arquivos VCF e classificar haplogrupos
usando o Haplogrep3.
"""

import streamlit as st
import sys
from pathlib import Path
import tempfile
import os

# Add parent directory to Python path
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from haplogrep_wrapper import Haplogrep3Wrapper, ClassificationMetric


# Configuração da página
st.set_page_config(
    page_title="Classificador de Haplogrupos Mitocondriais",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título e descrição
st.title("🧬 Classificador de Haplogrupos Mitocondriais")
st.markdown("""
Esta aplicação permite classificar haplogrupos mitocondriais a partir de arquivos VCF
usando a ferramenta Haplogrep3 com árvores filogenéticas atualizadas.
""")

st.divider()

# Detectar ambiente (Docker/Cloud vs Local Windows)
if os.path.exists("/app/haplogrep/haplogrep3.jar"):
    # Ambiente Docker/Cloud (Render.com)
    DEFAULT_HAPLOGREP_PATH = "/app/haplogrep/haplogrep3.jar"
    USE_JAR = True
else:
    # Ambiente local Windows
    DEFAULT_HAPLOGREP_PATH = "C:/repos/dnabr_afr/haplogrep/haplogrep3.exe"
    USE_JAR = False

# Sidebar com configurações
with st.sidebar:
    st.header("⚙️ Configurações")

    # Mostrar ambiente detectado
    if USE_JAR:
        st.info("🐳 Ambiente: Docker/Cloud (Render.com)")
        # No ambiente cloud, mostrar o path mas desabilitar edição
        st.text_input(
            "Caminho do Haplogrep3",
            value=DEFAULT_HAPLOGREP_PATH,
            disabled=True,
            help="Path configurado automaticamente no ambiente Docker"
        )
        haplogrep_path = DEFAULT_HAPLOGREP_PATH
    else:
        st.info("💻 Ambiente: Local Windows")
        # No ambiente local, permitir edição do caminho
        haplogrep_path = st.text_input(
            "Caminho do Haplogrep3",
            value=DEFAULT_HAPLOGREP_PATH,
            help="Caminho completo para o executável do Haplogrep3"
        )

    # Seleção da árvore filogenética
    st.subheader("Árvore Filogenética")
    tree_options = {
        "phylotree-fu-rcrs@1.2": "PhyloTree 17 - Forensic Update 1.2 (Recomendado)",
        "phylotree-fu-rcrs@1.0": "PhyloTree 17 - Forensic Update 1.0",
        "phylotree-rcrs@17.2": "PhyloTree 17.2",
        "phylotree-rcrs@17.0": "PhyloTree 17.0",
        "phylotree-rsrs@17.0": "PhyloTree 17.0 (RSRS)",
        "phylotree-rcrs@16.0": "PhyloTree 16.0",
        "phylotree-rcrs@15.0": "PhyloTree 15.0"
    }

    selected_tree = st.selectbox(
        "Selecione a árvore",
        options=list(tree_options.keys()),
        format_func=lambda x: tree_options[x],
        help="Árvore filogenética usada para classificação"
    )

    # Seleção da métrica
    st.subheader("Métrica de Classificação")
    metric_options = {
        "KULCZYNSKI": "Kulczynski (Padrão)",
        "HAMMING": "Hamming Distance",
        "JACCARD": "Jaccard Index",
        "KIMURA": "Kimura Distance"
    }

    selected_metric = st.selectbox(
        "Selecione a métrica",
        options=list(metric_options.keys()),
        format_func=lambda x: metric_options[x],
        help="Método usado para calcular a similaridade"
    )

    # Opções avançadas
    with st.expander("🔧 Opções Avançadas"):
        extend_report = st.checkbox(
            "Relatório Estendido",
            value=True,
            help="Inclui informações adicionais sobre SNPs"
        )

        num_hits = st.slider(
            "Número de melhores resultados",
            min_value=1,
            max_value=10,
            value=3,
            help="Quantidade de haplogrupos candidatos a exibir"
        )

        het_level = st.slider(
            "Nível de Heteroplasmia",
            min_value=0.0,
            max_value=1.0,
            value=0.9,
            step=0.1,
            help="Limiar para incluir heteroplasmias no perfil"
        )

        keep_files = st.checkbox(
            "Manter arquivos após processamento",
            value=False,
            help="Se marcado, os arquivos VCF e resultados serão salvos permanentemente"
        )

# Área principal
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📁 Upload do Arquivo VCF")
    uploaded_file = st.file_uploader(
        "Selecione um arquivo VCF",
        type=["vcf"],
        help="Faça upload do arquivo VCF contendo variantes mitocondriais"
    )

    if uploaded_file:
        st.success(f"✅ Arquivo carregado: {uploaded_file.name}")

        # Mostrar informações do arquivo
        file_size = uploaded_file.size / 1024  # KB
        st.info(f"📊 Tamanho: {file_size:.2f} KB")

        # Botão para processar
        process_button = st.button(
            "🚀 Classificar Haplogrupo",
            type="primary",
            use_container_width=True
        )
    else:
        st.info("👆 Faça upload de um arquivo VCF para começar")
        process_button = False

with col2:
    st.subheader("📊 Resultados")
    results_placeholder = st.empty()

# Processamento
if uploaded_file and process_button:
    with st.spinner("🔬 Analisando arquivo VCF... Por favor, aguarde."):
        try:
            # Criar diretório de uploads se não existir
            upload_dir = Path("C:/repos/dnabr_afr/uploads")
            upload_dir.mkdir(parents=True, exist_ok=True)

            # Criar diretório de resultados se não existir
            results_dir = Path("C:/repos/dnabr_afr/results")
            results_dir.mkdir(parents=True, exist_ok=True)

            # Determinar se deve usar diretório temporário ou permanente
            if keep_files:
                # Salvar em diretório permanente
                input_path = upload_dir / uploaded_file.name
                with open(input_path, 'wb') as f:
                    f.write(uploaded_file.getvalue())

                # Nome do arquivo de saída baseado no arquivo de entrada
                output_filename = f"{input_path.stem}_haplogroups.txt"
                output_path = results_dir / output_filename
            else:
                # Usar arquivos temporários
                with tempfile.NamedTemporaryFile(delete=False, suffix=".vcf", mode='wb') as tmp_input:
                    tmp_input.write(uploaded_file.getvalue())
                    input_path = Path(tmp_input.name)

                with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode='w') as tmp_output:
                    output_path = Path(tmp_output.name)

            # Inicializar o wrapper
            wrapper = Haplogrep3Wrapper(
                haplogrep_path=haplogrep_path,
                default_tree=selected_tree,
                use_jar=USE_JAR
            )

            # Converter métrica para enum
            metric_map = {
                "KULCZYNSKI": ClassificationMetric.KULCZYNSKI,
                "HAMMING": ClassificationMetric.HAMMING,
                "JACCARD": ClassificationMetric.JACCARD,
                "KIMURA": ClassificationMetric.KIMURA
            }

            # Executar classificação
            result = wrapper.classify(
                input_file=input_path,
                output_file=output_path,
                metric=metric_map[selected_metric],
                extend_report=extend_report,
                hits=num_hits,
                het_level=het_level
            )

            # Exibir resultados
            if result.success:
                st.success("✅ Classificação concluída com sucesso!")

                # Mostrar informação sobre arquivos salvos
                if keep_files:
                    st.info(f"📁 **Arquivos salvos permanentemente:**\n"
                           f"- VCF: `{input_path}`\n"
                           f"- Resultados: `{output_path}`")

                # Ler resultados
                content = wrapper.read_results(result.output_file)

                # Exibir em abas
                tab1, tab2, tab3 = st.tabs(["📋 Resultados Principais", "📄 Resultado Completo", "ℹ️ Informações Técnicas"])

                with tab1:
                    st.subheader("Haplogrupo Classificado")

                    # Processar e exibir de forma estruturada
                    lines = content.strip().split('\n')

                    if len(lines) > 1:
                        # Assumir que primeira linha é cabeçalho
                        headers = lines[0].split('\t')

                        # Exibir cada resultado
                        for i, line in enumerate(lines[1:], 1):
                            if line.strip():
                                st.markdown(f"### 🧬 Resultado {i}")

                                values = line.split('\t')

                                # Criar colunas para exibir dados importantes
                                col_a, col_b, col_c = st.columns(3)

                                # Tentar extrair informações principais
                                # (ajustar de acordo com formato real do Haplogrep3)
                                for j, (header, value) in enumerate(zip(headers, values)):
                                    if j < 3:
                                        with [col_a, col_b, col_c][j]:
                                            st.metric(header, value)
                                    else:
                                        st.text(f"{header}: {value}")

                                st.divider()
                    else:
                        st.info("Nenhum resultado de classificação encontrado no arquivo.")

                with tab2:
                    st.subheader("Resultado Completo")
                    st.text_area(
                        "Saída do Haplogrep3",
                        value=content,
                        height=400,
                        disabled=True
                    )

                    # Botão de download
                    st.download_button(
                        label="⬇️ Baixar Resultados",
                        data=content,
                        file_name=f"{uploaded_file.name}_haplogroups.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                with tab3:
                    st.subheader("Informações Técnicas")

                    info_col1, info_col2 = st.columns(2)

                    with info_col1:
                        st.markdown("**Configurações Utilizadas:**")
                        st.write(f"- 🌳 Árvore: `{selected_tree}`")
                        st.write(f"- 📐 Métrica: `{selected_metric}`")
                        st.write(f"- 📊 Relatório Estendido: `{extend_report}`")

                    with info_col2:
                        st.markdown("**Parâmetros Avançados:**")
                        st.write(f"- 🎯 Número de hits: `{num_hits}`")
                        st.write(f"- 🧬 Nível de heteroplasmia: `{het_level}`")
                        st.write(f"- 📝 Código de retorno: `{result.return_code}`")
                        st.write(f"- 💾 Arquivos mantidos: `{keep_files}`")

                    if keep_files:
                        st.markdown("**Localização dos Arquivos:**")
                        st.code(f"VCF: {input_path}\nResultados: {output_path}", language="text")

                    if result.stdout:
                        with st.expander("Ver saída padrão (stdout)"):
                            st.code(result.stdout, language="text")

            else:
                st.error("❌ Erro na classificação!")
                st.error(f"**Mensagem de erro:** {result.stderr}")

                if result.stdout:
                    with st.expander("Ver detalhes do erro"):
                        st.code(result.stdout, language="text")

                st.info("💡 **Dicas para resolução:**\n"
                       "- Verifique se o caminho do Haplogrep3 está correto\n"
                       "- Confirme que o arquivo VCF está no formato correto\n"
                       "- Tente selecionar uma árvore filogenética diferente")

            # Limpar arquivos temporários (somente se keep_files = False)
            if not keep_files:
                try:
                    os.unlink(input_path)
                    os.unlink(output_path)
                except:
                    pass

        except FileNotFoundError as e:
            st.error(f"❌ Erro: Arquivo não encontrado - {str(e)}")
            st.info("Verifique se o caminho do Haplogrep3 está correto nas configurações.")

        except Exception as e:
            st.error(f"❌ Erro inesperado: {str(e)}")
            st.exception(e)

# Rodapé
st.divider()
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Desenvolvido com Streamlit e Haplogrep3</p>
    <p>📚 <a href='https://haplogrep.readthedocs.io/' target='_blank'>Documentação do Haplogrep3</a></p>
</div>
""", unsafe_allow_html=True)
