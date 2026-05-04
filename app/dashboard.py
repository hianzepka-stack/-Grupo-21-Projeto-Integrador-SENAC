import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / 'data' / 'base_original.csv'

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def prepare_caffeine_category(df: pd.DataFrame) -> pd.DataFrame:
    bins = [-1, 0, 1, 2, 3, np.inf]
    labels = ['0 xícaras', '1 xícara', '2 xícaras', '3 xícaras', '4+ xícaras']
    df['caffeine_category'] = pd.cut(df['caffeine_intake_cups'], bins=bins, labels=labels)
    return df


def prepare_stress_category(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 4, 7, 10]
    labels = ['Baixo', 'Médio', 'Alto']
    df['categoria_estresse'] = pd.cut(df['stress_level'], bins=bins, labels=labels, include_lowest=True)
    return df


def main() -> None:
    st.set_page_config(page_title='Dashboard Sono, Tela e Estresse', layout='wide')
    st.title('Dashboard de Sono, Tempo de Tela e Estresse')
    st.markdown(
        'Painel de métricas usando **Pandas + Streamlit + Matplotlib/Seaborn** para explorar a relação entre qualidade do sono, tempo de tela e nível de estresse.'
    )

    df = load_data(DATA_PATH)
    required_cols = [
        'stress_level',
        'daily_screen_time_hours',
        'sleep_duration_hours',
        'occupation',
        'caffeine_intake_cups',
        'sleep_quality_score',
    ]

    if not all(col in df.columns for col in required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        st.error(f'As colunas necessárias não foram encontradas no dataset: {missing}')
        return

    df = prepare_caffeine_category(df)
    df = prepare_stress_category(df)

    st.sidebar.header('Filtros')
    min_stress = float(df['stress_level'].min())
    max_stress = float(df['stress_level'].max())
    high_stress_threshold = st.sidebar.slider(
        'Limite para estresse alto',
        min_value=min_stress,
        max_value=max_stress,
        value=7.0,
        step=0.1,
    )
    mobile_hours_threshold = st.sidebar.slider(
        'Horas de tela altas (> x horas/dia)',
        min_value=0.0,
        max_value=float(df['daily_screen_time_hours'].max()),
        value=6.0,
        step=0.5,
    )

    st.subheader('Métricas principais')
    col1, col2 = st.columns(2)

    avg_screen_by_stress = (
        df.groupby(pd.cut(df['stress_level'], bins=8), observed=False)['daily_screen_time_hours']
        .mean()
        .round(2)
    )
    correlation = df['sleep_duration_hours'].corr(df['stress_level'])
    avg_sleep_by_occupation = (
        df.groupby('occupation')['sleep_duration_hours']
        .mean()
        .sort_values(ascending=False)
        .round(2)
    )

    high_stress = df[df['stress_level'] >= high_stress_threshold]
    high_stress_mobile = high_stress[high_stress['daily_screen_time_hours'] > mobile_hours_threshold]
    pct_high_stress_mobile = (
        len(high_stress_mobile) / len(high_stress) * 100 if len(high_stress) > 0 else 0
    )

    col1.metric('Correlação sono × estresse', f'{correlation:.3f}')
    col1.metric('Tempo médio de sono por ocupação', '')
    col2.metric('Estresse alto ≥', f'{high_stress_threshold:.1f}')
    col2.metric('Pessoas com estresse alto e +6h de tela', f'{pct_high_stress_mobile:.1f}%')

    st.write('#### Média de tempo de tela por nível de estresse')
    st.dataframe(avg_screen_by_stress.reset_index().rename(columns={'stress_level': 'faixa_estresse', 'daily_screen_time_hours': 'media_tempo_tela'}))

    st.markdown('---')
    st.write('### Visualizações')

    sns.set_style('whitegrid')

    # Arrange plots in a grid for presentation style
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.histplot(df['daily_screen_time_hours'], bins=20, kde=False, color='steelblue', ax=ax1)
        ax1.set_title('Histograma do Tempo de Tela')
        ax1.set_xlabel('Horas de tela diárias')
        ax1.set_ylabel('Número de pessoas')
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(
            data=df,
            x='sleep_duration_hours',
            y='stress_level',
            hue='categoria_estresse',
            palette='viridis',
            alpha=0.8,
            s=40,
            ax=ax2,
        )
        ax2.set_title('Horas de Sono × Nível de Estresse')
        ax2.set_xlabel('Horas de sono')
        ax2.set_ylabel('Nível de estresse')
        ax2.legend(title='Categoria de Estresse', loc='upper right')
        st.pyplot(fig2)

    # Second row
    col3, col4 = st.columns(2)

    with col3:
        avg_sleep_by_occupation_sorted = avg_sleep_by_occupation.sort_values(ascending=True)
        colors = [
            '#d32f2f' if value < 6 else '#f57c00' if value < 7 else '#388e3c'
            for value in avg_sleep_by_occupation_sorted.values
        ]

        fig3, ax3 = plt.subplots(figsize=(7, 5))
        ax3.barh(
            avg_sleep_by_occupation_sorted.index,
            avg_sleep_by_occupation_sorted.values,
            color=colors,
            edgecolor='black',
            height=0.6,
        )
        ax3.set_title('Ocupações mais afetadas por baixo sono')
        ax3.set_xlabel('Horas de sono médias')
        ax3.set_ylabel('Ocupação')
        ax3.tick_params(axis='x', rotation=0)
        ax3.invert_yaxis()

        for value, label in zip(avg_sleep_by_occupation_sorted.values, avg_sleep_by_occupation_sorted.index):
            ax3.text(value + 0.08, label, f'{value:.2f}', va='center', fontsize=9)

        st.pyplot(fig3)

    with col4:
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        sns.boxplot(
            x='caffeine_category',
            y='sleep_quality_score',
            data=df,
            palette='pastel',
            ax=ax4,
        )
        ax4.set_title('Qualidade do Sono por faixa de cafeína')
        ax4.set_xlabel('Consumo de cafeína')
        ax4.set_ylabel('Pontuação de qualidade do sono')
        ax4.tick_params(axis='x', rotation=20)
        st.pyplot(fig4)

    # Heatmap in full width
    st.write('#### Heatmap de Correlação')
    corr_cols = [
        'daily_screen_time_hours',
        'sleep_duration_hours',
        'sleep_quality_score',
        'stress_level',
        'caffeine_intake_cups',
    ]
    corr_matrix = df[corr_cols].corr()

    fig5, ax5 = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt='.2f',
        cmap='coolwarm',
        center=0,
        square=True,
        ax=ax5,
    )
    ax5.set_title('Heatmap de Correlação')
    st.pyplot(fig5)

    st.markdown('---')
    st.write('##### Observações')
    st.write(
        '''
- A correlação é medida entre horas de sono e nível de estresse: valores próximos de -1 ou 1 indicam relação mais forte.
- O histograma mostra a distribuição das horas de tela.
- O boxplot compara qualidade do sono por faixa de consumo de cafeína.
        '''
    )


