import requests
import json
import numpy as np
from scipy.stats import pearsonr
from datetime import datetime


# Função para obter os indicadores e séries disponíveis
def get_available_indicators_and_series(token):
    url = "https://apis.4intelligence.ai/api-feature-store/api/v1/indicators"
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data  # Retorna os dados da resposta
    else:
        print(f"Erro na requisição para obter indicadores. Código de status: {response.status_code}")
        print(f"Resposta completa da API: {response.text}")
        return None


# Função para filtrar os dados (indicador code e descrição curta)
def filter_indicator_data(indicators):
    filtered_data = []

    # Itera pelos dados dos indicadores e extrai o necessário
    for indicator in indicators.get('data', []):
        indicator_code = indicator.get('indicator_code', 'Não disponível')
        description = indicator.get('name', {}).get('pt-br', 'Não disponível')
        filtered_data.append({
            'indicator_code': indicator_code,
            'description': description
        })

    return filtered_data


# Função para obter séries dentro do código do indicador
def get_series_by_indicator(indicator_code, token):
    url = f"https://apis.4intelligence.ai/api-feature-store/api/v1/indicators/{indicator_code}/series?limit=4000"
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            return data['data']  # Retorna as séries disponíveis
        else:
            print(f"Erro ao acessar as séries do indicador {indicator_code}. A chave 'data' não foi encontrada.")
            return []
    else:
        print(f"Erro na requisição para obter séries do indicador {indicator_code}. Código de status: {response.status_code}")
        return []


# Função para obter dados históricos de uma série
def get_series_data(indicator_code, series_code, token, limit=4000):
    url = f"https://apis.4intelligence.ai/api-feature-store/api/v1/indicators/{indicator_code}/series/{series_code}/observations?limit={limit}"
    headers = {'Authorization': token}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        observations = data.get('data', [])
        if observations:
            return observations
        else:
            print(f"Nenhuma observação encontrada para a série {series_code}.")
            return None
    else:
        print(f"Erro na requisição para {series_code}. Código de status: {response.status_code}")
        return None


# Função para sincronizar as datas das duas séries
def synchronize_data(data1, data2):
    dates1 = {entry['date']: entry['value'] for entry in data1}
    dates2 = {entry['date']: entry['value'] for entry in data2}

    common_dates = set(dates1.keys()).intersection(set(dates2.keys()))

    synchronized_data1 = [(date, dates1[date]) for date in common_dates]
    synchronized_data2 = [(date, dates2[date]) for date in common_dates]

    synchronized_data1.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%dT%H:%M:%S"))
    synchronized_data2.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%dT%H:%M:%S"))

    return synchronized_data1, synchronized_data2


# Função para calcular a correlação entre duas séries
def calculate_correlation(data1, data2):
    if not data1 or not data2:
        print("Os dados das séries estão vazios ou mal formatados.")
        return None

    values1 = [entry[1] for entry in data1]
    values2 = [entry[1] for entry in data2]

    if len(values1) != len(values2):
        print(f"As séries têm tamanhos diferentes: {len(values1)} e {len(values2)}")
        return None

    values1 = np.array(values1)
    values2 = np.array(values2)

    corr, _ = pearsonr(values1, values2)

    return corr


