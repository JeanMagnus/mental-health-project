import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE

# Função para treinar o modelo (corrigida e cacheada)
@st.cache_resource
def treinar_e_avaliar_modelo(df):
    """
    Executa todo o fluxo de treino e avaliação, retornando o relatório.
    """
    st.write("Cache miss: Treinando o modelo...") # Mensagem para sabermos quando o cache não é usado

    # 1. Definição das variáveis e limpeza inicial
    features = ['Age', 'family_history', 'work_interfere', 'benefits', 'Gender_clean']
    target = 'treatment'
    df_ml = df.dropna(subset=features + [target]).copy()

    # 2. Preparação dos dados
    df_ml[target] = df_ml[target].map({'Yes': 1, 'No': 0})
    X = df_ml[features]
    y = df_ml[target]
    X_encoded = pd.get_dummies(X, drop_first=True)

    # --- FLUXO CORRIGIDO ---
    # 3. DIVIDIR OS DADOS PRIMEIRO
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, stratify=y, random_state=42
    )

    # 4. APLICAR SMOTE APENAS NOS DADOS DE TREINO
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)

    # 5. Treinar o modelo com os dados de treino balanceados
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train_resampled, y_train_resampled)
    
    # 6. Avaliar o modelo nos dados de teste ORIGINAIS
    y_pred = model.predict(X_test)
    
    # Gera o relatório
    report = classification_report(y_test, y_pred, output_dict=True)
    df_report = pd.DataFrame(report).transpose()
    
    return df_report

# --- Interface do Streamlit ---
st.title("Página de Classificação e Avaliação do Modelo")

# Verifica se o DataFrame existe no estado da sessão
if 'df' in st.session_state:
    df_principal = st.session_state['df']
    st.info("DataFrame carregado com sucesso da página principal!")

    with st.spinner('Treinando e avaliando o modelo... Por favor, aguarde.'):
        # Chama a função para obter o relatório
        relatorio_df = treinar_e_avaliar_modelo(df_principal)

    st.success("Modelo treinado e avaliado!")
    st.subheader("Relatório de Classificação Final")
    st.dataframe(relatorio_df)
    st.caption("Este relatório mostra o desempenho do modelo em dados de teste que ele nunca viu, após ser treinado com a técnica de balanceamento SMOTE aplicada corretamente.")

else:
    st.error("Os dados não foram carregados. Por favor, vá para a página principal primeiro para carregar o arquivo.")