if __name__ == '__main__':
    main()


# ============ CÓDIGO DE teste.eduard.py ============

# CARGA DO DADO TRATADO
df_eduardo = pd.read_csv('../data/base_original.csv')

def prepare_stress_category_eduardo(df: pd.DataFrame) -> pd.DataFrame:
    bins = [0, 4, 7, 10]
    labels = ['Baixo', 'Médio', 'Alto']
    df['categoria_estresse'] = pd.cut(df['stress_level'], bins=bins, labels=labels, include_lowest=True)
    return df

df_eduardo = prepare_stress_category_eduardo(df_eduardo)

# SIDEBAR (Barra Lateral para Filtros) ---
st.sidebar.header("Filtros de Análise")
lista_ocupacoes = ["Todas"] + sorted(df_eduardo['occupation'].unique().tolist())
ocupacao_selecionada = st.sidebar.selectbox("Selecione a Ocupação:", lista_ocupacoes)

# Filtragem dos dados baseada na escolha do usuário
if ocupacao_selecionada != "Todas":
    df_filtrado = df_eduardo[df_eduardo['occupation'] == ocupacao_selecionada]
else:
    df_filtrado = df_eduardo

st.title(f" Análise de Bem-estar: {ocupacao_selecionada}")

#VISUALIZAÇÕES CIRCULARES
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("Proporção de Níveis de Estresse")
    # Gráfico de Pizza Tradicional
    dados_estresse = df_filtrado['categoria_estresse'].value_counts()
    
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        dados_estresse, 
        labels=dados_estresse.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#ff9999','#66b3ff','#99ff99'],
        explode=(0.05, 0, 0) # Destaca a primeira fatia
    )
    ax.axis('equal')
    st.pyplot(fig)

with c2:
    st.subheader("Qualidade do Sono")
    # Criando as faixas de qualidade
    df_filtrado['status_sono'] = pd.cut(
        df_filtrado['sleep_quality_score'], 
        bins=[0, 5, 8, 10], 
        labels=['Baixa', 'Regular', 'Alta'], 
        include_lowest=True
    )
    dados_sono = df_filtrado['status_sono'].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    # Grafico de rosca
    ax.pie(
        dados_sono, 
        labels=dados_sono.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=['#ffcc99','#ff6666','#c2c2f0'],
        pctdistance=0.85
    )
    
    centro_circulo = plt.Circle((0,0), 0.70, fc='white')
    fig.gca().add_artist(centro_circulo)
    
    ax.axis('equal')
    st.pyplot(fig)

st.divider()
c3, c4 = st.columns(2)

with c3:
    st.subheader(" Uso de Celular > 6h por Dia")
    # Criando categoria binária para o gráfico
    df_filtrado['uso_celular'] = df_filtrado['daily_screen_time_hours'].apply(
        lambda x: 'Excessivo (>6h)' if x > 6 else 'Moderado (<=6h)'
    )
    dados_celular = df_filtrado['uso_celular'].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        dados_celular, 
        labels=dados_celular.index, 
        autopct='%1.1f%%', 
        colors=['#ff9999','#99ff99'],
        shadow=True
    )
    ax.axis('equal')
    st.pyplot(fig)

with c4:
    st.subheader("Consumo de Cafeína")
    df_filtrado['cat_cafeina'] = df_filtrado['caffeine_intake_cups'].apply(
        lambda x: 'Muita (4+)' if x >= 4 else ('Moderada (1-3)' if x > 0 else 'Nenhuma')
    )
    dados_cafe = df_filtrado['cat_cafeina'].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        dados_cafe, 
        labels=dados_cafe.index, 
        autopct='%1.1f%%', 
        colors=['#c2c2f0','#ffb3e6','#ffcc99'],
        wedgeprops=dict(width=0.3)
    )
    ax.axis('equal')
    st.pyplot(fig)
