import streamlit as st
from utils import load_data, aplicar_estilos

# Carregar estilos e dados
aplicar_estilos()
if 'df' not in st.session_state:
    df = load_data()
    st.session_state['df'] = df
else:
    df = st.session_state['df']


def pagina_inicial():
    """
    Esta função contém todo o conteúdo da página inicial com o novo design e os textos originais.
    """

    # --- 1. SEÇÃO DE DESTAQUE (HERO SECTION) ---
    col_img, col_title = st.columns([1, 3], gap="large")
    with col_img:
        st.image("https://emojicdn.elk.sh/🧠?style=twitter", width=150)
    with col_title:
        st.title("Saúde Mental no Setor de Tecnologia")
    
    st.divider()

    # --- 2. MÉTRICAS PRINCIPAIS (KPIs) ---
    total_participantes = df.shape[0]
    paises_cobertos = df['country'].nunique()
    media_idade = int(df['age'].median())

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Total de Participantes", f"{total_participantes}")
    col_kpi2.metric("Países Cobertos", f"{paises_cobertos}")
    col_kpi3.metric("Idade Média", f"{media_idade} anos")

    st.divider()
    
    # --- 3. TEXTO INTRODUTÓRIO (TEXTO ORIGINAL RESTAURADO) ---
    st.markdown("""
    Neste projeto, será utilizado o dataset <b>"Mental Health in Tech Survey"</b>, disponível no Kaggle,
    que reúne respostas de profissionais da área de tecnologia sobre saúde mental no ambiente de trabalho.
    A pesquisa foi organizada pela <b>OSMI (Open Sourcing Mental Illness)</b>, organização que promove
    conscientização sobre saúde mental, especialmente em ambientes técnicos.
    
    <br>
    
    A análise desse tipo de dado é extremamente relevante, pois a saúde mental vem se tornando um tema central
    nas discussões sobre qualidade de vida no trabalho. Identificar padrões, barreiras ao tratamento e relações
    com condições laborais pode ajudar empresas e profissionais a tomarem decisões mais conscientes e humanizadas.
    """, unsafe_allow_html=True)

    # --- 4. CARDS DE NAVEGAÇÃO (COM TEXTOS ORIGINAIS RESTAURADOS) ---
    st.subheader("Explore as páginas ao lado para navegar entre:")

    col_card1, col_card2, col_card3 = st.columns(3, gap="large")

    with col_card1:
        with st.container(border=True, height=130):
            st.markdown("##### 📊 Estatísticas e visualizações gerais")
            st.caption("Leve-me para a página de Análise Geral.")

        with st.container(border=True, height=130):
            st.markdown("##### 👤 IA de Apoio (Classificação)")
            st.caption("Use nosso modelo para uma recomendação personalizada.")

    with col_card2:
        with st.container(border=True, height=130):
            st.markdown("##### 📈 Comparações por gênero, país, idade e trabalho remoto")
            st.caption("Leve-me para a página de Comparações.")
        
        with st.container(border=True, height=130):
            st.markdown("##### 🧠 Perfis (Clustering)")
            st.caption("Descubra as 'personas' de profissionais nos dados.")

    with col_card3:
        with st.container(border=True, height=130):
            st.markdown("##### 🔗 Correlações entre fatores de apoio e tratamento")
            st.caption("Leve-me para a página de Correlações.")
        

# Lógica de navegação principal
pages = [
    st.Page(pagina_inicial, title="Página Inicial", icon="🏠", default=True),
    st.Page("pages/Analise_Geral.py", title="Análise Geral", icon="📊"),
    st.Page("pages/Comparacoes.py", title="Comparações", icon="📈"),
    st.Page("pages/Correlacoes.py", title="Correlações", icon="🔗"),
    st.Page("pages/Classificacao.py", title="Classificação", icon="👤"),
    st.Page("pages/Clustering.py", title="Perfis", icon="👥"),
]

# Mensagem de boas-vindas na sidebar (TEXTO ORIGINAL RESTAURADO)
with st.sidebar:
    st.write("Bem vindo ao projeto de análise de dados sobre saúde mental no setor de tecnologia!")
    st.write("Selecione uma página no menu para começar a explorar os dados.")

# Executa a navegação
pg = st.navigation(pages)
pg.run()