# Arquivo: Home.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

# Tente importar a função de estilos, se não existir, crie uma função vazia
try:
    from utils import aplicar_estilos
except ImportError:
    def aplicar_estilos():
        pass

# 1. Aplica os estilos de CSS (se houver)
aplicar_estilos()

if 'df' not in st.session_state:
    # Chama a função importada do seu arquivo utils.py
    df = load_data()
    # Salva o DataFrame no estado da sessão
    st.session_state['df'] = df
    print("Dados carregados e salvos na sessão pela primeira vez.")

# 2. DEFINA A FUNÇÃO DA PÁGINA INICIAL PRIMEIRO
def pagina_inicial():
    """
    Esta função contém todo o código e conteúdo que você quer mostrar na sua página inicial.
    """
    st.markdown("""
<div style="text-align: center; padding: 4rem;">
    <h1 style="font-size: 5em;">🧠 Saúde Mental no Setor de Tecnologia</h1>
</div>
<div style="text-align: left; padding: 1rem;">
    <p style="font-size: 1.5em; max-width: 800px; margin: auto;">Neste projeto, será utilizado o dataset <b>"Mental Health in Tech Survey"</b>, disponível no Kaggle,
            que reúne respostas de profissionais da área de tecnologia sobre saúde mental no ambiente de trabalho.
            A pesquisa foi organizada pela <b>OSMI (Open Sourcing Mental Illness)</b>, organização que promove
            conscientização sobre saúde mental, especialmente em ambientes técnicos.

</div>
<div style="text-align: left; padding: 1rem;">
    <p style="font-size: 1.5em; max-width: 800px; margin: auto;">A análise desse tipo de dado é extremamente relevante, pois a saúde mental vem se tornando um tema central
            nas discussões sobre qualidade de vida no trabalho. Identificar padrões, barreiras ao tratamento e relações
            com condições laborais pode ajudar empresas e profissionais a tomarem decisões mais conscientes e humanizadas.

</div>

<div style="text-align: left; padding: 1rem;">
<h3 style="margin-top: 2em; max-width: 800px; margin: auto;">Explore as páginas ao lado para navegar entre:</h3>
    <ul style="list-style: none; padding: 0; font-size: 1.1em; max-width: 800px; margin: auto;">
        <li>📊 <b>Estatísticas e visualizações gerais</b></li>
        <li>📈 <b>Comparações por gênero, país, idade e trabalho remoto</b></li>
        <li>📉 <b>Correlações entre fatores de apoio e tratamento</b></li>
    </ul>
</div>
""", unsafe_allow_html=True)

# 3. AGORA, CRIE A LISTA DE PÁGINAS USANDO A FUNÇÃO
pages = [
    st.Page(pagina_inicial, title="Página Inicial", icon=":material/home:", default=True),
    st.Page("pages/Analise_Geral.py", title="Análise Geral", icon=":material/analytics:"),
    st.Page("pages/Comparacoes.py", title="Comparações", icon=":material/compare_arrows:"),
    st.Page("pages/Correlacoes.py", title="Correlações", icon=":material/hub:"),
    st.Page("pages/Classificacao.py", title="Classificação", icon=":material/person:"),
    st.Page("pages/Clustering.py", title="Perfis", icon=":material/groups:"),
]

with st.sidebar.container(height=350):
    st.write("Bem vindo ao projeto de análise de dados sobre saúde mental no setor de tecnologia!")
    st.write(
            "Selecione uma página no menu para começar a explorar os dados."
    )

# 4. FINALMENTE, RODE A NAVEGAÇÃO
pg = st.navigation(pages)
pg.run()