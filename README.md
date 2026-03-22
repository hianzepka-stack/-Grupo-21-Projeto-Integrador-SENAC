1. Tema do Projeto e Integrantes
Título do Projeto: [Defina um nome criativo ou descritivo]

Integrantes do Grupo:


Caio Costa Josino

Carlos Eduardo Moraes Souza

Danylo Marques Ferreira

Fernanda Guimarães dos Santos

Hian Zepka

Rafaela de Araujo Folha

Stephanie Souza dos Reis

2. Estrutura do Repositório:

data/: Reservada para armazenar os arquivos de dados brutos (CSV, Excel, JSON). É aqui que colocaremos a base de dados escolhida.

docs/: Espaço para documentação complementar, como o roteiro do projeto, imagens de referência e capturas de tela do dashboard final.

src/: Destinada aos arquivos de configuração ou scripts da ferramenta Low Code que utilizaremos para a análise.

3. Objetivo da Análise
Entender como o tempo excessivo de tela e a falta de sono afetam o estresse dos indivíduos.

Base de Dados: Sleep, Screen Time and Stress Analysis  
*Link:* https://www.kaggle.com/datasets/jayjoshi37/sleep-screen-time-and-stress-analysis

O dataset contém 15.000 registros sintéticos que exploram a relação entre tempo de tela no celular, qualidade do sono e níveis de estresse em pessoas com diferentes estilos de vida e ocupações.

4. Planejamento das Tarefas
Caio Costa Josino: 

Carlos Eduardo Moraes Souza: 

Danylo Marques Ferreira: Objetivo e descrição

Fernanda Guimarães dos Santos: Escolha da base de dados

Hian Zepka: Responsável pela criação do grupo no github e criação da estrutura.

Rafaela de Araujo Folha: 

Stephanie Souza dos Reis: Escolha das métricas do dashboard

Entrega de todas as tarefas até o dia 22/03/2026

5. Ideia Inicial do Dashboard
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
