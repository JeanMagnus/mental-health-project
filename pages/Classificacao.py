# Conteúdo COMPLETO para o arquivo pages/Classificacao.py

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE


# --- LÓGICA EM SEGUNDO PLANO ---
# Função para treinar o modelo e deixá-lo pronto para uso.
# O cache garante que isso rode apenas uma vez por sessão.
@st.cache_resource
def get_trained_model(df):
    """
    Prepara os dados, treina o modelo com SMOTE e o retorna pronto para previsões.
    """
    st.write("Cache miss: Carregando e treinando o modelo pela primeira vez...")

    # 1. Preparação dos dados
    features = ['Age', 'family_history', 'work_interfere', 'benefits', 'Gender_clean']
    target = 'treatment'
    df_ml = df.dropna(subset=features + [target]).copy()
    df_ml[target] = df_ml[target].map({'Yes': 1, 'No': 0})
    X = df_ml[features]
    y = df_ml[target]
    X_encoded = pd.get_dummies(X, drop_first=True)

    # 2. Divisão e Balanceamento (fluxo correto)
    X_train, _, y_train, _ = train_test_split(
        X_encoded, y, test_size=0.2, stratify=y, random_state=42
    )
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # 3. Treinamento do Modelo
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_resampled, y_train_resampled)
    
    # Retorna o modelo treinado e as colunas necessárias para o formulário
    return model, X_encoded.columns

# --- INTERFACE DO FORMULÁRIO ---
st.title("🧠 Formulário de Previsão")
st.markdown("Preencha os dados abaixo para que o modelo de Machine Learning faça uma previsão em tempo real.")

# Verifica se os dados principais foram carregados na Home
if 'df' in st.session_state:
    df_principal = st.session_state['df']
    
    # Carrega o modelo treinado (do cache)
    with st.spinner('Carregando o modelo preditivo...'):
        modelo, colunas_modelo = get_trained_model(df_principal)
    
    # Cria o formulário
    with st.form("prediction_form"):
        st.header("Por favor, forneça suas informações")
        
        # Inputs do usuário
        age_input = st.slider("Idade", min_value=18, max_value=100, value=30, step=1)
        family_history_input = st.radio("Você tem histórico familiar de doença mental?", ("No", "Yes"), index=0, horizontal=True)
        work_interfere_input = st.selectbox("Você sente que sua condição de saúde mental interfere no seu trabalho?", ("Never", "Sometimes", "Often", "Rarely"))
        benefits_input = st.radio("Sua empresa oferece benefícios de saúde mental?", ("No", "Don't know", "Yes"), index=1, horizontal=True)
        gender_input = st.radio("Gênero", ("Female", "Male", "Other"), index=0, horizontal=True)

        # Botão de envio
        submit_button = st.form_submit_button("Fazer Previsão")

    # Lógica a ser executada APÓS o envio do formulário
    if submit_button:
        # 1. Coleta e formata os dados do formulário
        dados_usuario = {
            'Age': [age_input],
            'family_history': [family_history_input],
            'work_interfere': [work_interfere_input],
            'benefits': [benefits_input],
            'Gender_clean': [gender_input]
        }
        usuario_df = pd.DataFrame(dados_usuario)

        # 2. Aplica o pré-processamento
        usuario_encoded = pd.get_dummies(usuario_df, drop_first=True)
        usuario_final = usuario_encoded.reindex(columns=colunas_modelo, fill_value=0)

        # 3. Faz a previsão de probabilidade
        probabilidade = modelo.predict_proba(usuario_final)
        prob_sim = probabilidade[0][1]

        # 4. Exibe o resultado
        st.header("Resultado da Análise")
        if prob_sim > 0.6:
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
                icon="💡"
            )
        
        st.warning(
            "**Observação:** Este é um resultado gerado por um modelo estatístico e não substitui "
            "uma avaliação profissional de saúde.",
            icon="⚠️"
        )
else:
    st.error("Os dados não foram carregados. Por favor, vá para a página principal primeiro para carregar o arquivo.")