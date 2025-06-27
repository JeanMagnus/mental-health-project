import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data

st.set_page_config(layout="wide")
st.title("Análise Geral do Perfil dos Participantes")
st.markdown("Esta página apresenta a distribuição das principais variáveis da pesquisa.")

df_original = load_data()

# --- TRADUÇÃO E PREPARAÇÃO DOS DADOS ---
df = df_original.copy()
df['family_history'] = df['family_history'].replace({'Yes': 'Sim', 'No': 'Não'})
df['treatment'] = df['treatment'].replace({'Yes': 'Sim', 'No': 'Não'})
df['benefits'] = df['benefits'].replace({'Yes': 'Sim', 'No': 'Não', "Don't know": 'Não sabe'})

# --- LÓGICA DE CLASSIFICAÇÃO DE GÊNERO (DA PÁGINA COMPARAÇÕES) ---
# Aplicando a mesma lógica para padronizar os gêneros em todo o app
male_terms = ['male', 'm', 'man', 'cis male', 'cis man', 'male (cis)', 'make', 'mail', 'malr', 'msle', 'maile', 'cis male']
female_terms = ['female', 'f', 'woman', 'cis female', 'cis-female/femme', 'femake', 'cis woman', 'femail']
# Agrupando Trans e Não-Binárie para consistência
trans_nb_terms = ['trans-female', 'trans woman', 'male to female', 'transfemale', 'non-binary', 'agender', 'androgyne', 'genderqueer', 'gender fluid', 'nonbinary']

def classify_gender_custom(g):
    g = str(g).strip().lower()
    if g in male_terms:
        return 'Homem'
    elif g in female_terms:
        return 'Mulher'
    elif g in trans_nb_terms:
        return 'Trans/NB'
    else:
        return 'Outro'

# Criando uma nova coluna com os gêneros limpos e agrupados
df['gender_group_classified'] = df['gender'].apply(classify_gender_custom)


# --- Filtros na Barra Lateral (usando a nova coluna de gênero) ---
st.sidebar.header("Filtros")
paises = st.sidebar.multiselect("País:", options=df["country"].unique(), default=df["country"].unique())
# O filtro agora usa a coluna de gênero classificada
generos = st.sidebar.multiselect("Gênero:", options=df["gender_group_classified"].unique(), default=df["gender_group_classified"].unique())

# Aplicando os filtros com a nova coluna de gênero
df_filtrado = df[(df["country"].isin(paises)) & (df["gender_group_classified"].isin(generos))]
df_idade_limpa = df_filtrado[(df_filtrado['age'] >= 15) & (df_filtrado['age'] <= 80)].copy()

# --- LAYOUT PRINCIPAL ---
st.markdown("### Resultados para a Seleção Atual")

# Calcula as contagens com base nos dados filtrados e na coluna de gênero classificada
total_participantes = df_filtrado.shape[0]
counts_genero = df_filtrado['gender_group_classified'].value_counts()
homens = counts_genero.get('Homem', 0)
mulheres = counts_genero.get('Mulher', 0)
# CORREÇÃO: "Outros" agora é a soma de 'Trans/NB' e 'Outro'
soma_outros = counts_genero.get('Trans/NB', 0) + counts_genero.get('Outro', 0)

# Cria as colunas para os KPIs com os valores corretos
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total de Participantes", total_participantes)
kpi2.metric("Homens", homens)
kpi3.metric("Mulheres", mulheres)
kpi4.metric("Outros Gêneros", soma_outros) # KPI agora usa a soma correta

st.markdown("---") # Linha divisória

col1, col2 = st.columns(2)

# Gráfico 1: Distribuição de Histórico Familiar
with col1:
    history_counts = df_filtrado['family_history'].value_counts().reset_index()
    history_counts.columns = ['Histórico Familiar', 'Quantidade']
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
    fig_benefits = px.pie(
        benefits_counts,
        values='Quantidade',
        names='Benefícios',
        title='<b>Distribuição: Benefícios de Saúde Mental Oferecidos</b>',
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    fig_benefits.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5, title_text=''))
    st.plotly_chart(fig_benefits, use_container_width=True)

# Gráfico de boxplot (idade x tratamento)
with col4:
    # A coluna 'treatment' já foi traduzida no início
    fig_box = px.box(df_idade_limpa, x='treatment', y='age', color='treatment',
        title='<b>Distribuição da Idade por Tratamento</b>',
        labels={"treatment": "Buscou Tratamento?", "age": "Idade"},
        color_discrete_sequence=px.colors.qualitative.Set2)

    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.markdown("Observação: Os dados de idade para o gráfico de distribuição foram filtrados entre 15 e 80 anos.")