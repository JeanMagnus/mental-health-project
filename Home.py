import streamlit as st
from pages import Analise_Geral, Comparacoes, Correlacoes

st.set_page_config(page_title="Projeto Saúde Mental", layout="wide")


st.markdown("""
<div style="text-align: center; padding: 2rem;">
    <h1 style="font-size: 3em;">🧠 Saúde Mental no Setor de Tecnologia</h1>
</div>
<div style="text-align: left; padding: 1rem;">
    <p style="font-size: 1.2em; max-width: 800px; margin: auto;">Neste projeto, será utilizado o dataset <b>"Mental Health in Tech Survey"</b>, disponível no Kaggle,
            que reúne respostas de profissionais da área de tecnologia sobre saúde mental no ambiente de trabalho.
            A pesquisa foi organizada pela <b>OSMI (Open Sourcing Mental Illness)</b>, organização que promove
            conscientização sobre saúde mental, especialmente em ambientes técnicos.

</div>
<div style="text-align: left; padding: 1rem;">
    <p style="font-size: 1.2em; max-width: 800px; margin: auto;">A análise desse tipo de dado é extremamente relevante, pois a saúde mental vem se tornando um tema central
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
