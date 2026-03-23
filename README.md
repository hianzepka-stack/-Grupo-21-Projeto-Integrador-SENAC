1. Tema do Projeto e Integrantes
Título do Projeto: Tempo excessivo de tela e a falta de sono

Integrantes do Grupo:

Caio Costa Josino

Carlos Eduardo Moraes Souza

Danylo Marques Ferreira

Fernanda Guimarães dos Santos

Hian Zepka

Rafaela de Araujo Folha

Stephanie Souza dos Reis

2. Estrutura do Repositório:

data/: Reservada para armazenar os arquivos de dados brutos (CSV). É aqui que colocaremos a base de dados escolhida.

docs/: Espaço para documentação complementar, como o roteiro do projeto, imagens de referência e capturas de tela do dashboard final.

src/: Destinada aos arquivos de configuração ou scripts da ferramenta Low Code que utilizaremos para a análise.

app/: dashboard

3. Objetivo da Análise
Entender como o tempo excessivo de tela e a falta de sono afetam o estresse dos indivíduos.

Base de Dados: Sleep, Screen Time and Stress Analysis  
*Link:* https://www.kaggle.com/datasets/jayjoshi37/sleep-screen-time-and-stress-analysis

O dataset contém 15.000 registros sintéticos que exploram a relação entre tempo de tela no celular, qualidade do sono e níveis de estresse em pessoas com diferentes estilos de vida e ocupações.

4. Planejamento das Tarefas e Cronograma
O grupo se comunicou pelo whatsapp e nos organizamos conformes tarefas abaixo:

# Cronograma

| Data / Período       | Atividade                                                                 | Responsável                  |
|----------------------|---------------------------------------------------------------------------|------------------------------|
| *10/03*              | Apresentação do projeto pela professora                                   | Todos                        |
| *11/03 – 20/03*      | Discussões iniciais pelo WhatsApp, escolha do tema e da base de dados     | Todos                        |
| *15/03 – 21/03*      | Criação do grupo no GitHub e estrutura de pastas e README                 | Hian Zepka                   |
| *20/03 – 22/03*      | Finalização do objetivo, descrição, alimentação README                    | Danylo, Fernanda e Stephanie |
| *21/03 – 23/03*      | Sugestão dos gráficos, métricas do dashboard                              | Caio, Carlos,  e Rafaela     |
| *22/03 – 23/03*      | Últimos ajustes, revisão do README e entrega                              | Todos (Hian coordena)        |

**Prazo final de entrega:** 23/03/2026

6. Ideia Inicial do Dashboard
Métricas principais que vamos mostrar:
- Média de tempo de tela por nível de estresse
- Correlação entre horas de sono e estresse
- Tempo médio de sono por ocupação
- Porcentagem de pessoas com estresse alto que usam celular > 6h/dia

Visualizações (todas feitas com Matplotlib/Seaborn – super simples):*
1. Histograma do Tempo de Tela
2. Scatter plot: Horas de Sono × Nível de Estresse (com linha de tendência)
3. Gráfico de barras: Estresse médio por Ocupação
4. Boxplot: Qualidade do Sono por faixa de cafeína
5. Tabela de correlação (heatmap)

Tecnologia:  Pandas + Streamlit

Planejamento do Processo de ETL

1. Extração (Extract)
- Baixar o arquivo CSV do Kaggle
- Carregar com Pandas: df = pd.read_csv('data/sleep_screen_time_stress.csv')

2. Transformação (Transform) – passos simples
- Verificar e remover duplicatas: df.drop_duplicates()
- Tratar valores faltantes (se houver): df.fillna(0) ou média
- Converter colunas de texto para numérico (ex: horas de sono)
- Criar coluna nova: df['categoria_estresse'] = pd.cut(df['Stress_Level'], bins=[0,4,7,10], labels=['Baixo','Médio','Alto'])
- Calcular médias e correlações: df.groupby('Occupation')['Sleep_Hours'].mean()

3. Carga (Load)
- Salvar versão limpa: df_clean.to_csv('data/sleep_clean.csv', index=False)
- Deixar o DataFrame pronto para usar no dashboard

Fluxo visual do processo:
Extração → Limpeza → Criação de colunas → Análise básica → Arquivo limpo.
