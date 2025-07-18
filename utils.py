import pandas as pd
import streamlit as st

def simplificar_genero(genero):
    genero = str(genero).strip().lower()

    if "trans" in genero:
        return "Trans"

    elif genero in ['m','male', 'cis male', 'cis man', 'man', 'male (cis)',
                    'male-ish', 'maile', 'mal', 'msle', 'malr', 'mail', 'make',
                    'guy (-ish) ^_^', 'ostensibly male, unsure what that really means',
                    'something kinda male?', 'male leaning androgynous']:
        return "Homem"

    elif genero in ['f','female', 'cis female', 'cis-female/femme', 'femail',
                    'femake', 'female (cis)']:
        return "Mulher"

    elif genero in ['non-binary', 'enby', 'fluid', 'androgyne', 'neuter',
                    'queer', 'nah', 'all', 'p', 'a little about you',
                    'queer/she/they']:
        return "Não-binário"

    else:
        return "Não-binário"

@st.cache_data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/JeanMagnus/ciencia-dados/main/survey.csv')

    # Normalização de colunas
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Padronização básica de gênero
    df['gender'] = df['gender'].str.lower().str.strip()
    df['gender'] = df['gender'].replace({
        'male': 'male', 'm': 'male', 'man': 'male',
        'female': 'female', 'f': 'female', 'woman': 'female',
        'non-binary': 'non-binary', 'nb': 'non-binary',
        'trans-female': 'trans', 'trans woman': 'trans',
        'trans male': 'trans', 'trans man': 'trans',
        'agender': 'non-binary', 'genderqueer': 'non-binary'
    })
    df['gender'] = df['gender'].fillna('not specified')

    # Agrupamento final com função robusta
    df['gender_group'] = df['gender'].apply(simplificar_genero)

    # Grupo unindo Trans e Não-binário
    df['grupo'] = df['gender_group'].replace({
        'Trans': 'Trans/NB',
        'Não-binário': 'Trans/NB'
    })

    return df
    

# FUNÇÃO CENTRALIZADA PARA TODOS OS ESTILOS VISUAIS (VERSÃO ATUALIZADA)
def aplicar_estilos():
    st.markdown(
        """
        <style>
        
        /* --- TIPOGRAFIA GERAL --- */

        /* Define um tamanho de fonte base maior para o app todo. 
           O padrão do navegador é 16px. Experimente 17px ou 18px.
        */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            font-size: 19px;
        }

        /* --- BARRA LATERAL (SIDEBAR) --- */
        
        /* Opcional: Deixar a fonte da sidebar um pouco maior que o conteúdo principal */
        [data-testid="stSidebar"] * {
            font-size: 1.1rem; /* 1.1rem = 110% do tamanho da fonte base (17px) */
        }

        /* Espaçamento entre o ícone e o texto no menu */
        [data-testid="stSidebarNavLink"] span:first-child {
            margin-right: 10px; 
        }

        </style>
        """,
        unsafe_allow_html=True,
    )