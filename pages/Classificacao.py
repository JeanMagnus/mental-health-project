import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

@st.cache_resource
def treinar_modelo():
    print("Iniciando o treinamento do modelo (isso só acontecerá uma vez)...")
    data = {
        'Age': [37, 44, 32, 31, 33, 35, 39, 42, 23, 29] * 80,
        'family_history': ['No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'No'] * 80,
        'work_interfere': ['Often', 'Rarely', 'Rarely', 'Often', 'Sometimes', 'Sometimes', 'Never', 'Sometimes', 'Never', 'Never'] * 80,
        'benefits': ['Yes', 'No', 'No', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'Yes'] * 80,
        'Gender_clean': ['Female', 'Male', 'Male', 'Male', 'Male', 'Female', 'Female', 'Female', 'Male', 'Female'] * 80,
        'treatment': ['Yes', 'No', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes', 'No'] * 80,
    }
    df = pd.DataFrame(data)

    features = ['Age', 'family_history', 'work_interfere', 'benefits', 'Gender_clean']
    target = 'treatment'
    df_ml = df.dropna(subset=features + [target]).copy()
    df_ml[target] = df_ml[target].map({'Yes': 1, 'No': 0})
    X = df_ml[features]
    y = df_ml[target]

    # Garante consistência nas colunas de dummies
    categorias_dummies = pd.get_dummies(pd.DataFrame({
        'family_history': ['No', 'Yes'],
        'work_interfere': ['Never', 'Sometimes', 'Often', 'Rarely'],
        'benefits': ['No', "Don't know", 'Yes'],
        'Gender_clean': ['Female', 'Male', 'Other'],
        'Age': [0]  # numérico, não gera dummy
    }), drop_first=True).columns

    X_encoded = pd.get_dummies(X, drop_first=True)
    X_encoded = X_encoded.reindex(columns=categorias_dummies, fill_value=0).astype(float)

    # Ajuste dinâmico do k_neighbors
    minority_class_count = min(y.value_counts())
    k_neighbors = max(1, min(5, minority_class_count - 1))
    print(f"SMOTE com k_neighbors={k_neighbors} (menor classe tem {minority_class_count} amostras)")

    smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_encoded, y)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_resampled, y_train_resampled)
    print("Modelo treinado e colocado em cache!")
    return model, categorias_dummies

modelo, colunas_modelo = treinar_modelo()

st.set_page_config(page_title="Previsão de Saúde Mental", page_icon="🧠", layout="centered")
st.title("🧠 Formulário de Previsão de Saúde Mental")
st.markdown("Preencha os dados abaixo para que o modelo de Machine Learning faça uma previsão.")

with st.form("prediction_form"):
    st.header("Informações do Usuário")
    age_input = st.slider("Idade", min_value=18, max_value=100, value=30, step=1)
    family_history_input = st.radio("Você tem histórico familiar de doença mental?", ("No", "Yes"), index=0)
    work_interfere_input = st.selectbox("Você sente que sua condição de saúde mental interfere no seu trabalho?", ("Never", "Sometimes", "Often", "Rarely"))
    benefits_input = st.select_slider("Sua empresa oferece benefícios de saúde mental?", options=["No", "Don't know", "Yes"])
    gender_input = st.radio("Gênero", ("Female", "Male", "Other"), index=0)
    submit_button = st.form_submit_button("Fazer Previsão")

if submit_button:
    dados_usuario = {
        'Age': [age_input],
        'family_history': [family_history_input],
        'work_interfere': [work_interfere_input],
        'benefits': [benefits_input],
        'Gender_clean': [gender_input]
    }
    usuario_df = pd.DataFrame(dados_usuario)
    usuario_encoded = pd.get_dummies(usuario_df, drop_first=True)
    usuario_encoded = usuario_encoded.reindex(columns=colunas_modelo, fill_value=0).astype(float)
    probabilidade = modelo.predict_proba(usuario_encoded)
    prob_sim = probabilidade[0][1]

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
