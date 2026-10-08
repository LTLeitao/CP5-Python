import os
import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Dashboard de Livros", layout="wide", page_icon="📚")

def carregar_css():
    caminho_css = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(caminho_css):
        with open(caminho_css, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

carregar_css()

st.markdown(
    """
    <div class="dashboard-header">
        <h1 class="display-5 fw-bold">📚 Painel de Análise de Coleta de Dados</h1>
        <p class="lead mb-0">Visualização de métricas e catálogo extraído via Web Crawler</p>
    </div>
    """,
    unsafe_allow_html=True
)

try:
    res_stats = requests.get(f"{API_URL}/stats").json()
    res_items = requests.get(f"{API_URL}/items?limit=500").json()
    
    df = pd.DataFrame(res_items)

    st.subheader("📊 Indicadores Chave do Sistema")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Livros", res_stats.get("total_registros", 0))
    col2.metric("Preço Médio", f"£ {res_stats.get('preco_medio', 0):.2f}")
    col3.metric("Preço Máximo", f"£ {res_stats.get('preco_maximo', 0):.2f}")
    col4.metric("Preço Mínimo", f"£ {res_stats.get('preco_minimo', 0):.2f}")

    if not df.empty:
        st.markdown("---")
        st.subheader("🔎 Filtro e Pesquisa")
        
        termo_busca = st.text_input(
            label="Buscar livro por título:",
            placeholder="Digite o nome do livro...",
            key="busca_titulo_input"
        )
        
        df_filtrado = df.copy()
        if termo_busca:
            df_filtrado = df_filtrado[df_filtrado["titulo"].str.contains(termo_busca, case=False, na=False)]

        st.markdown("---")
        st.subheader("📈 Análise Gráfica")
        
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            st.write("**Distribuição por Avaliação (Estrelas)**")
            avaliacoes_count = df_filtrado["avaliacao"].value_counts().sort_index()
            st.bar_chart(avaliacoes_count, color="#2563eb")

        with col_g2:
            st.write("**Valores dos Livros Coletados**")
            st.line_chart(df_filtrado.set_index("titulo")["preco"], color="#10b981")

        st.markdown("---")
        st.subheader("📋 Tabela de Registros Coletados")
        
        df_exibicao = df_filtrado.drop(columns=["url_origem"], errors="ignore")
        st.dataframe(df_exibicao, use_container_width=True)

except requests.exceptions.ConnectionError:
    st.error("❌ Não foi possível conectar à API. Certifique-se de que a FastAPI está rodando em http://127.0.0.1:8000")