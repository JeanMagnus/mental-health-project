# Arquivo: pages/Perfis_de_Profissionais.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.cluster import KMeans
import numpy as np

st.set_page_config(layout="wide")
st.title("Descoberta de Perfis de Profissionais (Clustering)")
st.markdown("""
Esta página usa **Aprendizagem Não Supervisionada (K-Means)** para descobrir grupos naturais (clusters) de profissionais com características semelhantes. O objetivo é identificar "personas" com base em seu ambiente de trabalho e atitudes em relação à saúde mental.
""")


@st.cache_data
def prepare_cluster_data():
    df = load_data()
    
    features_for_clustering = [
        'age', 'gender_group', 'family_history', 'benefits', 'care_options', 
        'anonymity', 'leave', 'work_interfere', 'remote_work', 'tech_company'
    ]
    
    df_cluster = df[features_for_clustering].copy().dropna()
    df_cluster = df_cluster[(df_cluster['age'] >= 15) & (df_cluster['age'] <= 80)]
    
    return df_cluster

df_cluster = prepare_cluster_data()


numerical_features = df_cluster.select_dtypes(include=np.number).columns.tolist()
categorical_features = df_cluster.select_dtypes(include=['object', 'category']).columns.tolist()

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])




st.divider() 

with st.container(border=True): 
    st.subheader("Configurações da Análise")
    col1, col2 = st.columns([3, 1]) 

    with col1:
        k = st.slider(
            "Selecione o número de perfis (clusters) a encontrar:", 
            min_value=2, 
            max_value=8, 
            value=4, 
            step=1,
            help="Escolha quantos grupos distintos você quer que a IA identifique."
        )

    with col2:
       
        st.write("")
        st.write("")
        run_button = st.button("Analisar Perfis", use_container_width=True, type="primary")



if run_button:
    
    kmeans_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('clusterer', KMeans(n_clusters=k, random_state=42, n_init=10))
    ])
    
    cluster_labels = kmeans_pipeline.fit_predict(df_cluster)
    
    df_result = df_cluster.copy()
    df_result['cluster'] = cluster_labels
    
    st.header("Análise dos Perfis Encontrados")
    st.info(f"Foram identificados **{k}** perfis distintos de profissionais. Abaixo, exploramos as características de cada um.")


    for col in ['family_history', 'benefits', 'care_options', 'anonymity', 'remote_work', 'tech_company']:
        if col in df_result.columns:
            df_result[f'{col}_numeric'] = df_result[col].apply(lambda x: 1 if x == 'Yes' else 0)

    profile_summary = df_result.groupby('cluster').agg({
        'age': 'mean',
        'family_history_numeric': 'mean',
        'benefits_numeric': 'mean',
        'care_options_numeric': 'mean',
        'remote_work_numeric': 'mean',
        'tech_company_numeric': 'mean'
    }).reset_index()

    profile_summary.columns = ['Perfil', 'Idade Média', '% com Histórico Familiar', '% com Benefícios', 
                               '% Conhece Opções', '% Trabalha Remoto', '% em Empresa de Tec.']

    st.subheader("Resumo dos Perfis")
    st.dataframe(profile_summary.style.format({
        'Idade Média': '{:.1f}', '% com Histórico Familiar': '{:.1%}', '% com Benefícios': '{:.1%}',
        '% Conhece Opções': '{:.1%}', '% Trabalha Remoto': '{:.1%}', '% em Empresa de Tec.': '{:.1%}'
    }))

    st.subheader("Visualização Comparativa dos Perfis (Gráfico de Radar)")

    profile_features = profile_summary.drop('Perfil', axis=1)
    scaler = MinMaxScaler()
    profile_scaled = pd.DataFrame(scaler.fit_transform(profile_features), columns=profile_features.columns)
    profile_scaled['Perfil'] = profile_summary['Perfil'] 

    radar_data = profile_scaled.melt(id_vars='Perfil', var_name='Característica', value_name='Valor')
    
    fig = px.line_polar(
        radar_data,
        r='Valor',
        theta='Característica',
        color='Perfil',
        line_close=True,
        title="Comparativo entre Perfis Encontrados (Valores Normalizados)",
        template="seaborn"
    )
    fig.update_traces(fill='toself')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Como interpretar o gráfico:** Todas as características foram colocadas na mesma escala (de 0 a 1) para uma comparação justa. Um valor perto de 1 significa que aquele perfil tem o valor mais alto para aquela característica em comparação com os outros perfis. Isso revela a "assinatura" de cada grupo.
    """)

else:
    st.info("Ajuste as configurações acima e clique em 'Analisar Perfis' para iniciar a descoberta.")