# Função principal para buscar os dados e calcular a correlação
def main():
    token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjgyX3VOQkNKVENnU0VNX3Z2TjR2LSJ9.eyJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL2VtYWlsIjoicGVkcm8uZ3VpbGhlcm1lQGdlcy5pbmF0ZWwuYnIiLCJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL3VzZXJfbWV0YWRhdGEiOnt9LCJodHRwczovLzRpbnRlbGxpZ2VuY2UuY29tLmJyL2FwcF9tZXRhZGF0YSI6eyJyb2xlcyI6WyJpc0NsYWFTIiwiaXNGYWFTIiwiaXNGZWF0dXJlU3RvcmUiXX0sImh0dHBzOi8vNGludGVsbGlnZW5jZS5jb20uYnIvbmFtZSI6InBlZHJvLmd1aWxoZXJtZUBnZXMuaW5hdGVsLmJyIiwiaXNzIjoiaHR0cHM6Ly80aW50ZWxsaWdlbmNlLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2N2JkYWYwY2NiZGE3YzJkZDM1YTc4ZGMiLCJhdWQiOlsiNGNhc3RodWIiLCJodHRwczovLzRpbnRlbGxpZ2VuY2UuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTc0MzUzODA1MSwiZXhwIjoxNzQ2MTMwMDUxLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXpwIjoibVNLWnFINUtxMVdvY3hKY2xuSVVSYlZJS1VXUmpvSnoiLCJwZXJtaXNzaW9ucyI6WyJhc2s6cXVlc3Rpb25zIiwiY3JlYXRlOnByb2plY3QtY2xhYXMiLCJjcmVhdGU6cHJvamVjdHMiLCJjcmVhdGU6d29ya3NwYWNlcyIsImVkaXQ6Z3JvdXAtYWxlcnRzIiwiZWRpdDpteS1ncm91cHMiLCJyZWFkOmFjY2Vzcy1ncm91cHMiLCJyZWFkOmNsaWVudHMiLCJyZWFkOmRvbWFpbnMiLCJyZWFkOmdyb3VwLWFsZXJ0cyIsInJlYWQ6aW5kaWNhdG9ycyIsInJlYWQ6bXktZ3JvdXBzIiwicmVhZDpvYnNlcnZhdGlvbnMiLCJyZWFkOnByZWRlZmluZWQtZ3JvdXBzIiwicmVhZDpwcm9qZWN0LWNsYWFzIiwicmVhZDpwcm9qZWN0aW9ucyIsInJlYWQ6cHJvamVjdHMiLCJyZWFkOnNlcmllcyIsInJlYWQ6dXNlcnMiLCJyZWFkOndvcmtzcGFjZXMiXX0.nmBYpRjgv2WrbexOc1SwimdvkKZ9oK6_QsjgQqdPcXgETcRArf53mEG86Lk2cVFzjoOKOiMeQwty3d4ejUrMlTjYteHxQmS75CXUCfVA3He_35EM5gQeeUxPPTiq6DHRtuoQqUhoP6sJtVVXDjx5XtpBEhNCpyCDJANBfWudOkad9JfOuCXf_Vx4n9tJKwmlkedPj9_6IM3toTXlfByKzrBcyJoMj_3ouESaE6tw7_ijgeespd4_fmSCwxeKqje-xA1q0TRM9buS7mQRZTk_RlWkOLYO6eL1pZMnJ1qy-049RQMocRGQVmRrgZy8veoFMY1stHUFfPYzMwjC7d6J9g'

    # Passo 1: Obter os indicadores e séries disponíveis
    print("Buscando indicadores e séries disponíveis...")
    indicators = get_available_indicators_and_series(token)

    # Passo 2: Filtrar os dados para mostrar apenas o indicator_code e a descrição
    if indicators:
        filtered_data = filter_indicator_data(indicators)

        # Salvar a resposta filtrada em um arquivo de texto
        with open("indicadores_filtrados.txt", "w", encoding="utf-8") as file:
            for entry in filtered_data:
                file.write(f"Indicator Code: {entry['indicator_code']}\n")
                file.write(f"Description: {entry['description']}\n\n")

        print("Resposta filtrada salva em 'indicadores_filtrados.txt'.")

    # Passo 3: Selecione manualmente o código do indicador para analisar
    indicator_code = input("Digite o código do indicador que deseja analisar: ")

    # Obter as séries dentro do indicador escolhido
    series = get_series_by_indicator(indicator_code, token)

    if series:
        print("\nSéries disponíveis para o indicador selecionado:")
        for idx, serie in enumerate(series):
            # Ajuste: verificando as chaves de cada série
            series_code = serie.get('code', 'Código não disponível')
            name = serie.get('name', {}).get('pt-br', 'Sem nome')
            print(f"{idx + 1}. {series_code} - {name}")

        # Passo 4: Selecione manualmente as duas séries para análise
        series_code_1 = input("Digite o código da primeira série: ")
        series_code_2 = input("Digite o código da segunda série: ")

        # Obtemos os dados históricos das duas séries
        data1 = get_series_data(indicator_code, series_code_1, token)
        data2 = get_series_data(indicator_code, series_code_2, token)

        if data1 and data2:
            # Sincroniza as datas e os valores das duas séries
            synchronized_data1, synchronized_data2 = synchronize_data(data1, data2)

            # Calculando a correlação entre as duas séries
            correlation = calculate_correlation(synchronized_data1, synchronized_data2)
            if correlation is not None:
                print(f"A correlação entre as séries {series_code_1} e {series_code_2} é: {correlation:.4f}")
            else:
                print("Não foi possível calcular a correlação.")
        else:
            print("Erro ao obter os dados para as séries fornecidas.")
    else:
        print("Não foram encontradas séries para o indicador selecionado.")


if __name__ == "__main__":
    main()