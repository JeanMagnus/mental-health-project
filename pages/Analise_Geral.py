import streamlit as st
import pandas as pd
import plotly.express as px
# Assumindo que a função load_data está no seu arquivo utils.py
from utils import load_data

st.set_page_config(layout="wide")
st.title("📊 Análise Geral do Perfil dos Participantes")
st.markdown("Esta página apresenta a distribuição das principais variáveis da pesquisa.")

df_original = load_data()

# --- TRADUÇÃO E PREPARAÇÃO DOS DADOS ---
df = df_original.copy()
df['family_history'] = df['family_history'].replace({'Yes': 'Sim', 'No': 'Não'})
df['treatment'] = df['treatment'].replace({'Yes': 'Sim', 'No': 'Não'})
df['benefits'] = df['benefits'].replace({'Yes': 'Sim', 'No': 'Não', "Don't know": 'Não sabe'})

# --- Filtros na Barra Lateral ---
st.sidebar.header("Filtros")
paises = st.sidebar.multiselect("País:", options=df["country"].unique(), default=df["country"].unique())
generos = st.sidebar.multiselect("Gênero:", options=df["gender_group"].unique(), default=df["gender_group"].unique())

df_filtrado = df[(df["country"].isin(paises)) & (df["gender_group"].isin(generos))]
df_idade_limpa = df_filtrado[(df_filtrado['age'] >= 15) & (df_filtrado['age'] <= 80)].copy()

<<<<<<< HEAD
# LAYOUT PRINCIPAL

# NOVA SEÇÃO DE KPIs DINÂMICOS
st.markdown("### Resultados para a Seleção Atual")

# Calcula as contagens com base nos dados filtrados
total_participantes = df_filtrado.shape[0]
counts_genero = df_filtrado['Gender_clean'].value_counts()
homens = counts_genero.get('Homem', 0)
mulheres = counts_genero.get('Mulher', 0)
outros = counts_genero.get('Outro/Prefiro não dizer', 0)

# Cria as colunas para os KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de Participantes", total_participantes)
kpi2.metric("Mulheres", mulheres)
kpi3.metric("Homens", homens)
kpi4.metric("Outros Gêneros", outros)

=======
# --- LAYOUT PRINCIPAL ---
st.markdown(f"**Mostrando resultados para {df_filtrado.shape[0]} participantes.**")
>>>>>>> 35390f4 (problem solved ✅)
st.markdown("---")

col1, col2 = st.columns(2)

# Gráfico 1: Distribuição de Histórico Familiar
with col1:
    history_counts = df_filtrado['family_history'].value_counts().reset_index()
    history_counts.columns = ['Histórico Familiar', 'Quantidade']
    # CORREÇÃO: Formatação/indentação
    fig_familia = px.pie(
        history_counts,
        values='Quantidade',
        names='Histórico Familiar',
        title='<b>Distribuição: Histórico Familiar de Problemas Mentais</b>'
    )
    fig_familia.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, title_text=''))
    st.plotly_chart(fig_familia, use_container_width=True)

# Gráfico 2: Distribuição da Busca por Tratamento
with col2:
    treat_counts = df_filtrado['treatment'].value_counts().reset_index()
    treat_counts.columns = ['Tratamento', 'Quantidade']
    # CORREÇÃO: Formatação/indentação
    fig_tratamento = px.pie(
        treat_counts,
        values='Quantidade',
        names='Tratamento',
        title='<b>Distribuição: Busca por Tratamento</b>',
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_tratamento.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, title_text=''))
    st.plotly_chart(fig_tratamento, use_container_width=True)

col3, col4 = st.columns(2)

# Gráfico 3: Distribuição de Benefícios
with col3:
    benefits_counts = df_filtrado['benefits'].value_counts().reset_index()
    benefits_counts.columns = ['Benefícios', 'Quantidade']
    # CORREÇÃO: Formatação/indentação
    fig_benefits = px.pie(
        benefits_counts,
        values='Quantidade',
        names='Benefícios',
        title='<b>Distribuição: Benefícios de Saúde Mental Oferecidos</b>',
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    fig_benefits.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, title_text=''))
    st.plotly_chart(fig_benefits, use_container_width=True)

# Gráfico de boxplot (idade x tratamento) (sem alteração, legenda padrão)
with col4:
    df_idade_limpa['treatment'] = df_idade_limpa['treatment'].replace({'Yes': 'Sim', 'No': 'Não'})
    fig_box = px.box(df_idade_limpa, x='treatment', y='age', color='treatment',
        title='Distribuição da Idade por Tratamento',
        labels={"treatment": "Buscou Tratamento?", "age": "Idade"},
        color_discrete_sequence=px.colors.qualitative.Set2)


    st.plotly_chart(fig_box, use_container_width=True)





st.markdown("---")


st.markdown("Observação: Os dados de idade foram filtrados entre 15 e 80 anos.")