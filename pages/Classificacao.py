
import streamlit as st
import pandas as pd
from utils import load_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Análise de Perfil de Saúde Mental")
st.markdown("""
Esta ferramenta usa **Inteligência Artificial** para analisar um perfil e determinar se ele é consistente com o de outras pessoas que, historicamente, buscaram tratamento para saúde mental. 
O objetivo é oferecer um **ponto de partida** para a reflexão sobre a necessidade de buscar ajuda profissional.
""")


@st.cache_data
def prepare_data():
    df = load_data()
    
    features = [
        'age', 'gender_group', 'family_history', 'benefits', 'care_options', 
        'anonymity', 'leave', 'work_interfere'
    ]
    target = 'treatment'
    
    df_model = df[features + [target]].copy()

    df_model['work_interfere'] = df_model['work_interfere'].fillna('Não sabe')
    df_model = df_model[(df_model['age'] >= 15) & (df_model['age'] <= 80)]
    
    df_model[target] = df_model[target].map({'Yes': 1, 'No': 0})
    df_model = df_model.dropna(subset=[target])
    df_model[target] = df_model[target].astype(int)

    X = df_model[features]
    y = df_model[target]
    
    return X, y

X, y = prepare_data()


@st.cache_resource
def train_model(X, y):
    categorical_features = X.select_dtypes(include=['object', 'category']).columns
    numerical_features = X.select_dtypes(include=np.number).columns

    numerical_transformer = SimpleImputer(strategy='median')
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                     ('classifier', RandomForestClassifier(random_state=42, n_estimators=100))])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    model_pipeline.fit(X_train, y_train)
    
    return model_pipeline, X_test, y_test


model, X_test, y_test = train_model(X, y)


st.header("Recomendação Personalizada")
st.markdown("Preencha os campos abaixo para que a IA analise o perfil e sugira se a busca por ajuda profissional pode ser benéfica.")

opcoes_pt = {
    'sim_nao': ['Não', 'Sim'],
    'sim_nao_naosei': ['Não', 'Sim', 'Não sei'],
    'opcoes_cuidado': ['Não', 'Sim', 'Não tenho certeza'],
    'facilidade_licenca': ['Um pouco fácil', 'Muito fácil', 'Não sei', 'Um pouco difícil', 'Muito difícil'],
    'interferencia_trabalho': ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Não sabe']
}

mapa_pt_para_en = {
    'Não': 'No', 'Sim': 'Yes', 'Não sei': "Don't know", 'Não tenho certeza': 'Not sure',
    'Um pouco fácil': 'Somewhat easy', 'Muito fácil': 'Very easy', 'Um pouco difícil': 'Somewhat difficult',
    'Muito difícil': 'Very difficult', 'Nunca': 'Never', 'Raramente': 'Rarely',
    'Às vezes': 'Sometimes', 'Frequentemente': 'Often'
}

with st.form("prediction_form"):
    st.subheader("Insira as características do perfil:")
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("Idade:", 15, 80, 30)
        gender_group = st.selectbox("Gênero:", options=X['gender_group'].unique())
        family_history_pt = st.selectbox("Possui histórico familiar de doença mental?", options=opcoes_pt['sim_nao'])
        benefits_pt = st.selectbox("A empresa oferece benefícios de saúde mental?", options=opcoes_pt['sim_nao_naosei'])
    with col2:
        care_options_pt = st.selectbox("Conhece as opções de cuidado mental da empresa?", options=opcoes_pt['opcoes_cuidado'])
        anonymity_pt = st.selectbox("A empresa garante anonimato?", options=opcoes_pt['sim_nao_naosei'])
        leave_pt = st.selectbox("Qual a facilidade de tirar uma licença por saúde mental?", options=opcoes_pt['facilidade_licenca'])
        work_interfere_pt = st.selectbox("Sua condição de saúde mental interfere no trabalho?", options=opcoes_pt['interferencia_trabalho'])

    submit_button = st.form_submit_button(label="Analisar Perfil")

if submit_button:
    family_history_en = mapa_pt_para_en[family_history_pt]
    benefits_en = mapa_pt_para_en[benefits_pt]
    care_options_en = mapa_pt_para_en[care_options_pt]
    anonymity_en = mapa_pt_para_en[anonymity_pt]
    leave_en = mapa_pt_para_en[leave_pt]
    work_interfere_en = mapa_pt_para_en[work_interfere_pt]

    input_data = pd.DataFrame({
        'age': [age], 'gender_group': [gender_group], 'family_history': [family_history_en],
        'benefits': [benefits_en], 'care_options': [care_options_en], 'anonymity': [anonymity_en],
        'leave': [leave_en], 'work_interfere': [work_interfere_en]
    })
    
    prediction_proba = model.predict_proba(input_data)[0]
    probability_yes = prediction_proba[1]

    st.subheader("Resultado da Análise")
    if probability_yes > 0.5:
        st.success(f"**Recomendação:** O perfil analisado é **consistente ({probability_yes:.1%})** com o de pessoas que buscaram ajuda. Considerar o apoio de um profissional de saúde mental pode ser um passo positivo.")
    else:
        st.warning(f"**Atenção:** Embora o perfil **não se alinhe ({probability_yes:.1%})** aos padrões mais comuns de quem busca ajuda, a saúde mental é uma jornada individual. É sempre válido buscar apoio se sentir necessidade.")
    st.progress(probability_yes)
    st.caption("Esta ferramenta é um auxílio de conscientização e não substitui o diagnóstico de um profissional qualificado.")


with st.expander("Ver detalhes técnicos e desempenho do modelo"):
    st.header("Avaliação de Desempenho do Modelo")

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Acurácia", f"{accuracy:.2%}")
    kpi2.metric("Precisão", f"{precision:.2%}")
    kpi3.metric("Recall", f"{recall:.2%}")

    st.markdown("""
    - **Acurácia:** Percentual de previsões corretas que o modelo fez.
    - **Precisão:** Dos perfis que o modelo sinalizou como "positivos", quantos eram de fato.
    - **Recall:** De todos os perfis "positivos" que existem, quantos o modelo conseguiu encontrar.
    """)

    st.subheader("Matriz de Confusão")
    st.write("A matriz de confusão nos ajuda a ver os acertos e erros do modelo em detalhes.")
    
    fig, ax = plt.subplots()
    ConfusionMatrixDisplay.from_estimator(model, X_test, y_test, ax=ax, cmap='Blues', display_labels=['Perfil Negativo', 'Perfil Positivo'])
    st.pyplot(fig)