import pandas as pd

def main():
    df = pd.read_csv('arquivo_dados/sleep_mobile_stress_dataset_15000.csv')

    # Ajusta cabeçalhos de coluna remove espaços extras e converte para string.
    df.columns = df.columns.str.strip().astype(str)

    # renomear colunas do inglês para o português.
    coluna_traducao = {
        'user_id': 'Usuário',
        'age': 'Idade',
        'gender': 'Gênero',        
        'occupation': 'Ocupação',
        'daily_screen_time_hours': 'Horas de Tela Diárias',
        'phone_usage_before_sleep_minutes': 'Minutos de Uso do Celular antes de Dormir',
        'sleep_duration_hours': 'Duração do Sono (Horas)',
        'sleep_quality_score': 'Pontuação de Qualidade do Sono',
        'stress_level': 'Nível de Estresse',
        'caffeine_intake_cups': 'Consumo de Cafeína (Xícaras)',
        'physical_activity_minutes': 'Minutos de Atividade Física',
        'notifications_received_per_day': 'Notificações Recebidas por Dia',
        'mental_fatigue_score': 'Pontuação de Fadiga Mental'
        # adicione mais conforme as colunas reais
    }
    df = df.rename(columns=coluna_traducao)

    # traduzir valores categóricos
    valor_traducao = {
        'Male': 'Masculino',
        'Female': 'Feminino',
        'Other': 'Outro',
        'Manager': 'Gerente',
        'Doctor': 'Médico',
        'Software Engineer': 'Engenheiro de Software',
        'Student': 'Estudante',
        'Researcher': 'Pesquisador',
        'Teacher': 'Professor',
        # adicione mais conforme os valores do dataset
    }
    df = df.replace(valor_traducao)
    return df

# Exibe as colunas disponíveis (Gênero e Ocupação) para visualizar os valores únicos
def mostrar_colunas(df, nome_coluna):  
    print('Colunas disponíveis:')
    print(df.columns.tolist())
    if nome_coluna in df.columns:
        print(df[nome_coluna].value_counts())
    else:
        print(f"Coluna '{nome_coluna}' não encontrada. Verifique o nome exatamente.")


def exibir():
    print('Iniciando o processamento do dataset...')
    df = main()
    
    nome_coluna = input('Digite o nome da coluna que você quer ver (Ex: Usuário): ').strip()
    mostrar_colunas(df, nome_coluna)


if __name__ == '__main__':
    exibir()


