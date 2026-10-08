import os
import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Dashboard de Livros", layout="wide")

def carregar_css():
    caminho_css = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(caminho_css):
        with open(caminho_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_css()

st.markdown(
    """
    <div class="dashboard-header">
        <h1 class="display-5 fw-bold"><i class="bi bi-journal-bookmark-fill me-2"></i> Painel de Análise de Coleta de Dados</h1>
        <p class="lead mb-0">Visualização de métricas e catálogo extraído via Web Crawler</p>
    </div>
    """,
    unsafe_allow_html=True
)

try:
    res_stats = requests.get(f"{API_URL}/stats").json()
    res_items = requests.get(f"{API_URL}/items?limit=500").json()
    
    df = pd.DataFrame(res_items)

    st.markdown("<h3><i class='bi bi-speedometer2 me-2'></i> Indicadores Chave do Sistema</h3>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Livros", res_stats.get("total_registros", 0))
    col2.metric("Preço Médio", f"£ {res_stats.get('preco_medio', 0):.2f}")
    col3.metric("Preço Máximo", f"£ {res_stats.get('preco_maximo', 0):.2f}")
    col4.metric("Preço Mínimo", f"£ {res_stats.get('preco_minimo', 0):.2f}")

    if not df.empty:
        st.markdown("---")
        st.markdown("<h3><i class='bi bi-search me-2'></i> Filtro e Pesquisa</h3>", unsafe_allow_html=True)
        
        termo_busca = st.text_input(
            label="Buscar livro por título:",
            placeholder="Digite o nome do livro...",
            key="input_busca_livro"
        )
        
        df_filtrado = df.copy()
        if termo_busca:
            df_filtrado = df_filtrado[df_filtrado["titulo"].str.contains(termo_busca, case=False, na=False)]

        st.markdown("---")
        st.markdown("<h3><i class='bi bi-graph-up-arrow me-2'></i> Análise Gráfica</h3>", unsafe_allow_html=True)
        
        if not df_filtrado.empty:
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                st.write("**Distribuição por Avaliação (Estrelas)**")
                avaliacoes_count = df_filtrado["avaliacao"].value_counts().sort_index()
                st.bar_chart(avaliacoes_count, color="#3b82f6")

            with col_g2:
                st.write("**Top 10 Livros Mais Caros (£)**")
                top_caros = df_filtrado.nlargest(10, "preco")[["titulo", "preco"]].set_index("titulo")
                st.bar_chart(top_caros, color="#10b981")

            st.markdown("---")
            st.markdown("<h3><i class='bi bi-table me-2'></i> Tabela de Registros Coletados</h3>", unsafe_allow_html=True)
            
            df_exibicao = df_filtrado.drop(columns=["url_origem"], errors="ignore")
            st.dataframe(df_exibicao, use_container_width=True)
        else:
            st.markdown("<div class='alert alert-warning d-flex align-items-center' role='alert'><i class='bi bi-exclamation-triangle-fill me-2'></i> Nenhum livro encontrado para o termo pesquisado.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert alert-info d-flex align-items-center' role='alert'><i class='bi bi-info-circle-fill me-2'></i> Nenhum registro encontrado no banco de dados. Execute o crawler para popular a base.</div>", unsafe_allow_html=True)

except requests.exceptions.ConnectionError:
    st.markdown("<div class='alert alert-danger d-flex align-items-center' role='alert'><i class='bi bi-x-circle-fill me-2'></i> Não foi possível conectar à API. Certifique-se de que a FastAPI está rodando em http://127.0.0.1:8000</div>", unsafe_allow_html=True)