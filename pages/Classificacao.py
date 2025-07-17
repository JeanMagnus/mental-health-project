import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import warnings

# Ignorar avisos futuros para uma saída mais limpa
warnings.filterwarnings("ignore", category=FutureWarning)

# =============================================================================
# PARTE 1: TREINAMENTO DO MODELO (COM CACHE)
# =============================================================================
# Usamos @st.cache_resource para garantir que o modelo seja treinado apenas uma vez,
# e não a cada interação do usuário. Isso é essencial para o desempenho.
@st.cache_resource
def treinar_modelo():
    """
    Função para carregar dados, pré-processar e treinar o modelo.
    O resultado (modelo treinado e colunas) fica em cache.
    """
    print("Iniciando o treinamento do modelo (isso só acontecerá uma vez)...")
    # Criando dados fictícios que se assemelham ao seu problema
    data = {
        'Age': [37, 44, 32, 31, 33, 35, 39, 42, 23, 29] * 80,
        'family_history': ['No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'No'] * 80,
        'work_interfere': ['Often', 'Rarely', 'Rarely', 'Often', 'Sometimes', 'Sometimes', 'Never', 'Sometimes', 'Never', 'Never'] * 80,
        'benefits': ['Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes'] * 80,
        'Gender_clean': ['Female', 'Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', 'Male', 'Female'] * 80,
        'treatment': ['Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'] * 80,
    }
    df = pd.DataFrame(data)

    # Pré-processamento e treinamento
    features = ['Age', 'family_history', 'work_interfere', 'benefits', 'Gender_clean']
    target = 'treatment'
    df_ml = df.dropna(subset=features + [target]).copy()
    df_ml[target] = df_ml[target].map({'Yes': 1, 'No': 0})
    X = df_ml[features]
    y = df_ml[target]
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_encoded, y)
    
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_resampled, y_train_resampled)
    print("Modelo treinado e colocado em cache!")
    
    # Retornamos o modelo e as colunas necessárias para a previsão
    return model, X_encoded.columns

# Carrega o modelo (ou busca do cache se já foi carregado)
modelo, colunas_modelo = treinar_modelo()


# =============================================================================
# PARTE 2: INTERFACE WEB COM STREAMLIT
# =============================================================================
st.set_page_config(page_title="Previsão de Saúde Mental", page_icon="🧠", layout="centered")
st.title("🧠 Formulário de Previsão de Saúde Mental")
st.markdown("Preencha os dados abaixo para que o modelo de Machine Learning faça uma previsão.")

# Usamos um formulário para agrupar os inputs e ter um único botão de envio
with st.form("prediction_form"):
    st.header("Informações do Usuário")
    
    # Inputs do usuário
    age_input = st.slider("Idade", min_value=18, max_value=100, value=30, step=1)
    family_history_input = st.radio("Você tem histórico familiar de doença mental?", ("No", "Yes"), index=0)
    work_interfere_input = st.selectbox("Você sente que sua condição de saúde mental interfere no seu trabalho?", ("Never", "Sometimes", "Often", "Rarely"))
    benefits_input = st.select_slider("Sua empresa oferece benefícios de saúde mental?", options=["No", "Don't know", "Yes"])
    gender_input = st.radio("Gênero", ("Female", "Male", "Other"), index=0)

    # Botão de envio do formulário
    submit_button = st.form_submit_button("Fazer Previsão")

# Lógica a ser executada APÓS o envio do formulário
if submit_button:
    # Cria um DataFrame com os dados do formulário
    dados_usuario = {
        'Age': [age_input],
        'family_history': [family_history_input],
        'work_interfere': [work_interfere_input],
        'benefits': [benefits_input],
        'Gender_clean': [gender_input]
    }
    usuario_df = pd.DataFrame(dados_usuario)

    # Aplica o pré-processamento
    usuario_encoded = pd.get_dummies(usuario_df, drop_first=True)
    usuario_final = usuario_encoded.reindex(columns=colunas_modelo, fill_value=0)

    # Faz a previsão de probabilidade
    probabilidade = modelo.predict_proba(usuario_final)
    prob_sim = probabilidade[0][1]

    # Exibe o resultado
    st.header("Resultado da Análise")
    if prob_sim > 0.5:
        st.success(
            f"O modelo prevê uma probabilidade de **{prob_sim:.0%}** de que uma pessoa com este perfil "
            f"busque tratamento para saúde mental.",
            icon="✅"
        )
        st.balloons()
    else:
        st.info(
            f"O modelo prevê uma probabilidade de **{prob_sim:.0%}** de que uma pessoa com este perfil "
            f"busque tratamento para saúde mental.",
            icon="❌"
        )
    
    st.warning(
        "**Observação:** Este é um resultado gerado por um modelo estatístico e não substitui "
        "uma avaliação profissional de saúde.",
        icon="⚠️"
    )