import streamlit as st
import plotly.express as px
from utils import load_data

st.title("🔁 Correlações entre Fatores")

df = load_data()
cols_corr = ['treatment', 'benefits', 'care_options', 'seek_help', 'anonymity', 'family_history', 'remote_work']
df_corr = df[cols_corr].copy()

for col in cols_corr:
    df_corr[col] = df_corr[col].map({'Yes': 1, 'No': 0})

df_corr = df_corr.dropna()
corr_matrix = df_corr.corr()

fig_heatmap = px.imshow(
    corr_matrix,
    text_auto=True,
    aspect="auto",
    color_continuous_scale='RdBu',
    title='Matriz de Correlação'
)
st.plotly_chart(fig_heatmap)

st.write("As correlações mais significativas envolvem histórico familiar e acesso a cuidados.")